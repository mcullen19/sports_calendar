"""Parse, merge, and deduplicate calendar events."""

import hashlib
import logging
from datetime import datetime
from typing import Any

from icalendar import Calendar

logger = logging.getLogger(__name__)


def parse_ical(content: str) -> list[Any]:
    """Parse iCal content and return list of VEVENT components."""
    events = []
    try:
        cal = Calendar.from_ical(content)
        if cal:
            for component in cal.walk("VEVENT"):
                events.append(component)
    except Exception as e:
        logger.warning("Failed to parse iCal: %s", e)
    return events


def event_key(event: Any) -> str:
    """Generate a key for deduplication: dtstart + summary."""
    dt = event.get("dtstart")
    summary = event.get("summary", "")
    if hasattr(dt, "dt"):
        dt = dt.dt
    dt_str = dt.isoformat() if dt else ""
    summary_str = str(summary) if summary else ""
    raw = f"{dt_str}|{summary_str}".lower()
    return hashlib.md5(raw.encode()).hexdigest()


def events_are_similar(e1: Any, e2: Any) -> bool:
    """Check if two events are likely duplicates."""
    return event_key(e1) == event_key(e2)


def _prefix_summary(event: Any, label: str | None) -> None:
    """Prefix event SUMMARY with label if present. Modifies event in place."""
    if not label or not label.strip():
        return
    summary = event.get("summary")
    if summary:
        event["summary"] = f"{label.strip()}: {summary}"
    else:
        event["summary"] = label.strip()


def merge_icals(
    ical_contents: list[str] | list[tuple[str, str | None]],
) -> Calendar:
    """Parse all iCal contents, deduplicate, and return merged Calendar.
    ical_contents: list of str (no labels) or list of (content, label).
    """
    # Normalize to (content, label) tuples
    items: list[tuple[str, str | None]] = []
    for item in ical_contents:
        if isinstance(item, tuple):
            items.append(item)
        else:
            items.append((item, None))

    seen_keys: set[str] = set()
    merged = Calendar()
    merged.add("prodid", "-//Family Sports Calendar//Aggregator//EN")
    merged.add("version", "2.0")
    merged.add("x-wr-calname", "Family Sports Calendar")

    for content, label in items:
        events = parse_ical(content)
        for event in events:
            key = event_key(event)  # Dedup before label (same event = same key)
            if key not in seen_keys:
                seen_keys.add(key)
                _prefix_summary(event, label)
                merged.add_component(event)

    return merged


def gamesheets_to_ical(api_data: dict) -> list[Any]:
    """Convert Gamesheets API response to icalendar VEVENTs. Stub."""
    # TODO: Implement when API structure known
    return []
