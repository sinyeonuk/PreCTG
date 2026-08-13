"""Compatibility wrapper for the maintained prediction command."""

from __future__ import annotations

from prectg.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["predict", *__import__("sys").argv[1:]]))
