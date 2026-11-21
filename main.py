#!/usr/bin/env python3
"""ICE-TOAST — catalogue photo of an impossible gadget (make.fun entry).

The program takes the finished catalogue photograph that ships in this
repository (assets/entry.png) and places an exact copy of it at the path
the harness expects: $MAKEFUN_OUTPUT_DIR/entry.png.

Why a plain copy? The photograph itself is the entry — a retro chrome
toaster toasting two golden-brown ice cubes, steam rising, one small plate
as the single accessory. Re-rendering it would only risk changing pixels,
so the program's job is to deliver the picture byte-for-byte, every run.
"""

import os
import shutil
import sys
from pathlib import Path

# The photograph lives next to this script, inside the repository.
SOURCE_IMAGE = Path(__file__).resolve().parent / "assets" / "entry.png"

# Where the harness wants the finished picture. Local runs fall back to
# a plain ./output directory so the script stays testable by hand.
OUTPUT_NAME = "entry.png"


def output_directory() -> Path:
    """Pick the harness output dir, or ./output when run locally."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path(__file__).resolve().parent / "output"


def main() -> int:
    target_dir = output_directory()
    target_dir.mkdir(parents=True, exist_ok=True)

    if not SOURCE_IMAGE.is_file():
        print(f"missing source image: {SOURCE_IMAGE}", file=sys.stderr)
        return 1

    destination = target_dir / OUTPUT_NAME
    shutil.copyfile(SOURCE_IMAGE, destination)

    # Confirm the copy landed intact before reporting success: a
    # truncated write must fail loudly here, never silently upstream.
    expected = SOURCE_IMAGE.stat().st_size
    actual = destination.stat().st_size
    if actual != expected:
        print(
            f"copy incomplete: expected {expected} bytes, got {actual}",
            file=sys.stderr,
        )
        return 1

    size = actual
    print(f"wrote {destination} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
