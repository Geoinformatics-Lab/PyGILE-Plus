"""Quality check for a PyGILE lesson notebook.

1. Runs the notebook as a learner would receive it (answer cells empty).
2. Runs it again with every answer cell replaced by its hidden solution,
   so every solution is proven to run in order, and prints each solution's output.

Usage: python qa.py lesson.ipynb [--quiet]
Exit code 1 if anything fails.
"""
import copy, re, sys, os
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellTimeoutError

path = sys.argv[1]
quiet = "--quiet" in sys.argv
nb = nbformat.read(path, as_version=4)
workdir = os.path.dirname(os.path.abspath(path))
ok = True


def run(notebook, attempts=3):
    # Errors inside cells never raise here (allow_errors=True); they are read
    # from the outputs below. An exception therefore means the kernel itself
    # failed, for example two lessons run in parallel picking the same port.
    # That is not the lesson's fault, so try again with a fresh kernel.
    original = copy.deepcopy(notebook)
    for attempt in range(1, attempts + 1):
        try:
            NotebookClient(notebook, timeout=180, kernel_name="python3", allow_errors=True,
                           resources={"metadata": {"path": workdir}}).execute()
            break
        except CellTimeoutError:
            raise
        except Exception as e:  # kernel did not start or died
            if attempt == attempts:
                raise
            print(f"Kernel problem ({type(e).__name__}: {e}); retrying, attempt {attempt + 1}")
            notebook.cells = copy.deepcopy(original.cells)
    errs = []
    for i, c in enumerate(notebook.cells):
        if c.cell_type != "code":
            continue
        expected = "raises-exception" in c.metadata.get("tags", [])
        got = [o for o in c.outputs if o.output_type == "error"]
        if got and not expected:
            errs.append((i, f"{got[0].ename}: {got[0].evalue}"))
        if expected and not got:
            errs.append((i, "expected an error (raises-exception) but none was raised"))
    return errs


# 1. learner version
e1 = run(copy.deepcopy(nb))
for i, e in e1:
    print(f"FAIL learner run, cell {i}: {e}")
ok &= not e1

# 2. solution version
sol_nb = copy.deepcopy(nb)
pat = re.compile(r"```python\n(.*?)\n```", re.S)
mapping = []
for i, c in enumerate(sol_nb.cells):
    if c.cell_type == "code" and (c.source.startswith("# Q") or c.source.startswith("# Your answer")):
        nxt = sol_nb.cells[i + 1] if i + 1 < len(sol_nb.cells) else None
        m = pat.search(nxt.source) if nxt is not None and nxt.cell_type == "markdown" else None
        if not m or "<details>" not in nxt.source:
            print(f"FAIL cell {i}: answer cell without a solution block after it")
            ok = False
            continue
        c.source = m.group(1)
        mapping.append(i)
e2 = run(sol_nb)
for i, e in e2:
    print(f"FAIL solution run, cell {i}: {e}\n   code: {sol_nb.cells[i].source[:120]!r}")
ok &= not e2

if not quiet:
    for i in mapping:
        c = sol_nb.cells[i]
        out = []
        for o in c.outputs:
            if o.output_type == "stream":
                out.append(o.text.strip())
            elif "data" in o:
                out.append(o.data.get("text/plain", "[image]" if "image/png" in o.data else ""))
        q = sol_nb.cells[i - 1].source.splitlines()[0][:70]
        print(f"[{i}] {q}\n     -> {' | '.join(out)[:200]}")

n_q = len(mapping)
print(f"{'PASS' if ok else 'FAIL'}: {os.path.basename(path)} — {len(nb.cells)} cells, {n_q} questions with solutions")
sys.exit(0 if ok else 1)
