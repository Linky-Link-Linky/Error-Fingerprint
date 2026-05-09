"""JavaScript language parser for efp-lite."""

import re
from .base import LanguageParser, ParsedError


class JavaScriptParser(LanguageParser):
    """Parser for JavaScript error messages."""
    
    language = "javascript"
    
    # JavaScript error patterns
    ERROR_PATTERNS = [
        re.compile(r'^(TypeError|ReferenceError|SyntaxError|RangeError|URIError|EvalError):\s*(.+)', re.I),
        re.compile(r'^(UnhandledPromiseRejectionWarning):\s*(.+)', re.I),
        re.compile(r'^(Error):\s*(.+)', re.I),
    ]
    
    # Stack frame patterns
    V8_FRAME_RE = re.compile(r'\s+at\s+([^\s(]+)\s*\(([^)]+)\)')
    SPIDERMONKEY_FRAME_RE = re.compile(r'([^\s@]+)@([^:]+):(\d+):(\d+)')
    
    # Location patterns
    LOCATION_RE = re.compile(r'at\s+([^\s(]+)\s*\(([^)]+):(\d+):(\d+)\)')
    SIMPLE_LOCATION_RE = re.compile(r'([^.]+)\.js:(\d+):(\d+)')
    
    def can_parse(self, message: str) -> bool:
        """Check if message looks like a JavaScript error."""
        message_lower = message.lower()
        
        # Check for common JavaScript error indicators
        js_indicators = [
            'typeerror:',
            'referenceerror:',
            'syntaxerror:',
            'rangeerror:',
            'uriserror:',
            'evalerror:',
            'unhandledpromiserejectionwarning:',
            ' at ',
            '.js:',
            'node:',
        ]
        
        return any(indicator in message_lower for indicator in js_indicators)
    
    def parse(self, message: str) -> ParsedError:
        """Parse JavaScript error message."""
        lines = message.strip().split('\n')
        if not lines:
            return ParsedError("Unknown", message, None, message)
        
        first_line = lines[0].strip()
        
        # Extract error type and message
        error_type = "Error"
        error_message = first_line
        
        for pattern in self.ERROR_PATTERNS:
            match = pattern.match(first_line)
            if match:
                error_type = match.group(1)
                if len(match.groups()) > 1:
                    error_message = match.group(2)
                break
        
        # Extract location from stack frames
        location = None
        if len(lines) > 1:
            # Look for location in stack frames
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # Try V8 format: at FunctionName (file.js:line:col)
                match = self.LOCATION_RE.search(line)
                if match:
                    func_name = match.group(1)
                    file_path = match.group(2)
                    line_num = match.group(3)
                    col_num = match.group(4)
                    location = f"{file_path}:{line_num}:{col_num}"
                    break
                
                # Try SpiderMonkey format: FunctionName@file.js:line:col
                match = self.SPIDERMONKEY_FRAME_RE.match(line)
                if match:
                    func_name = match.group(1)
                    file_path = match.group(2)
                    line_num = match.group(3)
                    col_num = match.group(4)
                    location = f"{file_path}:{line_num}:{col_num}"
                    break
                
                # Try simple format: file.js:line:col
                match = self.SIMPLE_LOCATION_RE.search(line)
                if match:
                    file_path = match.group(1)
                    line_num = match.group(2)
                    col_num = match.group(3)
                    location = f"{file_path}:{line_num}:{col_num}"
                    break
        
        return ParsedError(
            error_type=error_type,
            message=error_message,
            location=location,
            raw_first_line=first_line
        )
