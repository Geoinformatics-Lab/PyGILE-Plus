"""Build answer_key.json, which the PyGILE tutor uses to mark answers.

For each lesson it runs the notebook with every answer cell replaced by its
hidden solution (as qa.py does), and records for each answer cell:
  - what the solution prints or shows,
  - a fingerprint of each variable the solution creates or changes,
  - whether it draws a picture.

Run it in the pygile environment after changing any lesson:

    python PyGILE_course/tools/build_answer_key.py                 # every lesson
    python PyGILE_course/tools/build_answer_key.py A_Python/A03_Lists_and_loops.ipynb

Lessons not named on the command line keep their existing entries.
"""
import copy
import json
import os
import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

TOOLS = Path(__file__).resolve().parent
COURSE = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import add_nav  # noqa: E402
from pygile_tutor import ANSWER_STARTS, KEY_FILE, OWN_START, names_in  # noqa: E402

SOL = re.compile(r"```python\n(.*?)\n```", re.S)
MARK = "<<PYGILE-VARS>>"
# Questions with a personal answer ("print your own name"): any text is right,
# so the tutor checks only that the right number of lines is printed.
OPEN = re.compile(r"\byour (own )?name\b|\byour (town|village|city|home|school)\b", re.I)
ADDRESS = re.compile(r" at 0x[0-9a-fA-F]+>")
# Solutions whose printed result changes from run to run (timings, unseeded random
# numbers): their output is not compared, only their variables.
UNSTABLE = re.compile(r"perf_counter|time\.time\(|datetime\.now|date\.today|(?<![\w.])random\.(?!seed)"
                      r"|np\.random\.(?!seed|default_rng\(\d)")


def label_of(question_md):
    first = question_md.strip().splitlines()[0] if question_md.strip() else ""
    m = re.match(r"\*\*(Q\d) · ([^*:]+):?\*\*", first)
    if m:
        return m.group(1)
    return first.lstrip("#").strip()[:60]


def build(path):
    rel = path.relative_to(COURSE).as_posix()
    nb = nbformat.read(path, as_version=4)
    run = copy.deepcopy(nb)
    cells, answers = [], []
    setup = nbformat.v4.new_code_cell(
        f"import sys as _s, json as _j\n_s.path.insert(0, {str(TOOLS)!r})\n"
        "from pygile_tutor import fingerprint as _fp")
    cells.append(setup)
    own = []
    for i, c in enumerate(run.cells):
        if c.cell_type == "code" and c.source.lstrip().startswith(OWN_START):
            own.append(c.id)                  # open exercise: nothing to run or record
            cells.append(c)
        elif c.cell_type == "code" and c.source.lstrip().startswith(ANSWER_STARTS):
            nxt = run.cells[i + 1] if i + 1 < len(run.cells) else None
            m = SOL.search(nxt.source) if nxt is not None and nxt.cell_type == "markdown" else None
            if not m:
                print(f"  skip cell {i}: no solution after it")
                cells.append(c)
                continue
            names = names_in(m.group(1))
            question = run.cells[i - 1].source
            # A variable is required only if the question names it; helper names are free.
            named = set(re.findall(r"`([A-Za-z_]\w*)", question))   # `trek`, `peaks[0]`, `x = ...`
            required = [n for n in names if n in named]
            sol = nbformat.v4.new_code_cell(m.group(1))
            probe = nbformat.v4.new_code_cell(
                f"print({MARK!r} + _j.dumps({{n: _fp(globals()[n]) for n in {names!r} "
                f"if n in globals() and not callable(globals()[n]) "
                f"and type(globals()[n]).__name__ != 'module'}}))")
            answers.append({"id": c.id, "label": label_of(question), "required": required,
                            "open": bool(OPEN.search(question)),
                            "sol": sol, "probe": probe})
            cells += [sol, probe]
        else:
            cells.append(c)
    run.cells = cells
    os.environ.setdefault("MPLBACKEND", "Agg")
    NotebookClient(run, timeout=300, kernel_name="python3", allow_errors=True,
                   resources={"metadata": {"path": str(path.parent)}}).execute()

    out = {}
    for a in answers:
        printed, shown, image, error = [], [], False, None
        for o in a["sol"].outputs:
            if o.output_type == "stream" and o.name == "stdout":
                printed.append(o.text)
            elif o.output_type == "execute_result":
                txt = o.data.get("text/plain", "")
                if ADDRESS.search(txt):          # a map or other rich object: a picture
                    image = True
                else:
                    shown.append(txt)
            elif o.output_type == "display_data" and ({"image/png", "text/html"} & set(o.get("data", {}))):
                image = True
            elif o.output_type == "error":
                error = f"{o.ename}: {o.evalue}"
        variables = {}
        for o in a["probe"].outputs:
            if o.output_type == "stream" and MARK in o.text:
                variables = json.loads(o.text.split(MARK, 1)[1])
        if error:
            print(f"  WARNING {a['label']} ({a['id']}): solution raised {error}")
        output = ("".join(printed) + ("\n" + "\n".join(shown) if shown else "")).strip()
        out[a["id"]] = {"lesson": rel, "label": a["label"], "output": output,
                        "vars": variables, "required": a["required"], "image": image}
        if a["open"]:
            out[a["id"]]["open"] = True
        if UNSTABLE.search(a["sol"].source):
            out[a["id"]]["unstable"] = True
    for cell_id in own:
        out[cell_id] = {"lesson": rel, "label": "Your own country", "free": True, "output": "",
                        "vars": {}, "required": [], "image": False}
    return rel, out


def main(paths):
    key = json.loads(KEY_FILE.read_text(encoding="utf-8")) if KEY_FILE.exists() else {
        "answers": {}, "lessons": {}}
    targets = [COURSE / p for p in paths] if paths else add_nav.lessons()
    for path in targets:
        print(f"{path.relative_to(COURSE)} …")
        rel, entries = build(path)
        key["answers"] = {k: v for k, v in key["answers"].items() if v["lesson"] != rel}
        key["answers"].update(entries)
        key["lessons"][rel] = sum(1 for e in entries.values() if not e.get("free"))
        print(f"  {len(entries)} answers")
    key["lessons"] = dict(sorted(key["lessons"].items()))
    KEY_FILE.write_text(json.dumps(key, indent=0, ensure_ascii=False, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"Saved {KEY_FILE.relative_to(COURSE.parent)}: {len(key['answers'])} answers, "
          f"{len(key['lessons'])} lessons")


if __name__ == "__main__":
    main(sys.argv[1:])
