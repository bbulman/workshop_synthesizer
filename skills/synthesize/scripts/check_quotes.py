#!/usr/bin/env python3
"""The quote gate for /synthesize.

Checks that every evidence quote in a research-synthesizer report appears
verbatim in the source notes.

Usage:
  python3 check_quotes.py REPORT.md SOURCE_DIR   check a report
  python3 check_quotes.py --selftest             run the built-in cases

What counts as a match:
  - curly and straight quotes, apostrophes and dashes are treated as equal
  - whitespace and line breaks are collapsed, so a quote can wrap in the source
  - [...] elisions split a quote into fragments that must all appear, in order,
    in ONE source file (so an elision can't stitch two sources together)
  - case-sensitive: a quote that changes "Never" to "never" fails

Quotes tagged B.. or F.. (photos and FigJam boards) are skipped: they have no
text file to check against. The agent checks those against its transcription.

Exit code: 0 all found, 1 something not found, 2 usage error.
"""
import re
import sys
import tempfile
from pathlib import Path

QUOTE_LINE = re.compile(r'^\s*>\s*["“](.+?)["”]\s+[—–-]\s+([^\s,]+)', re.M)
TEXT_EXTS = {".md", ".txt", ".vtt", ".srt", ".csv", ".json", ".tsv"}
VISUAL_TAG = re.compile(r"^[BF]\d")
ELISION = re.compile(r"\[\s*(?:\.\.\.|…)\s*\]")


def norm(s: str) -> str:
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("—", "-"), ("–", "-"), ("…", "...")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def found_in(fragments, body):
    pos = 0
    for f in fragments:
        i = body.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return True


def check(report_text: str, sources: dict):
    """Return (checked, skipped, missing) where missing is a list of (tag, quote)."""
    checked, skipped, missing = 0, 0, []
    bodies = [norm(b) for b in sources.values()]
    for text, tag in QUOTE_LINE.findall(report_text):
        if VISUAL_TAG.match(tag):
            skipped += 1
            continue
        checked += 1
        frags = [norm(f) for f in ELISION.split(text) if f.strip()]
        if not frags or not any(found_in(frags, b) for b in bodies):
            missing.append((tag, text))
    return checked, skipped, missing


def load_sources(src: Path) -> dict:
    files = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
    return {p: p.read_text(errors="ignore") for p in files if p.suffix.lower() in TEXT_EXTS}


def selftest() -> int:
    src = {
        "p01.md": "Jane: Honestly the integrations step\nwas the worst part. I didn’t want to connect Slack yet.\nLater I liked the dashboard.",
        "p02.md": "Marco: The integrations step is why we bought it. Never skip it.",
    }
    cases = [
        ('> "the integrations step was the worst part" — P01, line 1', True, "wraps across lines"),
        ('> "I didn\'t want to connect Slack yet." — P01, line 2', True, "straight vs curly apostrophe"),
        ('> “I didn’t want to connect Slack yet.” — P01, line 2', True, "curly quotes in the report"),
        ('> "I didn\'t want to connect Slack [...] I liked the dashboard" — P01, line 2', True, "elision within one source"),
        ('> "the worst part [...] why we bought it" — P01', False, "elision stitching two sources"),
        ('> "I loved the onboarding" — P01, line 9', False, "invented quote"),
        ('> "the integrations step was the best part" — P01, line 1', False, "one word changed"),
        ('> "never skip it" — P02', False, "case changed"),
        ('> "Later I liked the dashboard. [...] the worst part" — P01', False, "fragments out of order"),
        ('> "speed beats polish" — F01:s12, section "Speed"', None, "FigJam quote skipped"),
        ('> "trust" — B01, cluster "trust"', None, "photo quote skipped"),
        ('> "Never skip it." – P02, 03:10', True, "en dash separator"),
    ]
    failed = 0
    for line, expect, label in cases:
        checked, skipped, missing = check(line, src)
        if expect is None:
            ok = skipped == 1 and checked == 0
        else:
            ok = checked == 1 and (not missing) == expect
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {label}")
    print(f"{len(cases) - failed} of {len(cases)} cases pass")
    return 1 if failed else 0


def main(argv) -> int:
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    report, src = Path(argv[1]), Path(argv[2])
    if not report.is_file() or not src.exists():
        print("Report or source path not found.")
        return 2
    sources = load_sources(src)
    if not sources:
        print(f"No text sources found under {src}.")
        return 2
    checked, skipped, missing = check(report.read_text(), sources)
    if checked + skipped == 0:
        print("No evidence quotes found in the report.")
        return 1
    for tag, text in missing:
        print(f'NOT FOUND ({tag}): "{text}"')
    print(f"{checked - len(missing)} of {checked} quotes found verbatim.")
    if skipped:
        print(f"{skipped} photo or board quotes skipped (no text file to check).")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
