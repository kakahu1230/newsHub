"""Parser for Reuters world news."""
from __future__ import annotations

from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from ..common import make_story, soup_from_html


def _extract_timestamp(article: BeautifulSoup) -> datetime | None:
    time_tag = article.find("time")
    if not time_tag:
        return None
    datetime_attr = time_tag.get("datetime")
    if datetime_attr:
        try:
            return datetime.fromisoformat(datetime_attr.replace("Z", "+00:00"))
        except ValueError:
            return None
    text = time_tag.get_text(strip=True)
    if not text:
        return None
    try:
        return datetime.strptime(text, "%B %d, %Y")
    except ValueError:
        return None


def parse(html: str) -> List:
    soup = soup_from_html(html)
    stories = []
    for article in soup.select("article.story-card, article.story" ):
        title_tag = article.find("h2") or article.find("h3")
        if not title_tag:
            continue
        link = title_tag.find("a")
        if not link or not link.get("href"):
            continue
        title = link.get_text(strip=True)
        url = link.get("href")
        if url.startswith("/"):
            url = f"https://www.reuters.com{url}"
        summary_tag = article.find("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        published_at = _extract_timestamp(article)
        stories.append(
            make_story(
                source="reuters",
                title=title,
                url=url,
                summary=summary,
                published_at=published_at,
            )
        )
    return stories


__all__ = ["parse"]
