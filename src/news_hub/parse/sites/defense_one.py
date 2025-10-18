"""Parser for Defense One."""
from __future__ import annotations

from datetime import datetime
from typing import List

from ..common import make_story, soup_from_html


def parse(html: str) -> List:
    soup = soup_from_html(html)
    stories = []
    for article in soup.select("article.article-card"):
        title_tag = article.find("h3") or article.find("h2")
        if not title_tag:
            continue
        link = title_tag.find("a")
        if not link or not link.get("href"):
            continue
        url = link.get("href")
        if url.startswith("/"):
            url = f"https://www.defenseone.com{url}"
        summary_tag = article.find("p")
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
                source="defense-one",
                title=link.get_text(strip=True),
                url=url,
                summary=summary,
                published_at=published_at,
            )
        )
    return stories


__all__ = ["parse"]
