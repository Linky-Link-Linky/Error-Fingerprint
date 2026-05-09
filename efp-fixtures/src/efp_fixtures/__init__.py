"""EFP Fixtures - 5,000+ labeled real-world error corpus."""

from .loader import (
    load_all,
    load_language,
    load_category,
    load_severity,
    load_framework,
    load_filtered,
    stream,
    stats,
    validate_dataset,
    get_available_languages,
    get_sample,
)
from .schema import (
    Fixture,
    FixtureStats,
    FilterOptions,
    Language,
    Category,
    Severity,
)

__version__ = "0.1.0"
__all__ = [
    # Loader functions
    "load_all",
    "load_language",
    "load_category",
    "load_severity",
    "load_framework",
    "load_filtered",
    "stream",
    "stats",
    "validate_dataset",
    "get_available_languages",
    "get_sample",
    # Schema classes
    "Fixture",
    "FixtureStats",
    "FilterOptions",
    "Language",
    "Category",
    "Severity",
]
