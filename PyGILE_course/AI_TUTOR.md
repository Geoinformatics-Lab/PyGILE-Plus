# The PyGILE tutor: marks, hints and a free AI helper

Every lesson can check your answers for you. When you run an answer cell, a small coloured box appears under it and tells you how you did. You can also add a free AI tutor that writes a short, personal hint for you.

This page explains everything, step by step. You do not need to know anything about AI.

**Contents**

- [Part 1 · Your marks (no account, no internet)](#part-1--your-marks-no-account-no-internet)
- [Part 2 · The AI tutor (optional)](#part-2--the-ai-tutor-optional)
  - [Which service should I choose?](#which-service-should-i-choose)
  - [1. Google Gemini (free)](#1-google-gemini-free)
  - [2. Groq (free, a good backup)](#2-groq-free-a-good-backup)
  - [3. OpenRouter (free, a small extra backup)](#3-openrouter-free-a-small-extra-backup)
  - [4. DeepSeek (paid, very cheap)](#4-deepseek-paid-very-cheap)
  - [When the free AI runs out](#when-the-free-ai-runs-out)
- [All the commands](#all-the-commands)
- [Problems and how to fix them](#problems-and-how-to-fix-them)
- [For teachers](#for-teachers)

---

## Part 1 · Your marks (no account, no internet)

### Turn it on

The first code cell of every lesson looks like this:

```python
# Optional: marks your answers as you go. Delete this cell to turn it off.
%run ../tools/tutor_on.py
```

Run it (click in the cell and press **Shift+Enter**). You will see:

> ✅ Answer checking is on. Run an answer cell to see your mark. Type %tutor for options, or %tutor ask and a question.

That's all. Now answer the questions as usual: type your code in the cell under the question, and press **Shift+Enter**.

### What the boxes mean

| Box | Meaning |
| --- | --- |
| ✅ **Correct** | Your result is the same as the course's own solution. Well done! |
| 🟡 **Nearly there** | Part of your result is right. The box says which part to check. |
| 🔴 **Not yet** | Your result is different, or Python found an error. The box explains the error in plain words. |
| ▶️ **It ran** | The answer is a chart or a map. A computer cannot judge a picture, so compare yours with the solution. |
| 🌍 **Your own project** | The optional exercise at the end of each part, on data from your own country. There is no single right answer, so it is not marked. With the AI tutor (Part 2), you get feedback on it. |

Under each box you also see your progress, for example **⭐ 6 of 28 questions done in this lesson**.

Some things to know:

- **There is more than one right answer.** The checker looks at your *result*, not at your exact code. You can choose your own variable names, unless the question gives one. If the question asks you to print a sentence, your own wording is fine when the numbers are right.
- **"Not yet" is not failure.** Read the message, change one thing, and run the cell again. That is how everyone learns to program.
- **Still stuck?** Open **Show solution** under the question. Then close it and try to write the answer yourself.
- The marking works **without internet and without any account**. Nothing leaves your computer.

---

## Part 2 · The AI tutor (optional)

The marks tell you *whether* your answer is right. The AI tutor tells you *why*, like a teacher sitting next to you. It writes two to four short sentences: one thing you did well, and one hint for what to change. It never gives you the whole answer.

> 🤖 You picked the item with the right idea: square brackets and an index. Remember that Python counts from 0, so the second peak is at index 1, not 2.

**You can also talk with it.** If a hint is not clear, or you want to know more, type `%tutor ask` and your question in a new cell (see [Ask the tutor a question](#ask-the-tutor-a-question)).

**It is optional.** Everything in Part 1 works without it.

**Before you start, three things to know:**

1. **Age.** Google's Gemini service is for people **18 or older**. If you are younger, use the marks in Part 1. They work for everyone.
2. **Privacy.** Only the question and your code are sent to the AI service, never your name. But free services may let their staff read what is sent, to improve their AI. So **never type personal information** (names, phone numbers, passwords) in an answer cell.
3. **Your key is like a password.** The AI service gives you a long code called an **API key**. The tutor saves it on your own computer only, in a hidden folder called `.pygile`. It is never saved in the notebook, so it is safe to share your notebooks. Do not post your key anywhere.

### Which service should I choose?

| | Service | Cost | Feedback messages per day |
| --- | --- | --- | --- |
| **Start here** | [1. Google Gemini](#1-google-gemini-free) | Free, no credit card | about 500 |
| **Good backup** | [2. Groq](#2-groq-free-a-good-backup) | Free, no credit card | about 1,000 |
| Extra backup | [3. OpenRouter](#3-openrouter-free-a-small-extra-backup) | Free, no credit card | about 50 |
| Never runs out | [4. DeepSeek](#4-deepseek-paid-very-cheap) | about US$1 for 1,500 messages | no daily limit |

**Our advice:** add **Gemini** first. Then add **Groq** as a backup. You can add as many as you like. The tutor uses the first one, and when its daily limit is used up, it moves to the next one automatically.

The numbers were checked in November 2026. Companies change their free limits from time to time.

### How to add a service (the same for all four)

1. In any lesson, make sure you have run the first code cell (Part 1).
2. Make a new cell: click **+** in the toolbar.
3. Type `%tutor setup` in the new cell and press **Shift+Enter**.
4. A list of the four services appears. Type the number you want, for example `1`, and press **Enter**.
5. The tutor shows you the steps to get your key. They are also below, for each service.
6. When you have copied your key, click in the box that says **Paste your key and press Enter**. Paste with **Ctrl+V** (on a Mac, **Cmd+V**) and press **Enter**.
   **The key stays invisible while you paste.** That is normal. It keeps your key hidden from anyone looking at your screen.
7. The tutor tests your key and says **✅ … is working!** Now run any answer cell to get your first hint.

You do this **once** per computer. The key stays saved for all lessons.

### 1. Google Gemini (free)

1. Open **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**.
2. Sign in with your Google account: the same one you use for Gmail or YouTube. No account? Make one free at [accounts.google.com/signup](https://accounts.google.com/signup).
3. The first time, Google asks you to accept its terms. Read them and accept.
4. Click the button **Create API key**.
5. A long code appears. This is your key. Click **Copy**.
6. Go back to your notebook and paste it (step 6 above).

**Limit:** about 500 feedback messages a day. It starts again every day at midnight in California, which is **about 1:45 pm in Nepal** (12:45 pm from mid-March to early November).

**Problems?** If the **Create API key** button is grey, you may be signed in with a school or company Google account that does not allow it. Sign out and use a personal Gmail account. More help: [Google's own page about keys](https://ai.google.dev/gemini-api/docs/api-key).

### 2. Groq (free, a good backup)

1. Open **[console.groq.com/keys](https://console.groq.com/keys)**.
2. Sign in with Google, with GitHub, or with your email address.
3. Click **Create API Key**. Type the name `PyGILE` and click **Submit**.
4. Click **Copy**. **Copy it now:** Groq shows the key only once. If you lose it, make a new one.
5. Go back to your notebook, type `%tutor setup`, choose **2** and paste it.

**Limit:** about 1,000 feedback messages a day.

### 3. OpenRouter (free, a small extra backup)

OpenRouter gives access to many free AI models through one key. The tutor uses its free models only, so it costs nothing.

1. Open **[openrouter.ai/keys](https://openrouter.ai/keys)**.
2. Sign up or sign in with Google, GitHub or email.
3. Click **Create API Key**, type the name `PyGILE` and click **Create**.
4. Click **Copy**. Copy it now: it is shown only once.
5. Go back to your notebook, type `%tutor setup`, choose **3** and paste it.

**Limit:** about 50 feedback messages a day.

### 4. DeepSeek (paid, very cheap)

Use this if the free services are not enough for you. You add a small amount of money first, and each feedback message takes a tiny part of it: about **US$1 for 1,500 messages**. There is no daily limit.

1. Open **[platform.deepseek.com](https://platform.deepseek.com)** and sign up.
2. Click **Top up** and add a small amount. US$2 is enough for months of practice. Check the current prices on [DeepSeek's pricing page](https://api-docs.deepseek.com/quick_start/pricing) first.
3. Click **API keys** in the menu, then **Create new API key**. Name it `PyGILE`.
4. Click **Copy**. Copy it now: it is shown only once.
5. Go back to your notebook, type `%tutor setup`, choose **4** and paste it.

**When the money runs out**, the hints stop until you top up again. Your marks keep working.

### Ask the tutor a question

When something is unclear, ask. Click **+** to add a new cell under your answer, type `%tutor ask` and your question, and press **Shift+Enter**:

```
%tutor ask why do we start counting at 0?
```

> 💬 You asked · about Q2: why do we start counting at 0?
> 🤖 Python counts the distance from the start of the list. The first item is 0 steps from the start, so its position is 0 …

- **It knows what you are working on**: the question you last ran, your code, what it showed and the hint it gave. You do not need to copy any of that.
- **Keep asking.** Each new `%tutor ask` continues the same conversation, so you can say *"I still don't get it"* or *"show me a smaller example"*.
- **A new question starts a new conversation.** When you run the answer to another question, the tutor starts fresh. Running the same answer again keeps the conversation, with your new code.
- **Long questions** can go on several lines in the same cell, as long as the cell starts with `%tutor ask`.
- **Any language.** You can ask in Nepali or English; the tutor answers in the language you write in.
- It explains and gives hints, but it does not write the whole answer for you. The full answer is always under **Show solution**.
- Each question uses one message of your daily limit, like a hint does. The privacy rule above applies here too: never type personal information.

### When the free AI runs out

If you practise a lot, you may use up a free daily limit. Then the box under your answer says so, and tells you what you can do:

- **Wait and keep practising.** Your ✅ marks always work. The limit starts again the next day (for Gemini, at about 1:45 pm Nepal time).
- **Add a free backup.** Type `%tutor setup` and add another free service, for example Groq. The tutor then moves to it automatically when the first one is used up.
- **Never run out.** Add DeepSeek (about US$1 for 1,500 messages).

---

## All the commands

Type a command in any cell of a lesson, after you have run the first code cell, and press **Shift+Enter**.

| Command | What it does |
| --- | --- |
| `%tutor` | Shows what is on, and which AI services you have added |
| `%tutor ask` *your question* | Asks the AI tutor about the answer you last ran (see [Ask the tutor a question](#ask-the-tutor-a-question)) |
| `%tutor setup` | Adds an AI service, step by step |
| `%tutor help` | Shows a link to this page |
| `%tutor progress` | Shows how many questions you have done in each lesson |
| `%tutor ai off` | Pauses the AI hints (`%tutor ai on` starts them again) |
| `%tutor remove gemini` | Removes a saved service and its key (also `groq`, `openrouter`, `deepseek`) |
| `%tutor off` | Stops the marking in this notebook (`%tutor on` starts it again) |
| `%tutor reset` | Clears your progress stars |

---

## Problems and how to fix them

**No box appears under my answer.**
- Run the first code cell of the lesson (`%run ../tools/tutor_on.py`) again.
- Use **JupyterLab**, which the PyGILE-Plus Docker image opens for you. Other notebook programs may not tell the tutor which question you are answering.

**It says "Not yet", but I think my answer is right.**
- Open **Show solution** and compare the *result*, not the code.
- Check the variable name. You may choose your own name when the question does not give one. But if the question says to store something in `town_elevations_m`, use exactly that name.
- If you ran some cells twice, the values may have changed. Click **Kernel → Restart Kernel and Run All Cells**, then run your answer again.
- With the AI tutor on, it can recognise a different correct method and change the mark to ✅.

**The box for the key did not appear, or I pressed Enter by mistake.**
Type `%tutor setup` again. Nothing is changed until a key works.

**"… did not accept your key".**
Copy the key again, carefully, with nothing before or after it. If you lost it, make a new key on the service's page and run `%tutor setup` again.

**"Could not connect to the AI service".**
Check your internet connection. Your marks still work offline.

**I use a shared or lab computer.**
Your key is saved for the computer's user account. When you finish, type `%tutor remove gemini` (and any other service you added), so the next person does not use your key.

**I want to remove everything.**
Delete the folder `.pygile` in your home folder (on Windows: `C:\Users\YourName\.pygile`). It holds only your keys and progress stars.

---

## For teachers

- **How marking works.** `tools/build_answer_key.py` runs every lesson with each hidden solution in place of the learner's answer cell, and saves what each solution prints, shows and stores in `tools/answer_key.json`. The tutor (`tools/pygile_tutor.py`) compares the learner's result with it. It knows which question a cell answers from the cell's ID, which JupyterLab sends with every run. No AI is involved in marking.
- **After editing a lesson,** rebuild its key in the Docker image (in a JupyterLab terminal):
  `python PyGILE_course/tools/build_answer_key.py A_Python/A03_Lists_and_loops.ipynb`
  (with no file name, it rebuilds all lessons).
- **The AI tutor** sends the question, the hidden solution, the learner's code and output, and the automatic mark to the learner's chosen service. Its instructions follow the course style guide: short, warm, one hint, never the full solution. It may raise a mark (for a valid answer solved another way) but never lowers one.
- **Other AI servers.** Any server with an OpenAI-style API works, including Ollama on a lab computer: add `"url"` and `"model"` to a service in `~/.pygile/tutor.json`.
