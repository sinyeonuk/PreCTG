"""Shared schema enums and model-result states."""

from __future__ import annotations

from enum import StrEnum


class AvailabilityTiming(StrEnum):
    """Earliest point at which a feature is available."""

    PRE_LABOR = "PRE_LABOR"
    EARLY_CTG = "EARLY_CTG"
    POST_WINDOW = "POST_WINDOW"
    POST_DELIVERY = "POST_DELIVERY"
    TARGET = "TARGET"
    UNKNOWN = "UNKNOWN"


class ModelStatus(StrEnum):
    """Explicit ML result availability state."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    INSUFFICIENT_DATA = "insufficient_data"
