"""Tests for efp-lite engine."""

import pytest

from efp_lite import LiteEngine, LiteResult


class TestLiteEngine:
    """Test cases for LiteEngine."""

    def test_init(self):
        """Test engine initialization."""
        engine = LiteEngine()
        assert engine is not None
        assert hasattr(engine, 'fingerprint')

    def test_fingerprint_javascript(self):
        """Test JavaScript fingerprinting."""
        engine = LiteEngine()
        
        # Test basic JavaScript error
        message = "TypeError: Cannot read properties of undefined (reading 'id')"
        result = engine.fingerprint(message)
        
        assert isinstance(result, LiteResult)
        assert result.language == "javascript"
        assert result.category == "null_reference"
        assert result.severity == "error"
        assert result.similar_to is None  # Always None in lite
        assert result._lite is True  # Should be True for lite engine
        assert result.fingerprint.startswith("js_")

    def test_fingerprint_python(self):
        """Test Python fingerprinting."""
        engine = LiteEngine()
        
        # Test basic Python error
        message = "Traceback (most recent call last):\n  File \"main.py\", line 23, in <module>\n    user = get_user()\nKeyError: 'user_123'"
        result = engine.fingerprint(message)
        
        assert isinstance(result, LiteResult)
        assert result.language == "python"
        assert result.category == "key_error"
        assert result.severity == "error"
        assert result.similar_to is None
        assert result._lite is True
        assert result.fingerprint.startswith("py_")

    def test_fingerprint_java(self):
        """Test Java fingerprinting."""
        engine = LiteEngine()
        
        # Test basic Java error
        message = "java.lang.NullPointerException: Cannot invoke method"
        result = engine.fingerprint(message)
        
        assert isinstance(result, LiteResult)
        assert result.language == "java"
        assert result.category == "null_reference"
        assert result.severity == "error"
        assert result.similar_to is None
        assert result._lite is True
        assert result.fingerprint.startswith("java_")

    def test_fingerprint_go(self):
        """Test Go fingerprinting."""
        engine = LiteEngine()
        
        # Test basic Go error
        message = "panic: runtime error: index out of range"
        result = engine.fingerprint(message)
        
        assert isinstance(result, LiteResult)
        assert result.language == "go"
        assert result.category == "index_error"
        assert result.severity == "error"
        assert result.similar_to is None
        assert result._lite is True
        assert result.fingerprint.startswith("go_")

    def test_fingerprint_generic(self):
        """Test generic fallback parser."""
        engine = LiteEngine()
        
        # Test generic error
        message = "Error: Something went wrong"
        result = engine.fingerprint(message)
        
        assert isinstance(result, LiteResult)
        assert result.language == "generic"
        assert result.category == "unknown"
        assert result.severity == "error"
        assert result.similar_to is None
        assert result._lite is True
        assert result.fingerprint.startswith("gen_")

    def test_language_hint(self):
        """Test language hint functionality."""
        engine = LiteEngine()
        
        # Test with language hint
        message = "TypeError: Cannot read properties"
        result = engine.fingerprint(message, language_hint="javascript")
        
        assert result.language == "javascript"
        assert result.fingerprint.startswith("js_")

    def test_framework_hint(self):
        """Test framework hint functionality."""
        engine = LiteEngine()
        
        # Test with framework hint
        message = "NullPointerException: Cannot invoke method"
        result = engine.fingerprint(message, framework_hint="spring")
        
        assert result.framework == "spring"

    def test_determinism(self):
        """Test that fingerprinting is deterministic."""
        engine = LiteEngine()
        
        message = "TypeError: Cannot read properties of undefined"
        
        # Generate fingerprint 10 times
        fingerprints = []
        for _ in range(10):
            result = engine.fingerprint(message)
            fingerprints.append(result.fingerprint)
        
        # All fingerprints should be identical
        assert len(set(fingerprints)) == 1
        assert all(fp == fingerprints[0] for fp in fingerprints)

    def test_different_errors_different_fingerprints(self):
        """Test that different errors produce different fingerprints."""
        engine = LiteEngine()
        
        message1 = "TypeError: Cannot read properties of undefined"
        message2 = "ReferenceError: user is not defined"
        
        result1 = engine.fingerprint(message1)
        result2 = engine.fingerprint(message2)
        
        # Fingerprints should be different
        assert result1.fingerprint != result2.fingerprint

    def test_noise_stripping(self):
        """Test that noise is properly stripped."""
        engine = LiteEngine()
        
        # Test with UUID
        message_with_uuid = "TypeError: Cannot read properties of 550e8400-e29b-41d4-a716-44665544000000"
        result = engine.fingerprint(message_with_uuid)
        
        assert "uuid" in result.variables
        assert "{uuid}" in result.template
        assert "550e8400-e29b-41d4-a716-44665544000000" not in result.template

    def test_processing_time(self):
        """Test that processing time is recorded."""
        engine = LiteEngine()
        
        message = "TypeError: Cannot read properties"
        result = engine.fingerprint(message)
        
        assert isinstance(result.processing_ms, int)
        assert result.processing_ms >= 0
        assert result.processing_ms < 100  # Should be fast

    def test_empty_message(self):
        """Test handling of empty message."""
        engine = LiteEngine()
        
        result = engine.fingerprint("")
        
        assert isinstance(result, LiteResult)
        assert result.language == "generic"
        assert result.category == "unknown"

    def test_long_message(self):
        """Test handling of long message."""
        engine = LiteEngine()
        
        # Create a very long message
        long_message = "TypeError: " + "x" * 1000
        
        result = engine.fingerprint(long_message)
        
        assert isinstance(result, LiteResult)
        assert result.template is not None
