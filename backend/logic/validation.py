from __future__ import annotations

import re

HANDLE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{2,31}$")
SEARCH_FRAGMENT_PATTERN = re.compile(r"^[a-z0-9_-]{1,32}$")


def normalize_handle(value: str) -> str:
    return value.strip().lower()


def validate_handle(value: str) -> str:
    handle = normalize_handle(value)
    if not HANDLE_PATTERN.fullmatch(handle):
        raise ValueError(
            "Handle must be 3-32 characters and contain lowercase letters, numbers, underscores, or hyphens."
        )
    return handle


def validate_search_fragment(value: str) -> str:
    fragment = normalize_handle(value)
    if not SEARCH_FRAGMENT_PATTERN.fullmatch(fragment):
        raise ValueError("Search query must be 1-32 handle characters.")
    return fragment


def validate_display_name(value: str) -> str:
    display_name = value.strip()
    if not 1 <= len(display_name) <= 80:
        raise ValueError("Display name must be 1-80 characters.")
    return display_name
