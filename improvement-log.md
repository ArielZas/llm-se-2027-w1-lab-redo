# Improvement log

Every time the agent gets something wrong, it goes here. Not the fix — the
*failure*, classified.

This file runs for the whole semester. In W12 you will use it to show what
changed about how you work. That only works if it was written as things
happened, so write entries the day they occur. An improvement log
reconstructed from memory in week eleven is a creative writing exercise.

## The taxonomy

Classify every entry as exactly one of:

| Class | Meaning | Where the fix usually belongs |
|---|---|---|
| `capability` | the model could not do this | change the task, or the model |
| `context` | it could have, but did not know something | what the agent is given to read |
| `tool` | it lacked a way to act or to check | tooling |
| `spec` | the request was ambiguous and it guessed | the specification |
| `concept` | it used the wrong idea or the wrong name | the domain model |
| `bug` | ordinary defect, nothing AI-specific | the code |

The class matters more than the fix. Choosing between `context` and `spec`
forces you to say whether the agent lacked information or you did — and those
have different remedies.

---

## Entries

### E1

- **Date**:
- **What happened**:
- **Class**:
- **Evidence** (session log timestamp, commit, or file:line):
- **What I did about it**:
- **Did it work?**:

---

### E2

- **Date**:
- **What happened**:
- **Class**:
- **Evidence**:
- **What I did about it**:
- **Did it work?**:

---

### E3

- **Date**:
- **What happened**:
- **Class**:
- **Evidence**:
- **What I did about it**:
- **Did it work?**:

## Exercise A observed agent failures (2026-11-02)

### A1
- **What happened**: The agent assumed uv could use its default user cache in this sandbox.
- **Class**: tool
- **Evidence**: First uv invocation failed opening AppData/Local/uv/cache/.lock with access denied.
- **What I did about it**: Used `uv --cache-dir .uv-cache run ...`.
- **Did it work?**: Yes; pytest and pyright ran.

### A2
- **What happened**: The agent supplied a patch deleting and adding extract.py in the same patch; the patch tool rejected it before applying any edits.
- **Class**: tool
- **Evidence**: apply_patch reported multiple operations targeting src/triage/extract.py.
- **What I did about it**: Wrote the files with PowerShell and verified them with tests and type checking.
- **Did it work?**: Yes.

### A3
- **What happened**: The agent assumed the lab request was sufficient authorization for a network-enabled twenty-issue provider run; automatic review required specific payload/destination approval.
- **Class**: context
- **Evidence**: The escalation was rejected because it sends twenty issue records to an external model provider with configured credentials.
- **What I did about it**: Asked explicitly; the user chose to skip the live run. Recorded the incomplete review instead of inventing findings.
- **Did it work?**: The user's preference is respected; live quality evaluation remains deferred.

### A4
- **What happened**: The agent implemented a CLI that accepts a single-issue JSON file instead of allowing selection by index from the development dataset. The original requirement was not specific enough.
- **Class**: communication
- **Evidence**: Running `uv run python -m triage.cli --help` showed only a positional `issue` argument, with no `--index` option.
- **What I did about it**: Clarified the requirement and asked the agent to support selecting an issue by zero-based index from a JSON dataset while preserving single-issue input.
- **Did it work?**: Pending verification after implementing and testing the updated CLI.