from __future__ import annotations

import re

INITIAL_BALANCE_PAISA = 10_000_000

# Strict pattern: optional leading digits, mandatory decimal with exactly 2 digits.
# Rejects: scientific notation, grouping separators, blank, non-string.
_BDT_PATTERN = re.compile(r"^[0-9]+\.\d{2}$")


def format_paisa(amount_paisa: int) -> str:
    if amount_paisa < 0:
        raise ValueError("amount_paisa must be non-negative")
    taka, paisa = divmod(amount_paisa, 100)
    return f"{taka}.{paisa:02d}"


def parse_paisa(value: str | object) -> int:
    """Parse a decimal BDT string into integer paisa without float.

    Accepts only strict decimal strings like "2500.00".
    Raises ValueError for zero, negative, malformed, blank,
    excess precision, scientific notation, or non-string input.
    """
    if not isinstance(value, str):
        raise ValueError("Amount must be a string.")
    raw = value.strip()
    if raw == "":
        raise ValueError("Amount must not be blank.")
    if not _BDT_PATTERN.fullmatch(raw):
        raise ValueError("Amount must be a valid decimal string with exactly two decimal places.")

    parts = raw.split(".")
    taka_str = parts[0]
    paisa_str = parts[1]

    taka = int(taka_str)
    paisa = int(paisa_str)
    total = taka * 100 + paisa

    if total <= 0:
        raise ValueError("Amount must be greater than zero.")
    return total
