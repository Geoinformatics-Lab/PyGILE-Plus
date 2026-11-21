"""Add or refresh the navigation bar at the top and bottom of every lesson.

The course order is the alphabetical order of the lesson files inside the part
folders (A_Python, B_Vector, ...). Run this after adding, renaming or rebuilding
a lesson, from anywhere:

    python PyGILE_course/tools/add_nav.py

With --check it changes nothing and exits with code 1 if any bar is out of date
(the automatic tests use this).
"""
import sys
from pathlib import Path
import nbformat

COURSE = Path(__file__).resolve().parents[1]
MARK = "<!-- pygile-nav -->"


def lessons():
    parts = sorted(p for p in COURSE.iterdir() if p.is_dir() and p.name[:2] in
                   {"A_", "B_", "C_", "D_", "E_"})
    return [nb for part in parts for nb in sorted(part.glob("[A-E][0-9][0-9]_*.ipynb"))]


def title(path):
    first = nbformat.read(path, as_version=4).cells[0].source.splitlines()[0]
    return first.lstrip("# ").strip()


def link(src, dst):
    rel = Path("..") / dst.parent.name / dst.name if src.parent != dst.parent else Path(dst.name)
    return f"[{title(dst)}]({rel.as_posix()})"


def with_nav(path, i, all_lessons):
    """Return the notebook at `path` with fresh navigation bars."""
    nb = nbformat.read(path, as_version=4)
    nb.cells = [c for c in nb.cells if MARK not in c.source]   # remove old bars
    prev_txt = (f"← Previous: {link(path, all_lessons[i - 1])}" if i > 0
                else "← You are at the start")
    next_txt = (f"Next: {link(path, all_lessons[i + 1])} →" if i < len(all_lessons) - 1
                else "You have reached the end of the course")
    bar = (f"{MARK}\n**PyGILE Course** · lesson {i + 1} of {len(all_lessons)} · "
           f"[Course home](../README.md)  \n{prev_txt} · {next_txt}")
    nb.cells.insert(1, nbformat.v4.new_markdown_cell(bar))
    nb.cells.append(nbformat.v4.new_markdown_cell(bar))
    return nb


def sources(nb):
    return [c.source for c in nb.cells]


def main(check=False):
    all_lessons = lessons()
    stale = []
    for i, path in enumerate(all_lessons):
        new = with_nav(path, i, all_lessons)
        if check:
            if sources(new) != sources(nbformat.read(path, as_version=4)):
                stale.append(path)
        else:
            nbformat.write(new, path)
            print(f"{i + 1:2d}. {path.parent.name}/{path.name}")
    if check:
        for path in stale:
            print(f"Navigation bar out of date: {path.relative_to(COURSE)}")
        if stale:
            print("Run: python PyGILE_course/tools/add_nav.py")
        return not stale
    return True


if __name__ == "__main__":
    sys.exit(0 if main(check="--check" in sys.argv) else 1)
