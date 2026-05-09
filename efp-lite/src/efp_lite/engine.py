"""Main fingerprinting engine for efp-lite."""

import hashlib
from dataclasses import dataclass
from typing import Optional, Dict, Tuple

from .patterns import NOISE_PATTERNS, full_normalization
from .languages import (
    JavaScriptParser,
    PythonParser,
    JavaParser,
    GoParser,
    GenericParser,
)


PARSERS = [
    JavaScriptParser(),
    PythonParser(),
    JavaParser(),
    GoParser(),
]


@dataclass
class LiteResult:
    """Result from efp-lite fingerprinting engine."""
    
    fingerprint: str
    template: str
    language: str
    framework: Optional[str]
    category: str
    severity: str
    variables: Dict[str, str]
    similar_to: None = None  # Always None in lite version
    processing_ms: int = 0
    _lite: bool = True  # Flag for callers to detect lite vs full API


class LiteEngine:
    """
    Self-hostable fingerprinting engine for 5 languages.
    
    For full language support and edge-case handling, see https://errorfingerprint.dev
    """
    
    def fingerprint(
        self,
        message: str,
        language_hint: Optional[str] = None,
        framework_hint: Optional[str] = None,
    ) -> LiteResult:
        """
        Full fingerprinting pipeline:
        1. Detect language
        2. Parse with language-specific parser
        3. Strip noise (apply NOISE_PATTERNS + path normalization)
        4. Extract template
        5. Classify category + severity
        6. Hash to fingerprint
        7. Return LiteResult
        """
        import time
        start_time = time.time_ns()
        
        # Step 1: Detect language
        language = self._detect_language(message, language_hint)
        
        # Step 2: Parse with language-specific parser
        parser = self._get_parser(language)
        parsed = parser.parse(message)
        
        # Step 3: Strip noise and extract variables
        template, variables = full_normalization(parsed.raw_first_line)
        
        # Step 4: Extract template from parsed message
        if parsed.message:
            template = parsed.message
        
        # Step 5: Classify category and severity
        category, severity = self._classify(parsed.error_type, language)
        
        # Step 6: Make fingerprint
        fingerprint = self._make_fingerprint(language, category, template)
        
        processing_ms = (time.time_ns() - start_time) // 1_000_000
        
        return LiteResult(
            fingerprint=fingerprint,
            template=template,
            language=language,
            framework=framework_hint,
            category=category,
            severity=severity,
            variables=variables,
            processing_ms=processing_ms,
        )
    
    def _detect_language(self, message: str, hint: Optional[str]) -> str:
        """Detect programming language from error message."""
        if hint and hint.lower() in ["javascript", "python", "java", "go"]:
            return hint.lower()
        
        # Try each parser to see if it can parse the message
        for parser in PARSERS:
            if parser.can_parse(message):
                return parser.language
        
        # Fall back to generic parser
        return "generic"
    
    def _get_parser(self, language: str):
        """Get the appropriate parser for a language."""
        for parser in PARSERS:
            if parser.language == language:
                return parser
        
        # Fall back to generic parser
        return GenericParser()
    
    def _classify(self, error_type: str, language: str) -> Tuple[str, str]:
        """Classify error category and severity."""
        error_type_lower = error_type.lower()
        language_lower = language.lower()
        
        # JavaScript classifications
        if language_lower == "javascript":
            if any(keyword in error_type_lower for keyword in [
                "typeerror", "referenceerror", "undefined", "null", "cannot read"
            ]):
                return "null_reference", "error"
            elif any(keyword in error_type_lower for keyword in [
                "syntaxerror", "unexpected token", "invalid character"
            ]):
                return "syntax_error", "error"
            elif any(keyword in error_type_lower for keyword in [
                "rangeerror", "index out of bounds"
            ]):
                return "index_error", "error"
            elif "unhandledpromiserejectionwarning" in error_type_lower:
                return "network_error", "warning"
            elif any(keyword in error_type_lower for keyword in [
                "econnrefused", "connection refused", "connect"
            ]):
                return "network_error", "error"
        
        # Python classifications
        elif language_lower == "python":
            if any(keyword in error_type_lower for keyword in [
                "attributeerror", "nonetype", "null", "has no attribute"
            ]):
                return "null_reference", "error"
            elif "keyerror" in error_type_lower:
                return "key_error", "error"
            elif "indexerror" in error_type_lower:
                return "index_error", "error"
            elif "modulenotfounderror" in error_type_lower:
                return "resource_not_found", "error"
            elif "filenotfounderror" in error_type_lower:
                return "resource_not_found", "error"
            elif "assertionerror" in error_type_lower:
                return "assertion_error", "error"
            elif "jsondecodeerror" in error_type_lower:
                return "serialization", "error"
            elif any(keyword in error_type_lower for keyword in [
                "operationalerror", "connection", "database", "psycopg2", "sqlalchemy"
            ]):
                return "database_error", "error"
        
        # Java classifications
        elif language_lower == "java":
            if any(keyword in error_type_lower for keyword in [
                "nullpointerexception", "null", "cannot invoke"
            ]):
                return "null_reference", "error"
            elif "arrayindexoutofboundsexception" in error_type_lower:
                return "index_error", "error"
            elif "numberformatexception" in error_type_lower:
                return "type_error", "error"
            elif "classcastexception" in error_type_lower:
                return "type_error", "error"
            elif "nosuchmethoderror" in error_type_lower:
                return "type_error", "error"
            elif "nosuchfielderror" in error_type_lower:
                return "type_error", "error"
            elif "illegalargumentexception" in error_type_lower:
                return "type_error", "error"
            elif "outofmemoryerror" in error_type_lower:
                return "out_of_memory", "critical"
            elif "timeoutexception" in error_type_lower:
                return "timeout", "error"
        
        # Go classifications
        elif language_lower == "go":
            if "panic" in error_type_lower:
                if any(keyword in error_type_lower for keyword in [
                    "nil pointer", "nil", "invalid memory address"
                ]):
                    return "null_reference", "error"
                elif any(keyword in error_type_lower for keyword in [
                    "index out of range", "slice bounds", "bounds"
                ]):
                    return "index_error", "error"
                elif any(keyword in error_type_lower for keyword in [
                    "deadlock", "all goroutines are asleep"
                ]):
                    return "concurrency", "critical"
                elif any(keyword in error_type_lower for keyword in [
                    "closed channel", "send on closed"
                ]):
                    return "concurrency", "error"
            elif "runtime error" in error_type_lower:
                return "type_error", "error"
            elif any(keyword in error_type_lower for keyword in [
                "connection refused", "connect", "dial", "handshake timeout"
            ]):
                return "network_error", "error"
            elif "file not found" in error_type_lower:
                return "resource_not_found", "error"
            elif "cannot unmarshal" in error_type_lower:
                return "type_error", "error"
        
        # Default classifications
        return "unknown", "error"
    
    def _make_fingerprint(self, language: str, category: str, template: str) -> str:
        """Generate fingerprint from language, category, and template."""
        # Create normalized input for hashing
        raw = f"{language}:{category}:{template}".lower().strip()
        hash_obj = hashlib.sha256(raw.encode())
        hash_hex = hash_obj.hexdigest()[:8]
        
        # Create fingerprint in format: lang_category_hash
        lang_prefix = language[:2]
        cat_prefix = category[:8]
        
        return f"{lang_prefix}_{cat_prefix}_{hash_hex}"
