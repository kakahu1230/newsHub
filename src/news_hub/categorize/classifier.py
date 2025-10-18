"""Story categorization based on keywords and source metadata."""
from __future__ import annotations

from typing import Dict, Iterable, List

from ..models import Story


CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "finance": ["market", "stocks", "economy", "financial", "bank", "inflation"],
    "politics": ["election", "parliament", "senate", "white house", "policy", "government"],
    "military": ["defense", "military", "army", "navy", "air force", "security"],
    "technology": ["technology", "startup", "software", "ai", "cyber", "tech"],
}

SOURCE_DEFAULTS: Dict[str, List[str]] = {
    "defense-one": ["military"],
    "techcrunch": ["technology"],
}


def classify(stories: Iterable[Story]) -> List[Story]:
    """Assign categories based on keywords and source defaults."""
    results: List[Story] = []
    for story in stories:
        categories = set()
        for source in story.sources:
            categories.update(SOURCE_DEFAULTS.get(source, []))
        text = f"{story.title} {story.summary}".lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                categories.add(category)
        story.categories = sorted(categories)
        results.append(story)
    return results


__all__ = ["classify"]
