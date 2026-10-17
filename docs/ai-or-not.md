# Which questions should use AI?

Related issue: #16.

## Decision rule and current scope

Use deterministic rules or structured data when they can fully answer the
question. Consider an LLM for supported study tasks that need explanation,
synthesis, or rewriting. Here, "needs AI" means that generative language handling
is appropriate for the proposed assistant; it does not mean a human or another
software approach could never solve the task.

The current application is rule based: `assistant.reply()` handles greetings,
empty input, and full office-name matches using `data/offices.csv`. There is no
LLM integration. All AI examples below describe future capabilities. The CSV is
development/test data, not a verified live university directory.

## 10 questions suited to AI

Assume the user supplies any notes, passages, exercises, or constraints named in
the question. These are input examples, not claims about files already in the
repository. Each row has one reason for choosing the AI route.

| # | Example question | Use AI? | One-line reason |
| --- | --- | --- | --- |
| 1 | Can you summarise these lecture notes into five key ideas? | Yes, when implemented | Selecting and condensing ideas from free-form text requires synthesis beyond office lookup rules. |
| 2 | Can you explain recursion to a beginner using a simple analogy? | Yes, when implemented | Adapting an explanation and analogy to a learner benefits from generated language. |
| 3 | How do recursion and iteration compare for the problem described here? | Yes, when implemented | Comparing approaches against a supplied problem requires contextual explanation. |
| 4 | Can you suggest a study plan from these topics, available hours, and exam date? | Yes, when implemented | Turning supplied constraints into an explained learning plan benefits from contextual generation, with dates and time totals checked deterministically. |
| 5 | What is missing or incorrect in my explanation of overfitting below? | Yes, when implemented | Giving targeted feedback requires interpreting the learner's free-form explanation. |
| 6 | Can you write five practice questions with answer explanations from these notes? | Yes, when implemented | Creating varied questions grounded in supplied material requires content generation. |
| 7 | Can you rewrite this technical paragraph in simpler language without changing its meaning? | Yes, when implemented | Simplification requires a semantic rewrite rather than an exact data lookup. |
| 8 | Can you translate this short study passage into Vietnamese while keeping the supplied technical terms? | Yes, when implemented | Context-sensitive translation must preserve meaning and a supplied terminology list. |
| 9 | Can you give me a hint for this exercise without revealing the final answer? | Yes, when implemented | A useful partial explanation must adapt to the exercise and the learner's progress. |
| 10 | Where do these two sets of study notes agree or contradict each other? | Yes, when implemented | Finding and explaining relationships across free-form sources requires synthesis. |

## 10 questions that do not need AI

Rows 1-6 already match full office names in the current CSV and can return the
stored room and hours. Rows 7-10 propose small deterministic extensions; the
current `reply()` does not yet implement listing, counting, capability help, or
an explicit yes/no existence check. None of those extensions needs an LLM.

| # | Example question | Use AI? | One-line reason |
| --- | --- | --- | --- |
| 1 | Where is the Training Office? | No | An exact lookup of the Training Office row supplies its stored room. |
| 2 | Where is Student Affairs? | No | An exact lookup of the Student Affairs row supplies its stored room. |
| 3 | Where is the Library? | No | An exact lookup of the Library row supplies its stored room. |
| 4 | Where is the IT Helpdesk? | No | An exact lookup of the IT Helpdesk row supplies its stored room. |
| 5 | What are the Training Office opening hours? | No | The Training Office row already contains the hours string to display. |
| 6 | What are the Library opening hours? | No | The Library row already contains the hours string to display. |
| 7 | Which offices are listed in the directory? | No | Listing the CSV `name` column is a deterministic operation. |
| 8 | How many offices are in the directory? | No | Counting valid office records is deterministic and requires no generated answer. |
| 9 | What can this assistant answer? | No | A fixed help response can describe the capabilities that are actually enabled. |
| 10 | Is a Sports Office listed in this directory? | No | An exact name-membership check can report whether a record exists without inferring real-world availability. |

## Routing boundaries

- Judge the requested task, not just a keyword: a question mentioning "Library"
  may ask for a study plan rather than its room or opening hours.
- Missing institutional information is a retrieval problem. For an unpublished
  deadline, policy, or room, ask for an official source or say it is unknown;
  an LLM must not fill the gap with a guess.
- Keep calculations, counting, sorting, and date checks deterministic even when
  AI helps phrase a longer response. Exact facts come from supplied evidence.
- Only display citations for sources actually used. A general explanation may
  have no citation; do not fabricate a reference to make it look verified.
- If AI is disabled or fails, retain the existing rule/CSV answers and give a
  clear unavailable/unknown response for requests those rules cannot answer.

These tables define routing examples, not a benchmark of model accuracy or a
claim that the proposed features have been implemented.
