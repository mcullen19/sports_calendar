"""Fetch iCal feeds and optional Gamesheets API data."""

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

TIMEOUT = 30


def fetch_ical(url: str) -> Optional[str]:
    """Fetch iCal content from a URL. Returns None on failure."""
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        logger.warning("Failed to fetch %s: %s", url[:50], e)
        return None


def fetch_all_icals(urls: list[str]) -> list[tuple[str, str | None]]:
    """Fetch all iCal feeds. Returns list of (content, label). Skips failed fetches."""
    return fetch_labeled_icals([{"url": u, "label": None} for u in urls])


def fetch_labeled_icals(
    sources: list[dict],
) -> list[tuple[str, str | None]]:
    """Fetch iCal feeds from sources with optional labels.
    Each source: {url: str, label: str | None}
    Returns list of (content, label). Skips failed fetches.
    """
    results = []
    for src in sources:
        url = src.get("url") if isinstance(src, dict) else None
        label = src.get("label") if isinstance(src, dict) else None
        if not url or not str(url).strip():
            continue
        content = fetch_ical(str(url).strip())
        if content:
            results.append((content, label))
    return results


def fetch_gamesheets(api_url: str, api_key: str) -> Optional[dict]:
    """Fetch schedule from Gamesheets API. Stub - returns None until implemented."""
    # TODO: Implement when API docs/credentials available
    logger.info("Gamesheets API not yet implemented")
    return None
