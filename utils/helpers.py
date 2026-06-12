import re


def extract_order_id(text: str) -> str | None:
    """Extract the first numeric sequence from a string (used as an order ID)."""
    match = re.search(r"\d+", text)
    return match.group() if match else None


def truncate(text: str, max_chars: int = 200) -> str:
    """Truncate a string for safe logging."""
    return text[:max_chars] + "..." if len(text) > max_chars else text
