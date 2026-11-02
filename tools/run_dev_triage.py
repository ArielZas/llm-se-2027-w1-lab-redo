"""Exercise A inspection run: first twenty dev issues, never the sealed split."""
import json
from pathlib import Path
from triage.extract import configured_extractor, triage
from triage.models import Issue

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    issues = [Issue.model_validate(item) for item in json.loads(
        (root / "data/snapshot/dev.json").read_text(encoding="utf-8"))[:20]]
    extractor = configured_extractor()
    output = root / "data/dev-triage-results.jsonl"
    with output.open("w", encoding="utf-8") as stream:
        for issue in issues:
            try:
                record = triage(issue, extractor)
                result = record.model_dump_json()
            except Exception as exc:
                result = json.dumps({"repo": issue.repo, "number": issue.number,
                                     "error": type(exc).__name__})
            stream.write(result + "\n")
            stream.flush()
            print(result, flush=True)

if __name__ == "__main__":
    main()
