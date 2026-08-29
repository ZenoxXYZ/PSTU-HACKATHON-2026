from __future__ import annotations

INITIAL_BALANCE_PAISA = 10_000_000


def format_paisa(amount_paisa: int) -> str:
    if amount_paisa < 0:
        raise ValueError("amount_paisa must be non-negative")
    taka, paisa = divmod(amount_paisa, 100)
    return f"{taka}.{paisa:02d}"
