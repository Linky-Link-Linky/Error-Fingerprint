"""EFP Lite - Self-hostable error fingerprinting engine."""

from .engine import LiteEngine, LiteResult
from .patterns import NOISE_PATTERNS
from .languages import (
    LanguageParser,
    JavaScriptParser,
    PythonParser,
    JavaParser,
    GoParser,
    GenericParser,
)

__version__ = "0.1.0"
__all__ = [
    "LiteEngine",
    "LiteResult",
    "NOISE_PATTERNS",
    "LanguageParser",
    "JavaScriptParser",
    "PythonParser",
    "JavaParser",
    "GoParser",
    "GenericParser",
]
