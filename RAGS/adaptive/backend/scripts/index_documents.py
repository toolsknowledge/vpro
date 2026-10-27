"""Index the sample documents from the command line (requires OPENAI_API_KEY).

Usage (from the project root):
    .venv/bin/python backend/scripts/index_documents.py            # incremental
    .venv/bin/python backend/scripts/index_documents.py --reindex  # full refresh
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dependencies import get_indexing_service  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--reindex", action="store_true", help="re-embed every file and remove stale chunks")
    args = parser.parse_args()

    result = get_indexing_service().run("reindex" if args.reindex else "index")
    print(f"[{result.status}] {result.message}")
    print(
        f"  discovered={result.discovered_files} processed={result.processed_files} "
        f"unchanged={result.unchanged_files} chunks_created={result.chunks_created} "
        f"chunks_removed={result.chunks_removed}"
    )
    for issue in result.skipped_files:
        print(f"  skipped  {issue.filename}: {issue.reason}")
    for issue in result.errors:
        print(f"  error    {issue.filename}: {issue.reason}")
    return 0 if result.status in ("success", "no_documents") else 1


if __name__ == "__main__":
    raise SystemExit(main())
