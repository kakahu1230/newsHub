"""Parser for TechCrunch."""
from __future__ import annotations

from datetime import datetime
from typing import List

from ..common import make_story, soup_from_html


def parse(html: str) -> List:
    soup = soup_from_html(html)
    stories = []
    for article in soup.select("article.post-block"):
        title_tag = article.find("h2", class_="post-block__title")
        if not title_tag:
            continue
        link = title_tag.find("a")
        if not link or not link.get("href"):
            continue
        summary_tag = article.find("div", class_="post-block__content")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        time_tag = article.find("time")
        published_at = None
        if time_tag and time_tag.get("datetime"):
            try:
                published_at = datetime.fromisoformat(time_tag["datetime"].replace("Z", "+00:00"))
            except ValueError:
                published_at = None
        stories.append(
            make_story(
                source="techcrunch",
                title=link.get_text(strip=True),
                url=link.get("href"),
                summary=summary,
                published_at=published_at,
            )
        )
    return stories


__all__ = ["parse"]
