"""Go language parser for efp-lite."""

import re
from .base import LanguageParser, ParsedError


class GoParser(LanguageParser):
    """Parser for Go error messages."""
    
    language = "go"
    
    # Go error patterns
    PANIC_RE = re.compile(r'^panic:\s*(.+)')
    RUNTIME_ERROR_RE = re.compile(r'^runtime error:\s*(.+)')
    GOROUTINE_RE = re.compile(r'^goroutine \d+\s*\[running\]:')
    
    def can_parse(self, message: str) -> bool:
        """Check if message looks like a Go error."""
        message_lower = message.lower()
        
        # Check for Go-specific error indicators
        go_indicators = [
            'panic:',
            'runtime error:',
            'goroutine ',
        ]
        
        return any(indicator in message_lower for indicator in go_indicators)
    
    def parse(self, message: str) -> ParsedError:
        """Parse Go error message."""
        lines = message.strip().split('\n')
        if not lines:
            return ParsedError("Unknown", message, None, message)
        
        first_line = lines[0].strip()
        
        # Parse panic message
        panic_match = self.PANIC_RE.match(first_line)
        if panic_match:
            error_type = "panic"
            error_message = panic_match.group(1).strip()
            location = None
            return ParsedError(error_type, error_message, location, first_line)
        
        # Parse runtime error
        runtime_match = self.RUNTIME_ERROR_RE.match(first_line)
        if runtime_match:
            error_type = "runtime_error"
            error_message = runtime_match.group(1).strip()
            location = None
            return ParsedError(error_type, error_message, location, first_line)
        
        # Parse goroutine information
        goroutine_match = self.GOROUTINE_RE.search(message)
        if goroutine_match:
            # Extract goroutine number
            goroutine_num = goroutine_match.group(1)
            
            # Find the actual error line
            error_line = None
            for line in lines:
                if 'created by goroutine' in line.lower():
                    # Skip goroutine creation lines
                    continue
                if line.strip():
                    error_line = line.strip()
                    break
            
            if error_line:
                # Check for panic or runtime error in the error line
                if 'panic:' in error_line.lower():
                    error_type = "panic"
                    error_message = error_line.split(':', 1)[1].strip()
                elif 'runtime error:' in error_line.lower():
                    error_type = "runtime_error"
                    error_message = error_line.split(':', 1)[1].strip()
                else:
                    error_type = "runtime_error"
                    error_message = error_line.strip()
                
                location = f"goroutine {goroutine_num}"
        
        return ParsedError(error_type, error_message, location, first_line)
