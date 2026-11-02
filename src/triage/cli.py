"""Usage: uv run python -m triage.cli issue.json (or - for stdin)."""
import argparse
from pathlib import Path
import sys
from pydantic import ValidationError
from triage.extract import configured_extractor, triage
from triage.models import Issue

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read one issue JSON and emit one triage JSON.")
    parser.add_argument("issue", help="UTF-8 JSON file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.issue == "-" else Path(args.issue).read_text(encoding="utf-8")
        issue = Issue.model_validate_json(raw)
        record = triage(issue, configured_extractor())
    except (OSError, ValidationError, ValueError):
        print("Invalid input/configuration or model record; check JSON schema and LLM_MODEL.", file=sys.stderr)
        return 1
    except Exception:
        # Provider exceptions may contain credentials or untrusted issue text.
        print("Model call failed; check provider credentials, quota and connectivity.", file=sys.stderr)
        return 1
    print(record.model_dump_json())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
