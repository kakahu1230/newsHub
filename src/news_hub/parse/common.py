"""Common utilities for parsing news sources."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from ..models import RawStory


def soup_from_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def make_story(
    source: str,
    title: str,
    url: str,
    summary: str,
    published_at: Optional[datetime],
    raw_text: str = "",
) -> RawStory:
    return RawStory(
        source=source,
        title=title.strip(),
        url=url.strip(),
        summary=summary.strip(),
        published_at=published_at,
        raw_text=raw_text.strip(),
    )


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


__all__ = ["soup_from_html", "make_story", "parse_iso_datetime"]
