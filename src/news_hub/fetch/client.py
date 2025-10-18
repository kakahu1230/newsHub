"""HTTP fetching utilities with caching and throttling."""
from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

from ..config import RAW_CACHE_DIR, SourceConfig


USER_AGENT = "NewsHubBot/1.0 (+https://example.com/newshub)"


@dataclass
class FetchResult:
    """Result of fetching a single URL."""

    html: str
    from_cache: bool
    cache_path: Path


class FetchError(RuntimeError):
    """Raised when fetching a URL fails."""


class HttpFetcher:
    """Fetch HTML content with optional caching and throttling."""

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def fetch(self, source: SourceConfig, force_refresh: bool = False) -> FetchResult:
        """Fetch HTML for a source, using cached results when possible."""
        RAW_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        latest_cache = self._latest_cache(source)

        if latest_cache and not force_refresh:
            return FetchResult(
                html=latest_cache.read_text(encoding="utf-8"),
                from_cache=True,
                cache_path=latest_cache,
            )

        time.sleep(source.throttle_seconds)
        try:
            response = self.session.get(source.url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            if latest_cache:
                return FetchResult(
                    html=latest_cache.read_text(encoding="utf-8"),
                    from_cache=True,
                    cache_path=latest_cache,
                )
            raise FetchError(f"Failed to fetch {source.url}: {exc}") from exc

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        cache_path = RAW_CACHE_DIR / f"{source.slug}-{timestamp}.html"
        cache_path.write_text(response.text, encoding="utf-8")
        return FetchResult(html=response.text, from_cache=False, cache_path=cache_path)

    def _latest_cache(self, source: SourceConfig) -> Optional[Path]:
        candidates = sorted(RAW_CACHE_DIR.glob(f"{source.slug}-*.html"))
        return candidates[-1] if candidates else None


__all__ = ["HttpFetcher", "FetchError", "FetchResult"]
