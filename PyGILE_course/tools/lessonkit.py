"""Helpers that build PyGILE lesson notebooks in one consistent format.

A lesson script does:

    from lessonkit import Lesson
    L = Lesson("A1 · Python as your calculator: the mountains of Nepal",
               time="45 minutes", needs="Nothing. This is the first lesson.",
               outcomes=["...", "...", "..."], intro="One short paragraph.")
    L.step("1. Running code", theory="...", examples=["print('hi')"], after="optional text")
    L.q1("question text", "solution code", "why it works")
    L.q2(...); L.q3(...)
    L.breaks(theory_before="...", code="Everest - 1", explanation="...")
    L.review("Exercise title", "question", "solution code", "why")
    L.recap([...], glossary=[("word", "meaning"), ...], next_text="...")
    L.save("A01_Python_as_your_calculator.ipynb")

The scripts that first built the 39 lessons are not kept in this repository,
so the notebooks themselves are the source: edit them directly.
Use this module to start a new lesson in the standard format, then run
add_nav.py, check_repo.py and qa.py.
"""
import nbformat as nbf

_LEVEL = {1: "one line", 2: "two lines", 3: "three lines"}


def _solution(code, why):
    why_txt = f"\n\n{why}" if why else ""
    return (
        "<details>\n<summary><b>Show solution</b></summary>\n\n"
        f"```python\n{code.strip()}\n```{why_txt}\n</details>"
    )


class Lesson:
    def __init__(self, title, time, needs, outcomes, intro=""):
        self.cells = []
        self.qn = 0
        outs = "\n".join(f"> {i}. {o}" for i, o in enumerate(outcomes, 1))
        text = (
            f"# {title}\n\n> **Time:** {time}  \n> **You need:** {needs}  \n"
            f"> **By the end you can:**\n{outs}"
        )
        if intro:
            text += f"\n\n{intro.strip()}"
        text += (
            "\n\n**How to practise:** after every step there are three questions. "
            "**Q1** needs one line of code, **Q2** two lines, **Q3** about three. "
            "Type your answer in the empty cell under each question, run it, then open "
            "**Show solution** to check. Try first, even if you are not sure: "
            "struggling for a few minutes is how the skill grows."
        )
        self.md(text)

    # basic cells -------------------------------------------------------
    def md(self, text):
        self.cells.append(nbf.v4.new_markdown_cell(text.strip()))

    def code(self, src, tags=None):
        c = nbf.v4.new_code_cell(src.strip())
        if tags:
            c.metadata["tags"] = list(tags)
        self.cells.append(c)

    # a teaching step -----------------------------------------------------
    def step(self, heading, theory, examples=(), after=None):
        self.qn = 0
        self.md(f"## {heading}\n\n{theory.strip()}")
        for ex in examples:
            self.code(ex)
        if after:
            self.md(after)

    def _q(self, level, question, solution, why):
        self.qn += 1
        if self.qn == 1:
            self.md("### Practice")
        self.md(f"**Q{level} · {_LEVEL[level]}:** {question.strip()}")
        self.code(f"# Q{level}: your answer\n")
        self.md(_solution(solution, why))

    def q1(self, question, solution, why=""):
        self._q(1, question, solution, why)

    def q2(self, question, solution, why=""):
        self._q(2, question, solution, why)

    def q3(self, question, solution, why=""):
        self._q(3, question, solution, why)

    # errors on purpose ---------------------------------------------------
    def breaks(self, heading, theory_before, code, explanation):
        self.md(f"## {heading}\n\n{theory_before.strip()}")
        self.code(code, tags=["raises-exception"])
        self.md(explanation)

    # end of lesson -------------------------------------------------------
    def review_intro(self, text=None):
        self.md(
            "## Mixed review\n\n"
            + (text or "These exercises combine everything in this lesson. "
               "Each one needs 5 to 10 lines. Plan in words first, then write the code.")
        )

    def review(self, title, question, solution, why=""):
        self.md(f"### {title}\n\n{question.strip()}")
        self.code("# Your answer\n")
        self.md(_solution(solution, why))

    def recap(self, points, glossary, next_text):
        pts = "\n".join(f"- {p}" for p in points)
        rows = "\n".join(f"| {w} | {m} |" for w, m in glossary)
        self.md(
            f"## Recap\n\n{pts}\n\n### Words you learned\n\n| Word | Meaning |\n| --- | --- |\n{rows}"
            f"\n\n## Next\n\n{next_text.strip()}"
        )

    def save(self, path):
        nb = nbf.v4.new_notebook()
        nb.cells = self.cells
        nb.metadata = {
            "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        }
        nbf.validate(nb)
        nbf.write(nb, path)
        n_q = sum(1 for c in self.cells if c.cell_type == "markdown" and c.source.startswith("**Q"))
        print(f"saved {path}: {len(self.cells)} cells, {n_q} practice questions")
