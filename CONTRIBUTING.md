# Contributing to Error Fingerprint

Thank you for your interest in contributing to Error Fingerprint! This document provides guidelines and information for contributors.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (for efp-lite testing)
- Git

### Setting Up
```bash
# Clone the repository
git clone https://github.com/Linky-Link-Linky/Error-Fingerprint.git
cd Error-Fingerprint

# Install dependencies for all components
pip install -r requirements.txt

# Run tests to verify setup
pytest
```

## 📁 Project Structure

```
Error-Fingerprint/
├── efp-opensource/
│   ├── efp-lite/          # Self-hostable engine
│   ├── efp-fixtures/      # 5,212 labeled errors
│   └── README.md          # Main documentation
├── api/                   # API implementation
├── fingerprint/           # Core engine
├── middleware/            # Auth & rate limiting
└── models/               # Data schemas
```

## 🎯 How to Contribute

### 1. Adding Language Support to efp-lite

**Location:** `efp-opensource/efp-lite/src/efp_lite/languages/`

**Steps:**
1. Create new language file: `{language}.py`
2. Implement the `LanguageParser` interface
3. Add language to `PARSERS` list in `engine.py`
4. Write comprehensive tests
5. Ensure 95% accuracy on relevant fixtures

**Example:**
```python
# efp-lite/src/efp_lite/languages/rust.py
from .base import LanguageParser

class RustParser(LanguageParser):
    def extract_language_specific(self, error: str) -> dict:
        # Extract Rust-specific patterns
        return {
            "language": "rust",
            "patterns": self._extract_rust_patterns(error)
        }
    
    def _extract_rust_patterns(self, error: str) -> list:
        # Implement Rust-specific parsing logic
        pass
```

### 2. Adding Error Fixtures

**Location:** `efp-opensource/efp-fixtures/data/{language}.jsonl`

**Guidelines:**
- Only use **real production errors** (no synthetic examples)
- Replace dynamic values with placeholders:
  - UUIDs → `{uuid}`
  - IPs → `{ip}`
  - Timestamps → `{timestamp}`
  - File paths → `{path}`
  - Line numbers → `{line}`
- Follow existing schema exactly
- Include stack traces when available

**Schema:**
```json
{
  "message": "TypeError: Cannot read properties of undefined (reading 'id')",
  "language": "javascript",
  "category": "null_reference",
  "severity": "error",
  "template": "Cannot read properties of {type} (reading '{property}')",
  "variables": {
    "type": "undefined",
    "property": "id"
  },
  "framework": "express",
  "source_file": "user.controller.js",
  "confidence": 0.95
}
```

### 3. Improving Core Engine

**Location:** `fingerprint/` directory

**Areas for improvement:**
- Language detection accuracy
- Framework detection patterns
- Noise reduction algorithms
- Template generation
- Performance optimization

**Testing Requirements:**
- All existing tests must pass
- New tests for added functionality
- Performance benchmarks
- Cross-language compatibility

### 4. Documentation

**Types of contributions:**
- README improvements
- API documentation
- Code comments
- Example implementations
- Tutorial content

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific component tests
pytest efp-opensource/efp-lite/tests/
pytest efp-opensource/efp-fixtures/tests/

# Run with coverage
pytest --cov=fingerprint --cov-report=html
```

### Test Requirements
- **efp-lite**: Must achieve 95% accuracy on relevant fixtures
- **efp-fixtures**: All fixtures must validate against schema
- **Core engine**: All fingerprint tests must be deterministic

### Performance Benchmarks
```bash
# Run performance tests
pytest tests/performance/

# Expected benchmarks:
# - Single fingerprint: <8ms (p99)
# - Batch processing: >1000 fingerprints/second
# - Memory usage: <50MB for 10K concurrent requests
```

## 📝 Development Workflow

### 1. Create Issue
- Discuss changes in an issue first
- Get feedback from maintainers
- Reference relevant issues in PR

### 2. Branch Naming
```bash
# Feature branches
git checkout -b feature/add-rust-support

# Bug fixes
git checkout -b fix/regex-pattern-issue

# Documentation
git checkout -b docs/update-readme
```

### 3. Making Changes
```bash
# Make your changes
# ... work on your feature ...

# Run tests
pytest

# Format code
black .
isort .

# Lint
flake8 .
mypy .
```

### 4. Submitting PR
- Fill out PR template completely
- Link to relevant issues
- Include test results
- Add documentation if needed

## 🔍 Code Review Process

### Review Criteria
1. **Functionality**: Does it work as intended?
2. **Testing**: Are tests comprehensive?
3. **Performance**: Does it meet benchmarks?
4. **Documentation**: Is it well documented?
5. **Style**: Does it follow coding standards?

### Review Levels
- **Maintainer Review**: Required for all changes
- **Community Review**: Optional but encouraged
- **Automated Checks**: Must pass all CI/CD

## 🏷️ Coding Standards

### Python Style
- Use **Black** for formatting
- Use **isort** for import sorting
- Follow **PEP 8** guidelines
- Type hints required for new code

### Code Quality
- Maximum 80 characters per line
- Meaningful variable names
- Docstrings for all public functions
- Error handling with specific exceptions

### Security
- No hardcoded secrets
- Input validation
- Safe error messages
- Dependency security scanning

## 🐛 Bug Reports

### Reporting Bugs
1. Use GitHub issue template
2. Provide minimal reproduction
3. Include environment details
4. Add error logs and stack traces

### Bug Fix Process
1. Reproduce the issue
2. Write failing test
3. Fix the issue
4. Ensure test passes
5. Update documentation

## 💡 Feature Requests

### Requesting Features
1. Check existing issues first
2. Use feature request template
3. Describe use case clearly
4. Consider implementation complexity

### Feature Implementation
1. Get approval from maintainers
2. Design solution first
3. Implement incrementally
4. Add comprehensive tests

## 🌟 Recognition

### Contributor Credits
- GitHub contributors list
- README acknowledgments
- Release notes
- Community spotlight

### Maintainer Criteria
- Consistent quality contributions
- Code review participation
- Community support
- Project vision alignment

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: conduct@errorfingerprint.dev (Code of Conduct issues)

### Resources
- [API Documentation](https://errorfingerprint.dev/docs)
- [efp-lite Guide](https://errorfingerprint.dev/lite)
- [Fixture Dataset Info](https://errorfingerprint.dev/fixtures)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community Guidelines

### Be Respectful
- Welcome newcomers
- Assume good faith
- Provide constructive feedback
- Celebrate contributions

### Stay Focused
- Keep discussions on-topic
- Use appropriate channels
- Follow issue templates
- Search before asking

### Learn and Teach
- Share knowledge
- Ask questions
- Document discoveries
- Mentor others

---

Thank you for contributing to Error Fingerprint! 🎉

Every contribution, no matter how small, helps make error handling better for everyone.
