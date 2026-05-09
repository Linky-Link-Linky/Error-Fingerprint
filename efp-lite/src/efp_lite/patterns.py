"""Noise stripping patterns for efp-lite engine."""

import re
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class Pattern:
    """A regex pattern for noise stripping."""
    name: str
    regex: re.Pattern
    placeholder: str


# Pre-compiled noise patterns
NOISE_PATTERNS: list[Pattern] = [
    Pattern("uuid", re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I), "{uuid}"),
    Pattern("ipv4", re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?\b'), "{ip}"),
    Pattern("ipv6", re.compile(r'\b([0-9a-f]{1,4}:){7}[0-9a-f]{1,4}\b', re.I), "{ip}"),
    Pattern("timestamp", re.compile(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?'), "{timestamp}"),
    Pattern("hex_addr", re.compile(r'0x[0-9a-fA-F]{4,}'), "{addr}"),
    Pattern("jwt", re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'), "{token}"),
    Pattern("base64", re.compile(r'[A-Za-z0-9+/]{20,}={0,2}'), "{blob}"),
    Pattern("hex_str", re.compile(r'\b[0-9a-fA-F]{7,}\b'), "{hex}"),
    Pattern("long_num", re.compile(r'\b\d{5,}\b'), "{id}"),
    Pattern("ansi", re.compile(r'\x1b\[[0-9;]*m'), ""),
]

# Path patterns
UNIX_PATH_RE = re.compile(r'(/[a-zA-Z0-9_.\-]+){3,}')
WIN_PATH_RE = re.compile(r'[A-Za-z]:\\[^\s:]+')
FILENAME_RE = re.compile(r'([^/\\]+\.[a-z]{1,6})$', re.I)

# Line/column patterns
LINE_COL_RE = re.compile(r':(\d+):(\d+)(?::\d+)?$')
LINE_ONLY_RE = re.compile(r':(\d+)$')

# Memory address patterns
MEMORY_ADDR_RE = re.compile(r'0x[0-9a-fA-F]+')

# Function name patterns
FUNCTION_RE = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\(')


def strip_noise(message: str) -> Tuple[str, Dict[str, str]]:
    """
    Strip noise from error message and extract variables.
    
    Args:
        message: Raw error message
        
    Returns:
        Tuple of (stripped_message, extracted_variables)
    """
    stripped = message
    variables = {}
    
    for pattern in NOISE_PATTERNS:
        matches = pattern.regex.findall(stripped)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]  # Take first group if tuple
            
            # Store the original value
            if pattern.name not in variables:
                variables[pattern.name] = []
            variables[pattern.name].append(match)
            
            # Replace with placeholder
            stripped = stripped.replace(match, pattern.placeholder)
    
    # Normalize whitespace
    stripped = re.sub(r'\s+', ' ', stripped).strip()
    
    return stripped, variables


def normalize_paths(message: str) -> str:
    """
    Normalize file paths in error messages.
    
    Args:
        message: Error message with paths
        
    Returns:
        Message with normalized paths
    """
    # Normalize Unix paths
    message = UNIX_PATH_RE.sub('{path}', message)
    
    # Normalize Windows paths
    message = WIN_PATH_RE.sub('{path}', message)
    
    # Normalize filenames
    message = FILENAME_RE.sub('{filename}', message)
    
    return message


def extract_line_col(message: str) -> str:
    """
    Extract and normalize line/column information.
    
    Args:
        message: Error message with line/col info
        
    Returns:
        Message with normalized line/col
    """
    # Replace line:col patterns
    message = LINE_COL_RE.sub(':{line}:{col}', message)
    
    # Replace line-only patterns
    message = LINE_ONLY_RE.sub(':{line}', message)
    
    return message


def normalize_memory_addresses(message: str) -> str:
    """
    Normalize memory addresses in error messages.
    
    Args:
        message: Error message with memory addresses
        
    Returns:
        Message with normalized addresses
    """
    return MEMORY_ADDR_RE.sub('{addr}', message)


def normalize_function_names(message: str) -> str:
    """
    Normalize function names in error messages.
    
    Args:
        message: Error message with function names
        
    Returns:
        Message with normalized function names
    """
    return FUNCTION_RE.sub('{function}(', message)


def full_normalization(message: str) -> Tuple[str, Dict[str, str]]:
    """
    Apply all normalization steps to error message.
    
    Args:
        message: Raw error message
        
    Returns:
        Tuple of (normalized_message, extracted_variables)
    """
    # Strip noise and extract variables
    stripped, variables = strip_noise(message)
    
    # Apply additional normalizations
    stripped = normalize_paths(stripped)
    stripped = extract_line_col(stripped)
    stripped = normalize_memory_addresses(stripped)
    stripped = normalize_function_names(stripped)
    
    return stripped, variables
