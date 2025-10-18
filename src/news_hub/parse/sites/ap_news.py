"""Parser for AP News."""
from __future__ import annotations

from datetime import datetime
from typing import List

from ..common import make_story, soup_from_html


MONTH_MAP = {
    month: index
    for index, month in enumerate(
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        start=1,
    )
}


def _parse_timestamp(text: str) -> datetime | None:
    parts = text.replace(",", "").split()
    if len(parts) < 3:
        return None
    month, day, year = parts[:3]
    try:
        return datetime(int(year), MONTH_MAP[month], int(day))
    except (ValueError, KeyError):
        return None


def parse(html: str) -> List:
    soup = soup_from_html(html)
    stories = []
    for card in soup.select("div.PagePromo-card"):
        title_tag = card.find("h3") or card.find("h2")
        if not title_tag:
            continue
        link = title_tag.find("a")
        if not link or not link.get("href"):
            continue
        url = link.get("href")
        if url.startswith("/"):
            url = f"https://apnews.com{url}"
        summary_tag = card.find("div", class_="PagePromo-description") or card.find("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        time_tag = card.find("span", class_="Timestamp")
        published_at = _parse_timestamp(time_tag.get_text(strip=True)) if time_tag else None
        stories.append(
            make_story(
                source="ap",
                title=link.get_text(strip=True),
                url=url,
                summary=summary,
                published_at=published_at,
            )
        )
    return stories


__all__ = ["parse"]
