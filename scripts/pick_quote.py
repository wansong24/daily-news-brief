#!/usr/bin/env python3
import argparse
from pathlib import Path
import re
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / 'references' / 'quote-pool.md'


def load_quotes(path: Path):
    text = path.read_text(encoding='utf-8')
    quotes = []
    for line in text.splitlines():
        m = re.match(r'\d+\. \*\*“(.+?)”\*\* —— (.+)$', line.strip())
        if m:
            quotes.append((m.group(1), m.group(2)))
    return quotes


def load_used(path: Optional[Path]):
    if not path or not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding='utf-8').splitlines() if line.strip()}


def main():
    ap = argparse.ArgumentParser(description='Pick a non-recent Chinese quote for the daily news brief.')
    ap.add_argument('--used-file', help='Optional text file containing previously used quote texts, one per line')
    args = ap.parse_args()

    quotes = load_quotes(POOL)
    used = load_used(Path(args.used_file) if args.used_file else None)

    for text, author in quotes:
        if text not in used:
            print(f'“{text}”\n—— {author}')
            return

    if quotes:
        text, author = quotes[0]
        print(f'“{text}”\n—— {author}')


if __name__ == '__main__':
    main()
