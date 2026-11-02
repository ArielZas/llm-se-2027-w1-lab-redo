# Unspecified decisions

The brief did not tell you everything. Every time you or your agent chose
something the brief did not specify, add a line here.

Examples of the kind of thing that counts: what fields the record has, what
happens to an issue with no clear type, how confident is confident enough,
what the output looks like when the model returns nothing usable.

You will need this list in W2, when we reconstruct the requirements this
build implicitly assumed. The comparison across the cohort is the lesson, so
write down what you actually decided, not what you think is the right answer.

---

-
-
-

## Exercise A decisions (2026-11-02)

- Accept one UTF-8 JSON object from a file or stdin; emit one JSON record on stdout using `uv run python -m triage.cli issue.json` or `uv run python -m triage.cli -`.
- Require repository, positive integer issue number, and nonempty title; allow a missing/null body and discard all other GitHub metadata.
- Return repository and issue number from validated input, never from the model, to preserve source identity.
- Extract issue_type, component, severity, has_reproduction_steps, summary, and uncertainty; defer queue assignment, deadlines, duplicate detection, and all routing.
- Use issue types bug/enhancement/documentation/question/meta/unknown, following the dataset taxonomy with an explicit abstention value.
- Keep component as a nullable repository-specific free-text name rather than inventing a shared cross-project taxonomy.
- Use severity low/medium/high/critical/unknown: cosmetic/documentation, limited defect, blocked core workflow, and claimed security exposure/data loss/widespread outage respectively; unknown covers unclear or inapplicable impact.
- Treat severity as an interpretation of reported claims, not verified security or operational impact; no severity gold labels exist in this snapshot.
- Represent reproduction as true/false/null and do not count empty template headings as actual steps.
- Include a short summary and qualitative uncertainty rather than an uncalibrated numerical confidence score.
- Bound repository/title/body to 200/2000/50000 characters and summary/uncertainty/component to 500/500/100; reject oversized input rather than silently truncate it.
- Use DSPy Predict with a typed Pydantic output and validate again at the model boundary; reject extra output fields and invalid types/enums.
- Load model configuration and credentials from environment/.env without a hard-coded provider or model default.
- Limit model output to 1000 tokens, request a 60-second provider timeout, disable LM caching and provider retries; DSPy adapter fallback may still make another request.
- Send only repository/title/body to the model, excluding labels, gold answers, identity number, and unrelated metadata.
- Treat issue text as untrusted data, encode it as JSON, provide no execution tools, and instruct the model to ignore embedded instructions; this mitigates but cannot guarantee resistance to prompt injection.
- On input/configuration/model failure, exit 1, print a generic diagnostic to stderr, and emit no successful record; omit raw provider exceptions to avoid leaking credentials or hostile text.
- Inject an extractor callable for offline contract tests; these tests verify plumbing/validation, not model accuracy or prompt-injection resistance.
- Provide tools/run_dev_triage.py solely for the lab's first-20-dev inspection, with JSONL records or exception class names in data/dev-triage-results.jsonl; never read the sealed test split.
- Defer the live twenty-issue run after the user explicitly requested skipping it; make no model-quality claims until it runs.
- Use a workspace-local uv cache because this sandbox cannot write the default user cache.

## CLI array selection (2026-11-02)

- Accept a top-level JSON array with an explicit zero-based integer `--index`, e.g. `uv run python -m triage.cli data/snapshot/dev.json --index 0`; do not implicitly select an element when the flag is omitted.
- Preserve single-object file/stdin input without `--index`; require an array when `--index` is supplied, including for stdin.
- Reject negative indexes, empty arrays, out-of-range indexes, and invalid selected issues before configuring or calling the model; use exit 1 with stderr and no stdout, while argparse rejects noninteger indexes with exit 2.
- Parse the complete JSON array but validate and triage only its selected element; unrelated elements need not satisfy the issue schema, and the command still emits exactly one record.
