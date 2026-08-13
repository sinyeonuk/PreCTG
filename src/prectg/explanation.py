"""Korean display labels derived from stable result codes."""

from __future__ import annotations

from prectg.schema import Signal

SIGNAL_LABELS = {
    Signal.LOW: "낮은 위험 신호",
    Signal.REVIEW: "관찰 필요",
    Signal.HIGH: "우선 검토 필요",
    Signal.UNAVAILABLE: "결과 없음",
}


def signal_label(signal: Signal | str) -> str:
    return SIGNAL_LABELS[Signal(signal)]
