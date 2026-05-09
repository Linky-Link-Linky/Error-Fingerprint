"""Base interface for language parsers."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedError:
    """Structured error information extracted from raw error string."""
    
    error_type: str        # "TypeError", "NullPointerException", etc.
    message: str           # Human-readable message after the colon
    location: Optional[str]  # file:line or equivalent
    raw_first_line: str    # The first meaningful line before noise stripping


class LanguageParser:
    """Base interface all language parsers must implement."""
    
    language: str  # Class variable for language identification
    
    def can_parse(self, message: str) -> bool:
        """
        Return True if this parser recognizes the message format.
        
        Args:
            message: Raw error string
            
        Returns:
            True if this parser can handle the message
        """
        raise NotImplementedError
    
    def parse(self, message: str) -> ParsedError:
        """
        Extract structured fields from a raw error string.
        
        Args:
            message: Raw error string
            
        Returns:
            ParsedError with extracted information
        """
        raise NotImplementedError
