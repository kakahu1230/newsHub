"""Data models used throughout NewsHub."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class RawStory:
    """Story as parsed from an individual news source."""

    source: str
    title: str
    url: str
    summary: str
    published_at: Optional[datetime]
    raw_text: str = ""


@dataclass
class Story:
    """Normalized story with deduplication and categorization."""

    id: str
    title: str
    url: str
    summary: str
    published_at: Optional[datetime]
    sources: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)


__all__ = ["RawStory", "Story"]
