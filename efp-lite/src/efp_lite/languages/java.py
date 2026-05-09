"""Java language parser for efp-lite."""

import re
from .base import LanguageParser, ParsedError


class JavaParser(LanguageParser):
    """Parser for Java error messages."""
    
    language = "java"
    
    # Java exception patterns
    EXCEPTION_RE = re.compile(r'^([a-zA-Z$][\w.$]*(?:Exception|Error)):\s*(.+)')
    ANDROID_EXCEPTION_RE = re.compile(r'^([a-zA-Z$][\w.$]*(?:Exception|Error)):\s*(.+)')
    
    # Stack frame patterns
    FRAME_RE = re.compile(r'^\s+at\s+([a-zA-Z$][\w.$]*)\(([^)]+)\)')
    NATIVE_METHOD_RE = re.compile(r'^\s+at\s+([a-zA-Z$][\w.$]*)\(Native Method\)')
    
    # Caused by pattern
    CAUSED_BY_RE = re.compile(r'^Caused by:\s+(.+)')
    
    # Location patterns
    LOCATION_RE = re.compile(r'([^.]+)\.java:(\d+)')
    
    def can_parse(self, message: str) -> bool:
        """Check if message looks like a Java error."""
        lines = message.strip().split('\n')
        if not lines:
            return False
        
        message_lower = message.lower()
        
        # Look for Java-specific indicators
        java_indicators = [
            'exception:',
            'error:',
            'caused by:',
            'at ',
            '.java:',
            'com.',
            'org.',
            'java.',
            'javax.',
        ]
        
        return any(indicator in message_lower for indicator in java_indicators)
    
    def parse(self, message: str) -> ParsedError:
        """Parse Java error message."""
        lines = message.strip().split('\n')
        if not lines:
            return ParsedError("Exception", message, None, message)
        
        # Find the root cause (last exception in chain)
        root_exception = None
        location = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for exception lines
            match = self.EXCEPTION_RE.match(line)
            if match:
                root_exception = line
                continue
            
            # Look for location in stack frames
            if not location:
                frame_match = self.FRAME_RE.match(line)
                if frame_match:
                    method = frame_match.group(1)
                    frame_info = frame_match.group(2)
                    
                    # Extract file and line from frame info
                    location_match = self.LOCATION_RE.search(frame_info)
                    if location_match:
                        file_name = location_match.group(1)
                        line_num = location_match.group(2)
                        location = f"{file_name}.java:{line_num}"
                    elif "Native Method" in frame_info:
                        location = "Native Method"
                    continue
        
        # Parse the root exception
        error_type = "Exception"
        error_message = root_exception or lines[0].strip()
        
        if root_exception:
            match = self.EXCEPTION_RE.match(root_exception)
            if match:
                error_type = match.group(1)
                if len(match.groups()) > 1:
                    error_message = match.group(2)
        
        return ParsedError(
            error_type=error_type,
            message=error_message,
            location=location,
            raw_first_line=lines[0].strip()
        )
