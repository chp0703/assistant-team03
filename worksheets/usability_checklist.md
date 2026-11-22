# Usability checklist — Lab 7 chat UI (Part E)

Tick every line against the **integrated** chat page (`ui/app.py` after the
starter, API client and chat page are merged). Do not tick a line until you have
seen it on screen. If a line fails, fix it (most fixes are one line) or open an
issue and link it in the "Notes" column.

**How to run the page under test**

```bash
# terminal 1 — backend (API, port 8000)
uvicorn assistant_api.main:create_app --factory
# terminal 2 — UI (port 8501)
streamlit run ui/app.py
```

| Field | Value |
|-------|-------|
| Commit / tag tested | |
| Date | |
| Checked by (GitHub username) | |
| Browser + window width(s) | |

---

## 1. Four rules for an assistant UI (Part A.2)

| # | Check | How to verify | ✓ | Notes |
|---|-------|---------------|---|-------|
| 1.1 | **Say what it can do** — a welcome message explains what the assistant helps with | open a new tab; read the page before typing anything | [ ] | |
| 1.2 | Example questions are shown and clicking one asks it | click an example in the sidebar | [ ] | |
| 1.3 | **Show your sources** — every normal answer shows `Sources: <id> — <title>` | ask "Can I register my thesis with 118 credits?" | [ ] | |
| 1.4 | **Fail politely** — every error is one human sentence plus a next step; no status code, exception or stack trace is visible | go through section 2 below | [ ] | |
| 1.5 | **Say it is an AI** — the page says it is an AI assistant | look at the sidebar / header | [ ] | |
| 1.6 | The page points to a human for important decisions (Training Office, room I.101) | read the sidebar; ask an out-of-scope question | [ ] | |

## 2. Every state the backend can produce (Parts A.1 and D.4)

| # | Situation | Try | Expected on screen | ✓ | Notes |
|---|-----------|-----|--------------------|---|-------|
| 2.1 | normal answer | "Can I register my thesis with 118 credits?" | answer + "Sources: H26#5.3 — …" | [ ] | |
| 2.2 | waiting | ask any question and watch | a "Thinking…" spinner; the user cannot send twice by accident | [ ] | |
| 2.3 | empty question | press Enter on an empty box | nothing is sent; no error, no empty bubble | [ ] | |
| 2.4 | too long question (> 2000 chars) | paste a very long text | "Please type a question (1–2000 characters)." | [ ] | |
| 2.5 | assistant does not know (`escalate: true`) | "what is the capital of France" | blue note: who can help — Training Office, room I.101 | [ ] | |
| 2.6 | AI helper down, backup used (`degraded: true`) | run the backend with the AI helper disabled / failing | small note: "Shown directly from the source document…" | [ ] | |
| 2.7 | backend down | stop the API (Ctrl+C in terminal 1), ask again | "Cannot reach the assistant…" instead of a crash; red message at the top | [ ] | |
| 2.8 | too many questions (429) | send many questions quickly | "Too many questions in a short time. Please wait a minute." | [ ] | |
| 2.9 | slow backend (timeout) | make the API slow / point to a non-responding host | "The assistant is taking too long. Please try again." | [ ] | |

## 3. Feedback 👍 / 👎 (Part D.3)

| # | Check | How to verify | ✓ | Notes |
|---|-------|---------------|---|-------|
| 3.1 | 👍 shows a "Thanks" toast and the buttons disappear for that answer | click 👍 | [ ] | |
| 3.2 | 👎 shows "Thanks — we will look at this answer." and the buttons disappear | click 👎 | [ ] | |
| 3.3 | Each answer can be rated only once; other answers keep their buttons | ask 2 questions, rate the first | [ ] | |
| 3.4 | Several answers on the page do not cause a `DuplicateWidgetID` error | ask 3+ questions | [ ] | |
| 3.5 | Error messages (section 2) do not show 👍 / 👎 buttons | trigger 2.7 | [ ] | |

## 4. Conversation and session

| # | Check | How to verify | ✓ | Notes |
|---|-------|---------------|---|-------|
| 4.1 | The chat history stays on screen after each new question | ask 3 questions | [ ] | |
| 4.2 | Two browser tabs are two separate conversations (own `session_id`) | open a second tab | [ ] | |
| 4.3 | The UI talks to the backend only through the API (`ui/` never imports `assistant_core`) | `grep -rn "assistant_core" ui/` returns nothing | [ ] | |

## 5. Accessibility basics (Part E.2)

| # | Check | How to verify | ✓ | Notes |
|---|-------|---------------|---|-------|
| 5.1 | Important information is real text, not only an emoji or a colour (e.g. the 👎 toast has a sentence) | read every message without looking at colour | [ ] | |
| 5.2 | Sentences are short and plain | read the welcome text, notes and errors aloud | [ ] | |
| 5.3 | The page works at phone width (~375 px): no text cut off, input box reachable, sources readable | shrink the browser window / use device mode | [ ] | |
| 5.4 | The page title in the browser tab says what the page is | look at the tab | [ ] | |

## 6. Two-minute hallway test (Part E.3)

Ask a classmate from **another team** to use the page for two minutes without
any explanation. Watch silently; do not help.

| Field | Value |
|-------|-------|
| Tester (another team, first name or "Team XX member" only) | |
| Task given | "Use this page to find something you need to know about the university." |
| What they did first | |
| **One thing that surprised them** | |
| Did they get stuck? Where? | |
| Follow-up (fix committed / issue link) | |

---

## Summary

- Lines ticked: __ / 27
- Lines fixed in this PR:
- Issues opened for remaining problems:
