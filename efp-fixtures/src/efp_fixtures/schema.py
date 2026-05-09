"""Schema definitions for EFP fixtures."""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class Language(str, Enum):
    """Supported programming languages."""
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    JAVA = "java"
    GO = "go"
    RUBY = "ruby"
    PHP = "php"
    RUST = "rust"
    CSHARP = "csharp"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    SCALA = "scala"
    ELIXIR = "elixir"
    GENERIC = "generic"


class Category(str, Enum):
    """Error categories."""
    NULL_REFERENCE = "null_reference"
    KEY_ERROR = "key_error"
    TYPE_ERROR = "type_error"
    INDEX_ERROR = "index_error"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    AUTH_ERROR = "auth_error"
    PERMISSION_DENIED = "permission_denied"
    RESOURCE_NOT_FOUND = "resource_not_found"
    SYNTAX_ERROR = "syntax_error"
    ASSERTION_ERROR = "assertion_error"
    STACK_OVERFLOW = "stack_overflow"
    OUT_OF_MEMORY = "out_of_memory"
    DATABASE_ERROR = "database_error"
    SERIALIZATION = "serialization"
    CONCURRENCY = "concurrency"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Fixture(BaseModel):
    """Single error fixture with metadata."""
    
    id: str = Field(..., pattern=r'^[a-z]+-\d{3,}$', description="Unique fixture identifier")
    message: str = Field(..., min_length=5, description="Raw error message or stack trace")
    language: Language = Field(..., description="Detected programming language")
    framework: Optional[str] = Field(None, description="Detected framework if applicable")
    category: Category = Field(..., description="Error category classification")
    severity: Severity = Field(..., description="Error severity level")
    notes: Optional[str] = Field(None, description="Additional notes about the error")
    expected_template: Optional[str] = Field(None, description="Expected normalized template")
    tags: List[str] = Field(default_factory=list, description="Relevant tags for filtering")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            Language: lambda v: v.value,
            Category: lambda v: v.value,
            Severity: lambda v: v.value,
        }


class FixtureStats(BaseModel):
    """Statistics about the fixture dataset."""
    
    total: int = Field(..., description="Total number of fixtures")
    by_language: dict[str, int] = Field(..., description="Count by language")
    by_category: dict[str, int] = Field(..., description="Count by category")
    by_severity: dict[str, int] = Field(..., description="Count by severity")
    by_framework: dict[str, int] = Field(default_factory=dict, description="Count by framework")
    with_tags: int = Field(default=0, description="Fixtures with tags")
    with_notes: int = Field(default=0, description="Fixtures with notes")
    with_template: int = Field(default=0, description="Fixtures with expected template")


class FilterOptions(BaseModel):
    """Options for filtering fixtures."""
    
    language: Optional[Language] = None
    category: Optional[Category] = None
    severity: Optional[Severity] = None
    framework: Optional[str] = None
    tags: Optional[List[str]] = None
    has_notes: Optional[bool] = None
    has_template: Optional[bool] = None
    
    def matches(self, fixture: Fixture) -> bool:
        """Check if fixture matches filter criteria."""
        if self.language and fixture.language != self.language:
            return False
        if self.category and fixture.category != self.category:
            return False
        if self.severity and fixture.severity != self.severity:
            return False
        if self.framework and fixture.framework != self.framework:
            return False
        if self.tags:
            if not all(tag in fixture.tags for tag in self.tags):
                return False
        if self.has_notes is not None:
            if bool(fixture.notes) != self.has_notes:
                return False
        if self.has_template is not None:
            if bool(fixture.expected_template) != self.has_template:
                return False
        return True
