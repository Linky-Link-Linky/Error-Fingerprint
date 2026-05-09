"""Generic language parser for efp-lite."""

from .base import LanguageParser, ParsedError


class GenericParser(LanguageParser):
    """Fallback parser for unrecognized error formats."""
    
    language = "generic"
    
    def can_parse(self, message: str) -> bool:
        """Generic parser can parse any message."""
        return True
    
    def parse(self, message: str) -> ParsedError:
        """Parse error message using generic approach."""
        lines = message.strip().split('\n')
        if not lines:
            return ParsedError("Error", message, None, message)
        
        first_line = lines[0].strip()
        
        # Try to extract error type from common patterns
        error_type = "Error"
        error_message = first_line
        
        # Look for common error prefixes
        prefixes = [
            "Error:", "Exception:", "Failed:", "Warning:",
            "Critical:", "Fatal:", "Panic:", "Abort:"
        ]
        
        for prefix in prefixes:
            if first_line.startswith(prefix):
                error_type = prefix.rstrip(":")
                error_message = first_line[len(prefix):].strip()
                break
        
        return ParsedError(
            error_type=error_type,
            message=error_message,
            location=None,
            raw_first_line=first_line
        )
