# PyGILE Course Style Guide

How every lesson in `PyGILE_course/` is written, so that the whole course reads as one book and a complete beginner never needs another resource for the foundations.

## Who we write for

Someone who has never written code and never studied GIS. Assume nothing. Every word that is not everyday English is explained the first time it appears.

## The shape of a lesson

1. **Header card** (one text cell)
   - Title: `A3 · Lists and loops: the eight-thousanders`
   - Time needed, what you need to know first, and three "By the end you can…" outcomes.
2. **Steps** (5 to 8 per lesson). Every step has exactly this order:
   1. **Theory** — one text cell, 3 to 8 short sentences. One idea only. Plain English. Introduce new words in **bold**.
   2. **Example** — one or two code cells that show the idea working on Nepal data. Comment lines that matter.
   3. **Reading the example** (optional) — one short text cell explaining what just happened, if it is not obvious.
   4. **Practice** — three questions, always in this order:
      - **Q1 · one line** — answerable with a single line of code. Repeats the example with a small change.
      - **Q2 · two lines** — needs two lines. Combines this step with something earlier.
      - **Q3 · three lines** — needs about three lines. A small real problem.

      Each question is a text cell with the question, then an empty code cell starting with `# Q1: your answer`, then a text cell with the hidden solution (see below).
3. **When it breaks** — at least one cell per lesson that raises a real error on purpose, with the tag `raises-exception`, followed by an explanation of how to read that error.
4. **Mixed review** — 3 to 5 longer exercises (5 to 10 lines) that combine the whole lesson. Same hidden-solution format.
   The last lesson of each part (A12, B12, C9, D6) then has **Your own country (optional)**: an open task that repeats the part's main skills on a place the learner chooses. Its code cell starts with `# Your own country`; it has no hidden solution and is not marked, and the AI tutor gives feedback on it. Code that needs the internet (downloads) goes in a fenced block in the text, never in a code cell.
5. **Recap** — five bullet points.
6. **Words you learned** — a two-column table.
7. **Next** — one sentence about the next lesson.

## Hidden solutions

~~~html
<details>
<summary><b>Show solution</b></summary>

```python
code here
```

One or two sentences explaining *why* it works.
</details>
~~~

The blank line after `</summary>` is required, or the code will not render in JupyterLab.

## Code rules

- Every notebook runs from top to bottom with **Restart Kernel and Run All Cells** with no errors, except cells tagged `raises-exception`.
- Empty answer cells contain only a comment, so they run without errors.
- Exercise solutions never depend on the learner's own answer cells. If a later example needs a variable, define it in an example cell, not in a question.
- Variable names say what they hold and include units: `height_m`, `rainfall_mm`, `area_km2`.
- Use only Python's standard library, NumPy, pandas and Matplotlib in Part A. GeoPandas and rasterio start in Part B.
- Read data with `pathlib` from the course data folder: `DATA = Path("..") / "data"`.
- Open text files with `encoding="utf-8"` (`open(..., encoding="utf-8")`, `.read_text(encoding="utf-8")`), as taught in A7. Without it, Windows may read the file in another encoding and garble characters such as `²` or `°`.
- No `!pip install`, no internet access, no absolute paths.
- Notebooks are saved **without outputs**.
- Before committing, run `python PyGILE_course/tools/check_repo.py` and `python PyGILE_course/tools/qa.py <lesson>`. The automatic tests run both on every pull request.
- After changing a lesson's questions or solutions, rebuild the tutor's answer key in the `pygile` environment: `python PyGILE_course/tools/build_answer_key.py <lesson>` (paths relative to `PyGILE_course/`). `check_repo.py` fails if the key is out of date. See [AI_TUTOR.md](AI_TUTOR.md#for-teachers).

## Writing rules

- Short sentences (under 25 words). Short paragraphs (3 sentences at most).
- Address the learner as "you". Be warm and direct, never childish.
- Never say "simply", "just", "obviously" or "easy". What is easy for us is not easy for a beginner.
- SI units. Write large numbers with commas in text (8,849 m) and without commas in code (`8849`).
- Use the facts sheet below. Any number that is not on it must be labelled as illustrative, for example "(made-up values for practice)".

## Facts sheet (verified; use these values)

| Fact | Value |
| --- | --- |
| Mount Everest (Sagarmatha) | 8,849 m |
| Kanchenjunga | 8,586 m |
| Lhotse | 8,516 m |
| Makalu | 8,485 m |
| Cho Oyu | 8,188 m |
| Dhaulagiri I | 8,167 m |
| Manaslu | 8,163 m |
| Annapurna I | 8,091 m |
| First ascents | Annapurna I 1950, Everest 1953, Cho Oyu 1954, Makalu 1955, Kanchenjunga 1955, Lhotse 1956, Manaslu 1956, Dhaulagiri I 1960 |
| Approximate elevations | Kathmandu 1,400 m · Pokhara 822 m · Lukla 2,860 m · Namche Bazaar 3,440 m · Everest Base Camp 5,364 m · Jomsom 2,720 m |
| Provinces of Nepal (7) | Koshi, Madhesh, Bagmati, Gandaki, Lumbini, Karnali, Sudurpashchim |
| Administrative units | 7 provinces, 77 districts, 753 local levels |
| Population (2021 census) | 29,164,578 |
| Gorkha earthquake | 25 April 2015, magnitude 7.8 |
| Melamchi flood | June 2021, Sindhupalchok district |
| Unit conversions | 1 m = 3.28084 ft · 1 km = 1,000 m · 1 km² = 1,000,000 m² |

Peak coordinates for the data files are approximate summit positions in decimal degrees (WGS84).

## File names

`A03_Lists_and_loops.ipynb`: part letter, two-digit lesson number, short title with underscores.
