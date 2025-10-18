"""Utilities for detecting similar stories across sources."""
from __future__ import annotations

import hashlib
import re
from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, Iterable, List, Set

from ..models import RawStory, Story


def _normalize(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(cleaned.split())


def _story_id(text: str) -> str:
    return hashlib.sha1(_normalize(text).encode("utf-8")).hexdigest()


def merge_stories(stories: Iterable[RawStory], similarity_threshold: float = 0.82) -> List[Story]:
    """Merge similar stories using fuzzy title matching."""
    merged: Dict[str, Story] = {}
    seen_sources: Dict[str, Set[str]] = {}
    for raw in stories:
        if not raw.title:
            continue
        normalized = _normalize(raw.title)
        match_id = None
        match_ratio = 0.0
        for story_id, story in merged.items():
            ratio = SequenceMatcher(None, normalized, _normalize(story.title)).ratio()
            if ratio > similarity_threshold and ratio > match_ratio:
                match_id = story_id
                match_ratio = ratio
        if match_id is None:
            story_id = _story_id(raw.title)
            merged[story_id] = Story(
                id=story_id,
                title=raw.title,
                url=raw.url,
                summary=raw.summary,
                published_at=raw.published_at,
                sources=[raw.source],
                categories=[],
            )
            seen_sources[story_id] = {raw.source}
        else:
            story = merged[match_id]
            sources = seen_sources[match_id]
            sources.add(raw.source)
            story.sources = sorted(sources)
            if raw.published_at and (
                story.published_at is None or raw.published_at < story.published_at
            ):
                story.published_at = raw.published_at
            if raw.summary and len(raw.summary) > len(story.summary):
                story.summary = raw.summary
    return sorted(
        merged.values(),
        key=lambda s: s.published_at or datetime.min,
        reverse=True,
    )


__all__ = ["merge_stories"]
