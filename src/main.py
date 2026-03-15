#!/usr/bin/env python3
"""Family Sports Calendar Aggregator - merge multiple iCal feeds into one."""

import logging
import sys
from pathlib import Path

# Add src to path so imports work when run as script or module
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml

from fetch import fetch_labeled_icals
from merge import merge_icals

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load config from YAML file."""
    path = Path(config_path)
    if not path.exists():
        logger.error("Config not found: %s (copy config.example.yaml to config.yaml)", config_path)
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _normalize_sources(config: dict) -> list[dict]:
    """Convert config to list of {url, label} sources."""
    sources = config.get("ical_sources") or []
    if sources:
        return [s if isinstance(s, dict) else {"url": s, "label": None} for s in sources]
    # Legacy: ical_urls
    urls = config.get("ical_urls") or []
    return [{"url": u, "label": None} for u in urls if u]


def main() -> None:
    config = load_config()
    sources = _normalize_sources(config)
    if not sources:
        logger.warning(
            "No ical_sources in config - create config.yaml from config.example.yaml"
        )

    ical_contents = fetch_labeled_icals(sources)
    if not ical_contents:
        logger.warning("No iCal content fetched - check your config and URLs")

    merged = merge_icals(ical_contents)

    output_path = Path("feed.ics")
    with open(output_path, "wb") as f:
        f.write(merged.to_ical())
    logger.info("Wrote %s", output_path)


if __name__ == "__main__":
    main()
