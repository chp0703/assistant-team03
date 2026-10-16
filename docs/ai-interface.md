# Future LLM interface

Related issue: #15.

## Scope and current behaviour

This document proposes the contract for a future AI service. The function and
types below are design examples; they are not implemented or importable yet.
This issue adds no LLM calls, provider SDK, credentials, or runtime dependencies.

Today, `assistant.reply(message)` in `src/assistant/rules.py` returns a plain
string using greetings and office records from `data/offices.csv`. The CLI and
planned UI keep using that existing interface until a separate integration task.

## Proposed Python interface

The future implementation is intended to live in `src/assistant/ai.py`.

```python
from collections.abc import Sequence
from typing import Literal, TypedDict


class Source(TypedDict):
    title: str
    reference: str


class ContextSource(Source):
    content: str


AIError = Literal[
    "invalid_input", "missing_context", "not_configured",
    "timeout", "provider_error", "invalid_response",
]


class AIResponse(TypedDict):
    answer: str
    sources: list[Source]
    status: Literal["ok", "fallback", "invalid_input"]
    error: AIError | None


def generate_answer(
    message: str,
    *,
    context: Sequence[ContextSource] = (),
    timeout_seconds: float = 10.0,
) -> AIResponse:
    ...
```

The service is synchronous and provider independent. Its configuration stays
inside the service; callers never pass API keys or a provider client. Callers
must treat `answer` as text and escape it before displaying it as HTML.

## Inputs

These limits are proposed application limits, not claims about any model's
context window.

| Input | Contract |
| --- | --- |
| `message` | Required string; strip leading/trailing whitespace, preserve case and internal text, then require 1-4,000 characters. |
| `context` | Up to 10 source records supplied by the backend, with at most 12,000 characters of `content` in total. Each record has a non-blank string `title`, `reference`, and `content`; references must be unique. An empty sequence is valid for general study explanations or work on text supplied in the message. |
| `timeout_seconds` | Finite number greater than 0 and at most 30 seconds; default 10. This is the total provider-call deadline, not a per-retry timeout. |

Reject wrong types, blank/oversized messages, malformed context, and invalid
timeouts before any provider call. Do not silently truncate input.

The backend owns retrieval and checks source relevance and currency before
calling the service. Institutional facts (rooms, hours, policies, deadlines)
require relevant supplied context. If evidence is absent or insufficient, return
`missing_context` and ask for an official source; model memory is not evidence.
General learning explanations may use model knowledge, but must not invent
institutional facts or citations. Treat user text and source content as data,
not instructions that can override service rules. Do not send secrets or
private student records to a provider.

## Outputs and sources

Every expected outcome returns all four `AIResponse` fields:

| Field | Contract |
| --- | --- |
| `answer` | Non-empty displayable text: either the generated answer or the safe message specified below. |
| `sources` | Only source metadata actually supporting the answer, copied from supplied context. Use `[]` when no source was used or the result is a fallback/input error. |
| `status` | `ok` for a validated generated answer, `fallback` for an unavailable/unsafe-to-answer request, or `invalid_input` for a validation failure. |
| `error` | `None` only for `ok`; otherwise one of the documented error codes. |

`title` and `reference` match the proposed citation shape in
[the UI source design](ui-sources.md). A reference can be a repository file plus
record name or a source URL. The service must reject unknown references rather
than showing model-invented citations. Sources are evidence, not a guarantee of
correctness; grounding validation still needs tests during implementation.

Illustrative successful response, assuming the backend supplied that note:

```python
{
    "answer": "Active recall means practising retrieval instead of rereading.",
    "sources": [
        {"title": "Study note", "reference": "user-provided:study-note-1"}
    ],
    "status": "ok",
    "error": None,
}
```

## Errors and safe messages

| Error | Status | User-facing answer / handling |
| --- | --- | --- |
| `invalid_input` | `invalid_input` | Blank message: `Please type a question.` Other validation failures: `The request is invalid. Please check the question, context, and timeout.` No provider call. |
| `missing_context` | `fallback` | `I don't have enough verified information to answer that. Please provide an official source.` No provider call when missing evidence is known in advance; discard an unsupported generated answer. |
| `not_configured` | `fallback` | `AI assistance is unavailable. Try asking about an office, or try again later.` Used when AI is disabled or provider configuration is absent. |
| `timeout` | `fallback` | Same unavailable message; stop waiting when the deadline expires. |
| `provider_error` | `fallback` | Same unavailable message for connection, authentication, rate-limit, or provider-service errors. |
| `invalid_response` | `fallback` | Same unavailable message for empty output, malformed output, or fabricated source references. |

All error responses have `sources: []`. Do not expose stack traces, provider
responses, configuration values, or credentials to users. Expected operational
failures become these response codes; programming bugs must remain visible to
developers instead of being silently swallowed. Logs may record the error code
and elapsed time, without raw prompts, source content, or credentials. Do not
retry automatically in the first implementation.

## Backend routing and fallback

The following flow is proposed for later integration, not current behaviour:

1. Validate the request. For blank input, keep `Please type a question.`
2. Check whether a deterministic rule fully answers the request. Greetings and
   direct office lookups use the existing rules/CSV and make no LLM call.
3. For supported study tasks that need explanation, synthesis, or rewriting,
   retrieve any required context and call `generate_answer` only if AI is enabled.
4. Display an `ok` answer with its supporting sources. For other results, display
   the documented safe message. A failed AI call must not recursively call AI.
5. Keep unsupported requests on the existing unknown-answer path:
   `I don't know that yet. Try asking about an office, e.g. 'training office'.`

The current `reply()` API has no explicit match flag. A later backend integration
must add or reuse an explicit routing decision, without comparing hard-coded
answer strings or assuming that any office-name substring fully answers a
complex request. This change does not alter `reply()` or the CLI.

## Checks required when implemented

- Direct greeting and office requests never call the provider.
- Valid generated output follows the schema and uses only supplied sources.
- Empty input and invalid limits fail before a provider call; context-free study
  explanations work, while unsupported institutional claims fail safely.
- Disabled/missing configuration, timeout, provider errors, and invalid output
  produce the documented codes/messages with no leaked data or retries.
- Existing rule/CLI tests still pass when AI is disabled or unavailable.

These are future implementation checks, not claims that an LLM integration has
been run or tested in this documentation issue.
