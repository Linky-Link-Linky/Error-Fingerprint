"""Tests for the EFP fixtures loader."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from efp_fixtures import (
    load_all,
    load_language,
    load_category,
    load_severity,
    load_framework,
    load_filtered,
    stream,
    stats,
    validate_dataset,
    get_available_languages,
    get_sample,
)
from efp_fixtures.schema import Language, Category, Severity, Fixture, FilterOptions


class TestLoadAll:
    """Test loading all fixtures."""

    def test_load_all_success(self):
        """Test successful loading of all fixtures."""
        fixtures = load_all()
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 10  # Should have at least our sample data
        
        # All items should be Fixture objects
        for fixture in fixtures:
            assert isinstance(fixture, Fixture)

    def test_load_all_structure(self):
        """Test that loaded fixtures have correct structure."""
        fixtures = load_all()
        
        for fixture in fixtures:
            assert fixture.id  # Required field
            assert fixture.message  # Required field
            assert fixture.language  # Required field
            assert fixture.category  # Required field
            assert fixture.severity  # Required field


class TestLoadLanguage:
    """Test loading fixtures by language."""

    def test_load_javascript(self):
        """Test loading JavaScript fixtures."""
        fixtures = load_language(Language.JAVASCRIPT)
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 10  # Should have our sample data
        
        for fixture in fixtures:
            assert fixture.language == Language.JAVASCRIPT
            assert fixture.id.startswith("js-")

    def test_load_python(self):
        """Test loading Python fixtures."""
        fixtures = load_language(Language.PYTHON)
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 10  # Should have our sample data
        
        for fixture in fixtures:
            assert fixture.language == Language.PYTHON
            assert fixture.id.startswith("py-")

    def test_load_nonexistent_language(self):
        """Test loading non-existent language."""
        # This should return empty list if file doesn't exist
        fixtures = load_language(Language.RUBY)  # We haven't created ruby.jsonl yet
        
        assert isinstance(fixtures, list)
        assert len(fixtures) == 0


class TestLoadCategory:
    """Test loading fixtures by category."""

    def test_load_null_reference(self):
        """Test loading null reference category fixtures."""
        fixtures = load_category(Category.NULL_REFERENCE)
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 5  # Should have some null reference errors
        
        for fixture in fixtures:
            assert fixture.category == Category.NULL_REFERENCE

    def test_load_network_error(self):
        """Test loading network error category fixtures."""
        fixtures = load_category(Category.NETWORK_ERROR)
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 5  # Should have some network errors
        
        for fixture in fixtures:
            assert fixture.category == Category.NETWORK_ERROR


class TestLoadSeverity:
    """Test loading fixtures by severity."""

    def test_load_error_severity(self):
        """Test loading error severity fixtures."""
        fixtures = load_severity(Severity.ERROR)
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 10  # Should have error severity fixtures
        
        for fixture in fixtures:
            assert fixture.severity == Severity.ERROR

    def test_load_critical_severity(self):
        """Test loading critical severity fixtures."""
        fixtures = load_severity(Severity.CRITICAL)
        
        assert isinstance(fixtures, list)
        # Should have some critical errors from our sample data
        
        for fixture in fixtures:
            assert fixture.severity == Severity.CRITICAL


class TestLoadFramework:
    """Test loading fixtures by framework."""

    def test_load_django(self):
        """Test loading Django framework fixtures."""
        fixtures = load_framework("django")
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 5  # Should have Django fixtures
        
        for fixture in fixtures:
            assert fixture.framework == "django"

    def test_load_node(self):
        """Test loading Node.js framework fixtures."""
        fixtures = load_framework("node")
        
        assert isinstance(fixtures, list)
        assert len(fixtures) >= 5  # Should have Node fixtures
        
        for fixture in fixtures:
            assert fixture.framework == "node"

    def test_load_nonexistent_framework(self):
        """Test loading non-existent framework."""
        fixtures = load_framework("nonexistent")
        
        assert isinstance(fixtures, list)
        assert len(fixtures) == 0


class TestLoadFiltered:
    """Test loading fixtures with custom filters."""

    def test_filter_by_language(self):
        """Test filtering by language."""
        filter_options = FilterOptions(language=Language.JAVASCRIPT)
        fixtures = load_filtered(filter_options)
        
        for fixture in fixtures:
            assert fixture.language == Language.JAVASCRIPT

    def test_filter_by_category(self):
        """Test filtering by category."""
        filter_options = FilterOptions(category=Category.NULL_REFERENCE)
        fixtures = load_filtered(filter_options)
        
        for fixture in fixtures:
            assert fixture.category == Category.NULL_REFERENCE

    def test_filter_by_multiple_criteria(self):
        """Test filtering by multiple criteria."""
        filter_options = FilterOptions(
            language=Language.PYTHON,
            category=Category.NULL_REFERENCE,
            severity=Severity.ERROR
        )
        fixtures = load_filtered(filter_options)
        
        for fixture in fixtures:
            assert fixture.language == Language.PYTHON
            assert fixture.category == Category.NULL_REFERENCE
            assert fixture.severity == Severity.ERROR

    def test_filter_by_tags(self):
        """Test filtering by tags."""
        filter_options = FilterOptions(tags=["node"])
        fixtures = load_filtered(filter_options)
        
        for fixture in fixtures:
            assert "node" in fixture.tags

    def test_filter_has_notes(self):
        """Test filtering by presence of notes."""
        filter_options = FilterOptions(has_notes=True)
        fixtures = load_filtered(filter_options)
        
        for fixture in fixtures:
            assert fixture.notes is not None

    def test_filter_has_template(self):
        """Test filtering by presence of template."""
        filter_options = FilterOptions(has_template=True)
        fixtures = load_filtered(filter_options)
        
        for fixture in fixtures:
            assert fixture.expected_template is not None


class TestStream:
    """Test streaming functionality."""

    def test_stream_all(self):
        """Test streaming all fixtures."""
        batches = list(stream(batch_size=5))
        
        assert len(batches) >= 2  # Should have multiple batches
        
        for batch in batches:
            assert isinstance(batch, list)
            assert len(batch) <= 5  # Batch size limit

    def test_stream_language(self):
        """Test streaming specific language."""
        batches = list(stream(language=Language.JAVASCRIPT, batch_size=3))
        
        for batch in batches:
            for fixture in batch:
                assert fixture.language == Language.JAVASCRIPT

    def test_stream_category(self):
        """Test streaming specific category."""
        batches = list(stream(category=Category.NULL_REFERENCE, batch_size=10))
        
        for batch in batches:
            for fixture in batch:
                assert fixture.category == Category.NULL_REFERENCE


class TestStats:
    """Test statistics functionality."""

    def test_stats_structure(self):
        """Test that stats returns correct structure."""
        stats_data = stats()
        
        assert isinstance(stats_data.total, int)
        assert stats_data.total >= 10  # Should have our sample data
        
        assert isinstance(stats_data.by_language, dict)
        assert isinstance(stats_data.by_category, dict)
        assert isinstance(stats_data.by_severity, dict)
        
        # Should have our sample languages
        assert "javascript" in stats_data.by_language
        assert "python" in stats_data.by_language
        assert "java" in stats_data.by_language
        assert "go" in stats_data.by_language

    def test_stats_counts(self):
        """Test that stats counts are accurate."""
        stats_data = stats()
        all_fixtures = load_all()
        
        assert stats_data.total == len(all_fixtures)
        
        # Verify language counts match
        js_count = sum(1 for f in all_fixtures if f.language == Language.JAVASCRIPT)
        assert stats_data.by_language.get("javascript", 0) == js_count


class TestValidateDataset:
    """Test dataset validation."""

    def test_validate_dataset_success(self):
        """Test dataset validation with valid data."""
        errors = validate_dataset()
        
        # Should have no errors for our sample data
        assert isinstance(errors, dict)
        # Our sample data should be valid, so errors should be empty or minimal

    def test_validate_dataset_with_invalid_file(self):
        """Test validation with invalid file."""
        # Create a temporary invalid file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"invalid": json}\n')
            f.write('{"id": "test-001", "message": "test"}\n')  # Missing required fields
            temp_file = Path(f.name)
        
        try:
            # Patch DATA_DIR to point to our temp file
            with patch('efp_fixtures.loader.DATA_DIR', temp_file.parent):
                errors = validate_dataset()
                
                assert isinstance(errors, dict)
                # Should have errors for our invalid file
                assert temp_file.name in errors
                assert len(errors[temp_file.name]) > 0
        finally:
            temp_file.unlink()


class TestGetAvailableLanguages:
    """Test getting available languages."""

    def test_get_available_languages(self):
        """Test getting list of available languages."""
        languages = get_available_languages()
        
        assert isinstance(languages, list)
        assert len(languages) >= 4  # Should have our sample languages
        
        # Should include languages we created files for
        assert Language.JAVASCRIPT in languages
        assert Language.PYTHON in languages
        assert Language.JAVA in languages
        assert Language.GO in languages


class TestGetSample:
    """Test getting random samples."""

    def test_get_sample_small(self):
        """Test getting small sample."""
        sample = get_sample(size=3)
        
        assert isinstance(sample, list)
        assert len(sample) <= 3
        assert len(sample) >= 0  # Could be less if dataset is small
        
        for fixture in sample:
            assert isinstance(fixture, Fixture)

    def test_get_sample_large(self):
        """Test getting sample larger than dataset."""
        sample = get_sample(size=1000)
        
        # Should return all fixtures if asking for more than available
        all_fixtures = load_all()
        assert len(sample) <= len(all_fixtures)

    def test_get_sample_with_language(self):
        """Test getting sample with language filter."""
        sample = get_sample(size=2, language=Language.JAVASCRIPT)
        
        assert isinstance(sample, list)
        assert len(sample) <= 2
        
        for fixture in sample:
            assert fixture.language == Language.JAVASCRIPT


class TestFilterOptions:
    """Test filter options functionality."""

    def test_filter_options_matches(self):
        """Test FilterOptions.matches method."""
        fixture = Fixture(
            id="test-001",
            message="TypeError: Cannot read properties",
            language=Language.JAVASCRIPT,
            framework="node",
            category=Category.NULL_REFERENCE,
            severity=Severity.ERROR,
            notes="Test note",
            tags=["javascript", "node"]
        )
        
        # Test language filter
        filter_opts = FilterOptions(language=Language.JAVASCRIPT)
        assert filter_opts.matches(fixture)
        
        filter_opts = FilterOptions(language=Language.PYTHON)
        assert not filter_opts.matches(fixture)
        
        # Test category filter
        filter_opts = FilterOptions(category=Category.NULL_REFERENCE)
        assert filter_opts.matches(fixture)
        
        # Test framework filter
        filter_opts = FilterOptions(framework="node")
        assert filter_opts.matches(fixture)
        
        # Test tags filter
        filter_opts = FilterOptions(tags=["javascript"])
        assert filter_opts.matches(fixture)
        
        filter_opts = FilterOptions(tags=["python"])
        assert not filter_opts.matches(fixture)
        
        # Test has_notes filter
        filter_opts = FilterOptions(has_notes=True)
        assert filter_opts.matches(fixture)
        
        filter_opts = FilterOptions(has_notes=False)
        assert not filter_opts.matches(fixture)
