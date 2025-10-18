"""CLI script to refresh NewsHub data."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime

from news_hub.fetch.client import HttpFetcher
from news_hub.pipeline import export, fetch_all, parse_all, process


def serialize_story(story) -> dict:
    payload = asdict(story)
    if isinstance(payload.get("published_at"), datetime):
        payload["published_at"] = payload["published_at"].isoformat()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh NewsHub data cache")
    parser.add_argument("--force", action="store_true", help="Force refetch even if cache exists")
    parser.add_argument(
        "--print", action="store_true", dest="print_output", help="Print processed stories to stdout"
    )
    args = parser.parse_args()

    fetcher = HttpFetcher()
    raw = fetch_all(fetcher, force_refresh=args.force)
    stories = parse_all(raw)
    processed = process(stories)
    export(processed)

    if args.print_output:
        print(json.dumps([serialize_story(story) for story in processed], indent=2))


if __name__ == "__main__":
    main()
