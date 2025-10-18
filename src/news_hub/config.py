"""Configuration for NewsHub data pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List

from .models import RawStory


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_CACHE_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


@dataclass(frozen=True)
class SourceConfig:
    """Definition of a news source."""

    slug: str
    name: str
    url: str
    parser: Callable[[str], List[RawStory]]
    throttle_seconds: float = 1.0


def get_sources() -> Dict[str, SourceConfig]:
    """Return mapping of source slug to configuration."""
    from .parse.sites import ap_news, defense_one, reuters, techcrunch

    return {
        cfg.slug: cfg
        for cfg in [
            SourceConfig(
                slug="reuters",
                name="Reuters Top News",
                url="https://www.reuters.com/world/",
                parser=reuters.parse,
                throttle_seconds=1.5,
            ),
            SourceConfig(
                slug="ap",
                name="AP News",
                url="https://apnews.com/hub/ap-top-news",
                parser=ap_news.parse,
                throttle_seconds=1.5,
            ),
            SourceConfig(
                slug="defense-one",
                name="Defense One",
                url="https://www.defenseone.com/",
                parser=defense_one.parse,
                throttle_seconds=2.0,
            ),
            SourceConfig(
                slug="techcrunch",
                name="TechCrunch",
                url="https://techcrunch.com/",
                parser=techcrunch.parse,
                throttle_seconds=1.5,
            ),
        ]
    }


__all__ = ["SourceConfig", "get_sources", "RAW_CACHE_DIR", "PROCESSED_DIR"]
