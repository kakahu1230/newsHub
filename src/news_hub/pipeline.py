"""NewsHub ETL pipeline utilities."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, Iterable, List

from .categorize.classifier import classify
from .config import PROCESSED_DIR, SourceConfig, get_sources
from .dedup.similarity import merge_stories
from .fetch.client import FetchResult, HttpFetcher
from .models import RawStory, Story


def fetch_all(fetcher: HttpFetcher, force_refresh: bool = False) -> Dict[str, FetchResult]:
    """Fetch raw HTML for all sources."""
    results = {}
    for source in get_sources().values():
        results[source.slug] = fetcher.fetch(source, force_refresh=force_refresh)
    return results


def parse_all(raw_html: Dict[str, FetchResult]) -> List[RawStory]:
    """Parse HTML from each source into raw stories."""
    stories: List[RawStory] = []
    sources = get_sources()
    for slug, fetch_result in raw_html.items():
        parser = sources[slug].parser
        stories.extend(parser(fetch_result.html))
    return stories


def process(stories: Iterable[RawStory]) -> List[Story]:
    """Deduplicate and classify stories."""
    deduped = merge_stories(stories)
    categorized = classify(deduped)
    return categorized


def export(stories: Iterable[Story]) -> None:
    """Persist processed stories to disk."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "id": story.id,
            "title": story.title,
            "url": story.url,
            "summary": story.summary,
            "published_at": story.published_at.isoformat() if story.published_at else None,
            "sources": story.sources,
            "categories": story.categories,
        }
        for story in stories
    ]
    output_path = PROCESSED_DIR / "stories.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


__all__ = ["fetch_all", "parse_all", "process", "export"]
