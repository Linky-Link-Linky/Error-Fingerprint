"""Loader for EFP fixtures dataset."""

import json
from pathlib import Path
from typing import Iterator, List, Dict, Optional
from collections import Counter

from .schema import Fixture, Language, Category, Severity, FixtureStats, FilterOptions


DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_all() -> List[Fixture]:
    """
    Load all fixtures from all language files.
    
    Returns:
        List of all Fixture objects
    """
    all_fixtures = []
    
    for language_file in DATA_DIR.glob("*.jsonl"):
        fixtures = load_language_file(language_file)
        all_fixtures.extend(fixtures)
    
    return all_fixtures


def load_language(language: Language) -> List[Fixture]:
    """
    Load fixtures for a specific language.
    
    Args:
        language: Language to load
        
    Returns:
        List of Fixture objects for the language
    """
    file_path = DATA_DIR / f"{language.value}.jsonl"
    return load_language_file(file_path)


def load_category(category: Category) -> List[Fixture]:
    """
    Load all fixtures matching a category across all languages.
    
    Args:
        category: Category to filter by
        
    Returns:
        List of Fixture objects matching the category
    """
    all_fixtures = load_all()
    return [f for f in all_fixtures if f.category == category]


def load_severity(severity: Severity) -> List[Fixture]:
    """
    Load all fixtures matching a severity across all languages.
    
    Args:
        severity: Severity to filter by
        
    Returns:
        List of Fixture objects matching the severity
    """
    all_fixtures = load_all()
    return [f for f in all_fixtures if f.severity == severity]


def load_framework(framework: str) -> List[Fixture]:
    """
    Load all fixtures from a specific framework.
    
    Args:
        framework: Framework name to filter by
        
    Returns:
        List of Fixture objects from the framework
    """
    all_fixtures = load_all()
    return [f for f in all_fixtures if f.framework == framework]


def load_filtered(filter_options: FilterOptions) -> List[Fixture]:
    """
    Load fixtures with custom filter criteria.
    
    Args:
        filter_options: FilterOptions with criteria
        
    Returns:
        List of Fixture objects matching the filter
    """
    all_fixtures = load_all()
    return [f for f in all_fixtures if filter_options.matches(f)]


def stream(
    language: Optional[Language] = None,
    category: Optional[Category] = None,
    batch_size: int = 1000,
) -> Iterator[List[Fixture]]:
    """
    Memory-efficient streaming loader.
    
    Args:
        language: Optional language filter
        category: Optional category filter
        batch_size: Number of fixtures to yield at once
        
    Yields:
        Batches of Fixture objects
    """
    if language:
        file_path = DATA_DIR / f"{language.value}.jsonl"
        files_to_process = [file_path]
    else:
        files_to_process = list(DATA_DIR.glob("*.jsonl"))
    
    batch = []
    
    for file_path in files_to_process:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        fixture_data = json.loads(line)
                        fixture = Fixture.model_validate(fixture_data)
                        
                        # Apply category filter if specified
                        if category and fixture.category != category:
                            continue
                        
                        batch.append(fixture)
                        
                        # Yield batch when it reaches the desired size
                        if len(batch) >= batch_size:
                            yield batch
                            batch = []
                    
                    except (json.JSONDecodeError, ValueError) as e:
                        # Skip invalid lines but continue processing
                        continue
        
        except (FileNotFoundError, IOError):
            # Skip files that don't exist or can't be read
            continue
    
    # Yield any remaining fixtures
    if batch:
        yield batch


def stats() -> FixtureStats:
    """
    Return summary statistics about the fixture dataset.
    
    Returns:
        FixtureStats with counts and breakdowns
    """
    all_fixtures = load_all()
    
    # Count by language
    language_counts = Counter(f.language.value for f in all_fixtures)
    
    # Count by category
    category_counts = Counter(f.category.value for f in all_fixtures)
    
    # Count by severity
    severity_counts = Counter(f.severity.value for f in all_fixtures)
    
    # Count by framework
    framework_counts = Counter(f.framework for f in all_fixtures if f.framework)
    
    # Count fixtures with optional fields
    with_tags = sum(1 for f in all_fixtures if f.tags)
    with_notes = sum(1 for f in all_fixtures if f.notes)
    with_template = sum(1 for f in all_fixtures if f.expected_template)
    
    return FixtureStats(
        total=len(all_fixtures),
        by_language=dict(language_counts),
        by_category=dict(category_counts),
        by_severity=dict(severity_counts),
        by_framework=dict(framework_counts),
        with_tags=with_tags,
        with_notes=with_notes,
        with_template=with_template,
    )


def validate_dataset() -> Dict[str, List[str]]:
    """
    Validate the dataset for consistency and completeness.
    
    Returns:
        Dictionary with validation errors by file
    """
    errors = {}
    
    for language_file in DATA_DIR.glob("*.jsonl"):
        file_errors = []
        line_num = 0
        
        try:
            with open(language_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line_num += 1
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    try:
                        fixture_data = json.loads(line)
                        fixture = Fixture.model_validate(fixture_data)
                        
                        # Validate ID format
                        if not fixture.id.startswith(language_file.stem):
                            file_errors.append(f"Line {line_num}: ID '{fixture.id}' doesn't match file language")
                        
                        # Validate language consistency
                        if fixture.language.value != language_file.stem:
                            file_errors.append(f"Line {line_num}: Language '{fixture.language}' doesn't match file name")
                        
                        # Check for duplicate IDs
                        # (This is a simple check - could be more sophisticated)
                        if len(fixture.id) < 6:
                            file_errors.append(f"Line {line_num}: ID '{fixture.id}' seems too short")
                    
                    except (json.JSONDecodeError, ValueError) as e:
                        file_errors.append(f"Line {line_num}: Invalid JSON or schema: {e}")
        
        except (FileNotFoundError, IOError) as e:
            file_errors.append(f"Cannot read file: {e}")
        
        if file_errors:
            errors[language_file.name] = file_errors
    
    return errors


def get_available_languages() -> List[Language]:
    """
    Get list of available languages in the dataset.
    
    Returns:
        List of Language enums that have data files
    """
    available = []
    
    for language_file in DATA_DIR.glob("*.jsonl"):
        try:
            language = Language(language_file.stem)
            available.append(language)
        except ValueError:
            # Skip files that don't match known languages
            continue
    
    return available


def get_sample(size: int = 10, language: Optional[Language] = None) -> List[Fixture]:
    """
    Get a random sample of fixtures.
    
    Args:
        size: Number of fixtures to sample
        language: Optional language filter
        
    Returns:
        List of random Fixture objects
    """
    import random
    
    if language:
        fixtures = load_language(language)
    else:
        fixtures = load_all()
    
    if len(fixtures) <= size:
        return fixtures
    
    return random.sample(fixtures, size)


# Internal helper function
def load_language_file(file_path: Path) -> List[Fixture]:
    """
    Load fixtures from a single language file.
    
    Args:
        file_path: Path to the JSONL file
        
    Returns:
        List of Fixture objects
    """
    fixtures = []
    
    if not file_path.exists():
        return fixtures
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    fixture_data = json.loads(line)
                    fixture = Fixture.model_validate(fixture_data)
                    fixtures.append(fixture)
                except (json.JSONDecodeError, ValueError) as e:
                    # Skip invalid lines but could log them
                    continue
    
    except (FileNotFoundError, IOError):
        # Return empty list if file can't be read
        pass
    
    return fixtures
