"""Python language parser for efp-lite."""

import re
from .base import LanguageParser, ParsedError


class PythonParser(LanguageParser):
    """Parser for Python error messages."""
    
    language = "python"
    
    # Python traceback patterns
    TRACEBACK_RE = re.compile(r'^Traceback \(most recent call last\):')
    EXCEPTION_RE = re.compile(r'^(\w+(?:\.\w+)*)Error:\s*(.+)')
    EXCEPTION_SIMPLE_RE = re.compile(r'^(\w+):\s*(.+)')
    
    # Frame patterns
    FRAME_RE = re.compile(r'^\s*File "([^"]+)", line (\d+), in (\w+)$')
    CODE_LINE_RE = re.compile(r'^\s+([^\s].*)$')
    
    # Chained exception patterns
    CHAINED_RE = re.compile(r'^During handling of the above exception, another exception occurred:')
    
    def can_parse(self, message: str) -> bool:
        """Check if message looks like a Python error."""
        lines = message.strip().split('\n')
        if not lines:
            return False
        
        # Look for traceback pattern
        if self.TRACEBACK_RE.match(lines[0].strip()):
            return True
        
        # Look for exception pattern
        for line in lines:
            if self.EXCEPTION_RE.match(line.strip()) or self.EXCEPTION_SIMPLE_RE.match(line.strip()):
                return True
        
        return False
    
    def parse(self, message: str) -> ParsedError:
        """Parse Python error message."""
        lines = message.strip().split('\n')
        if not lines:
            return ParsedError("Unknown", message, None, message)
        
        first_line = lines[0].strip()
        
        # Handle full traceback
        if self.TRACEBACK_RE.match(first_line):
            return self._parse_traceback(lines)
        
        # Handle simple exception
        return self._parse_simple_exception(lines)
    
    def _parse_traceback(self, lines) -> ParsedError:
        """Parse a full Python traceback."""
        # Find the exception line (last non-empty line)
        exception_line = None
        location = None
        
        for line in reversed(lines):
            line = line.strip()
            if line:
                exception_line = line
                break
        
        # Extract location from the last frame
        for i in range(len(lines) - 2, -1, -1):
            line = lines[i].strip()
            if self.FRAME_RE.match(line):
                match = self.FRAME_RE.match(line)
                if match:
                    file_path = match.group(1)
                    line_num = match.group(2)
                    function = match.group(3)
                    location = f"{file_path}:{line_num}"
                break
        
        # Parse exception type and message
        error_type = "Exception"
        error_message = exception_line
        
        if exception_line:
            for pattern in [self.EXCEPTION_RE, self.EXCEPTION_SIMPLE_RE]:
                match = pattern.match(exception_line)
                if match:
                    error_type = match.group(1)
                    if len(match.groups()) > 1:
                        error_message = match.group(2)
                    break
        
        return ParsedError(
            error_type=error_type,
            message=error_message,
            location=location,
            raw_first_line=lines[0].strip()
        )
    
    def _parse_simple_exception(self, lines) -> ParsedError:
        """Parse a simple exception without traceback."""
        first_line = lines[0].strip()
        
        # Parse exception type and message
        error_type = "Exception"
        error_message = first_line
        
        for pattern in [self.EXCEPTION_RE, self.EXCEPTION_SIMPLE_RE]:
            match = pattern.match(first_line)
            if match:
                error_type = match.group(1)
                if len(match.groups()) > 1:
                    error_message = match.group(2)
                break
        
        return ParsedError(
            error_type=error_type,
            message=error_message,
            location=None,
            raw_first_line=first_line
        )
