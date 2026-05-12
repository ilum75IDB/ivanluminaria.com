#!/usr/bin/env python3
"""
Shorten over-160-char descriptions in glossary mini-pages (issue #89).
Smart truncation: prefers sentence boundary (.), then semicolon (;),
then em-dash (—), then comma (,). Falls back to hard cut + ellipsis only
as last resort.

Strategy:
- target_max = 160 chars
- preferred_min = 100 chars (don't cut too short)
- Look for the latest sentence boundary between preferred_min and target_max
- If no good boundary, look between (preferred_min - 20) and target_max
- If still nothing, hard-cut at target_max-1 + ellipsis
"""
import re
from pathlib import Path
import sys

TARGET_MAX = 160
PREFERRED_MIN = 100
ABSOLUTE_MIN = 80


def smart_shorten(text: str, max_len: int = TARGET_MAX) -> tuple[str, str]:
    """
    Shorten a description to at most max_len chars, preferring sentence boundaries.
    Returns (shortened_text, strategy_used).
    """
    if len(text) <= max_len:
        return text, "unchanged"

    # Helper: find the latest occurrence of any of the given delimiters
    # in text[start:end+1] (returns index of delimiter char in text, or -1)
    def find_last_delim_in_range(s: str, start: int, end: int, delims: list[str]) -> int:
        best = -1
        for d in delims:
            # Search in window
            i = s.rfind(d, start, end + 1)
            if i > best:
                best = i
        return best

    # Strategy 1: sentence boundary (". " or just ".") between PREFERRED_MIN and max_len-1
    # Note: we look for ". " (period followed by space) preferring complete sentences
    idx = find_last_delim_in_range(text, PREFERRED_MIN, max_len - 1, [". "])
    if idx > 0:
        # Cut INCLUDING the period (so the description ends with a period)
        return text[: idx + 1].rstrip(), "sentence"

    # Strategy 2: em-dash or "—" between PREFERRED_MIN and max_len-1
    # Em-dash is multi-byte in some encodings but in Python str it's a single char
    idx = find_last_delim_in_range(text, PREFERRED_MIN, max_len - 1, [" — ", " - "])
    if idx > 0:
        return text[:idx].rstrip(), "em-dash"

    # Strategy 3: semicolon or colon
    idx = find_last_delim_in_range(text, PREFERRED_MIN, max_len - 1, ["; ", ": "])
    if idx > 0:
        return text[: idx + 1].rstrip(), "semicolon"

    # Strategy 4: comma between PREFERRED_MIN and max_len - 3 (need room for ellipsis)
    idx = find_last_delim_in_range(text, PREFERRED_MIN, max_len - 4, [", "])
    if idx > 0:
        return text[:idx].rstrip() + "...", "comma+ellipsis"

    # Strategy 5: fall back, look further back from ABSOLUTE_MIN for ANY boundary
    idx = find_last_delim_in_range(
        text, ABSOLUTE_MIN, max_len - 4, [". ", " — ", " - ", "; ", ": ", ", "]
    )
    if idx > 0:
        # Determine the actual char to decide if we keep it or not
        ch = text[idx]
        if ch == ".":
            return text[: idx + 1].rstrip(), "sentence-loose"
        elif ch in ";:":
            return text[: idx + 1].rstrip(), "semicolon-loose"
        else:
            return text[:idx].rstrip() + "...", "soft-loose"

    # Strategy 6 (last resort): hard cut + ellipsis at word boundary
    # Find last space before max_len - 3
    idx = text.rfind(" ", 0, max_len - 3)
    if idx > 0:
        return text[:idx].rstrip() + "...", "word-hard"

    # Strategy 7: absolutely last resort, hard truncate
    return text[: max_len - 3] + "...", "hard"


def process_file(path: Path) -> tuple[str, str, str, int, int]:
    """Returns (status, strategy, path_str, old_len, new_len)."""
    text = path.read_text(encoding="utf-8")

    # Match the description line, preserving quotes
    m = re.search(r'^description:\s*"([^"]*)"\s*$', text, re.MULTILINE)
    if not m:
        return "no-desc", "", str(path), 0, 0

    old_desc = m.group(1)
    old_len = len(old_desc)

    if old_len <= TARGET_MAX:
        return "unchanged", "ok", str(path), old_len, old_len

    new_desc, strategy = smart_shorten(old_desc, TARGET_MAX)
    new_len = len(new_desc)

    if new_desc == old_desc:
        return "no-change", strategy, str(path), old_len, new_len

    # Backup
    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")

    # Replace in the file
    escaped = new_desc.replace('\\', '\\\\').replace('"', '\\"')
    new_text = re.sub(
        r'^description:\s*"[^"]*"\s*$',
        f'description: "{escaped}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(new_text, encoding="utf-8")

    return "shortened", strategy, str(path), old_len, new_len


def main():
    base = Path("content/glossary")
    files = sorted(base.rglob("index.*.md"))

    stats = {
        "unchanged": 0,
        "shortened": 0,
        "no-desc": 0,
        "no-change": 0,
    }
    strategy_counts = {}
    examples_per_strategy = {}

    for f in files:
        status, strategy, path_str, old_len, new_len = process_file(f)
        stats[status] = stats.get(status, 0) + 1
        if status == "shortened":
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            if strategy not in examples_per_strategy:
                examples_per_strategy[strategy] = []
            if len(examples_per_strategy[strategy]) < 2:
                examples_per_strategy[strategy].append(
                    (path_str, old_len, new_len)
                )

    print(f"\n=== Summary ===")
    print(f"Total files scanned: {len(files)}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"\n=== Strategies used for shortening ===")
    for strat, count in sorted(strategy_counts.items(), key=lambda x: -x[1]):
        print(f"  {strat}: {count}")
        for path_str, ol, nl in examples_per_strategy.get(strat, []):
            print(f"    e.g. {path_str} ({ol}ch -> {nl}ch)")

    sys.exit(0)


if __name__ == "__main__":
    main()
