# Error Fingerprint Open Source

Normalize any error message into a stable fingerprint across 15 programming languages.

## One Line Value Proposition

Production-ready error fingerprinting with three components: self-hostable engine, comprehensive dataset, and managed API.

## Features

- **efp-lite**: Self-hostable engine for 5 languages (JavaScript, Python, Java, Go, Generic)
- **efp-fixtures**: 5,212 labeled real-world error strings across 15 languages
- **Full API**: Production-grade service with 15 languages, <8ms p99, 99.9% uptime
- **Docker-ready**: One-command deployment for self-hosting
- **MIT Licensed**: Open source with permissive licensing
- **Enterprise Features**: Similarity clustering, rate limiting, monitoring

## Quick Start

### Self-Host with efp-lite (5 Languages)

```bash
# Pull and run engine
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite

# Test it works
curl -X POST http://localhost:8080/v1/fingerprint \
  -H "Content-Type: application/json" \
  -d '{"message": "KeyError: '\''user_id'\'' not found in session dict"}'
```

### Use Full API via RapidAPI (15 Languages)

```bash
# Get your free API key (no credit card required)
# Visit: https://rapidapi.com/Daymo-W5ovDZJrz/api/error-fingerprint-api

# Use the API
curl -X POST "https://error-fingerprint-api.p.rapidapi.com/fingerprint" \
  -H "X-RapidAPI-Key: YOUR_RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: error-fingerprint-api.p.rapidapi.com" \
  -H "Content-Type: application/json" \
  -d '{"message": "TypeError: Cannot read properties of undefined (reading '\''userId'\'')\n    at AuthMiddleware.verify (auth.middleware.js:38:24)"}'
```

### Use Dataset for Testing/Training

```python
# Install the dataset
pip install efp-fixtures

# Load all 5,212 errors
from efp_fixtures import load_all
errors = load_all()

# Load specific languages
python_errors = load_language("python")
network_errors = load_category("network_error")

print(f"Loaded {len(errors)} total errors")
print(f"Python errors: {len(python_errors)}")
```

## Example Input and Output

### Input
```json
{
  "message": "TypeError: Cannot read properties of undefined (reading 'id')"
}
```

### Output
```json
{
  "fingerprint": "js_null_ref_a3f2c1d8",
  "template": "Cannot read properties of {type} (reading '{property}')",
  "language": "javascript",
  "framework": "express",
  "category": "null_reference",
  "severity": "error",
  "variables": {
    "type": "undefined",
    "property": "id"
  },
  "similar_to": ["js_null_ref_b2f1e9c7"],
  "processing_ms": 4
}
```

## Why This Exists

Error messages are inconsistent across programming languages, frameworks, and even different instances of the same error. This makes debugging, monitoring, and error analysis difficult.

Error Fingerprint solves this by:
- **Normalizing** any error message into a stable fingerprint
- **Extracting** dynamic variables (IDs, file paths, line numbers)
- **Generating** canonical templates for error classification
- **Supporting** 15 programming languages and 20+ frameworks
- **Providing** similarity clustering for related errors
- **Processing** in <8ms with 99.9% uptime

## Installation

### Option 1: Self-Hosted Engine

```bash
# Docker (recommended)
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite

# Local Python
git clone https://github.com/Linky-Link-Linky/Error-Fingerprint.git
cd Error-Fingerprint/efp-opensource/efp-lite
pip install -e .
python -m efp_lite.server
```

### Option 2: Dataset Package

```bash
# Install from PyPI
pip install efp-fixtures

# Install from source
git clone https://github.com/Linky-Link-Linky/Error-Fingerprint.git
cd Error-Fingerprint/efp-opensource/efp-fixtures
pip install -e .
```

### Option 3: Full API

```bash
# Visit RapidAPI marketplace
https://rapidapi.com/Daymo-W5ovDZJrz/api/error-fingerprint-api

# Get free API key (50,000 requests/month, no credit card)
```

## Documentation

- **API Documentation**: https://errorfingerprint.dev/docs
- **efp-lite Guide**: https://errorfingerprint.dev/lite
- **Dataset Documentation**: https://errorfingerprint.dev/fixtures
- **GitHub Repository**: https://github.com/Linky-Link-Linky/Error-Fingerprint
- **Issues & Discussions**: https://github.com/Linky-Link-Linky/Error-Fingerprint/discussions

## Roadmap

### Current Status
- efp-lite: Stable v0.1.0 with 5 languages
- efp-fixtures: 5,212 labeled errors across 15 languages
- Full API: Production-ready with RapidAPI integration

### Upcoming Features
- **Additional Languages**: Ruby, PHP, Rust, C#, Swift, Scala, Elixir in efp-lite
- **Enhanced Similarity**: Machine learning-based clustering
- **Source Map Support**: JavaScript source map resolution
- **Batch Processing**: Multiple errors in single request
- **Web Dashboard**: Real-time monitoring and analytics
- **Enterprise Features**: SSO, audit logs, custom models

### Contributing to Roadmap
- Feature requests: GitHub Issues with "enhancement" label
- Bug reports: GitHub Issues with "bug" label
- Discussions: GitHub Discussions for ideas and feedback

## Contributing

We welcome contributions to all three components:

### efp-lite (Self-Hostable Engine)
- Add new language support by implementing `LanguageParser` interface
- Improve existing language parsers for better accuracy
- Add new framework detection patterns
- Optimize performance and memory usage
- Write comprehensive tests (95% accuracy required)

### efp-fixtures (Dataset)
- Add real production error strings to appropriate `.jsonl` files
- Replace dynamic values with placeholders (`{uuid}`, `{ip}`, `{timestamp}`)
- Follow existing schema exactly
- Validate fixtures with test suite
- Do not submit synthetic examples or Stack Overflow snippets

### Infrastructure
- Improve CI/CD pipeline and testing
- Enhance documentation and examples
- Add new GitHub Actions workflows
- Improve Docker images and deployment
- Add security scanning and dependency updates

### Development Workflow
```bash
# Clone the repository
git clone https://github.com/Linky-Link-Linky/Error-Fingerprint.git
cd Error-Fingerprint

# Run tests for all components
pytest

# Start efp-lite locally
cd efp-opensource/efp-lite
python -m efp_lite.server

# Validate fixtures
cd efp-opensource/efp-fixtures
pytest tests/
```

### Code Standards
- Use Black for code formatting
- Follow PEP 8 guidelines
- Add type hints for new code
- Write comprehensive docstrings
- Include error handling and logging

### Community
- Join discussions at https://github.com/Linky-Link-Linky/Error-Fingerprint/discussions
- Report bugs at https://github.com/Linky-Link-Linky/Error-Fingerprint/issues
- Request features at https://github.com/Linky-Link-Linky/Error-Fingerprint/issues/new?template=feature_request
- Review contributions and provide feedback

---

## Language Support

| Language | efp-lite | Full API | Fixtures |
|-----------|-----------|-----------|-----------|
| JavaScript / Node.js | ✓ | ✓ | ✓ |
| Python | ✓ | ✓ | ✓ |
| Java / Kotlin | ✓ | ✓ | ✓ |
| Go | ✓ | ✓ | ✓ |
| Ruby | — | ✓ | ✓ |
| PHP | — | ✓ | ✓ |
| Rust | — | ✓ | ✓ |
| C# | — | ✓ | ✓ |
| Swift | — | ✓ | ✓ |
| Scala | — | ✓ | ✓ |
| Elixir | — | ✓ | ✓ |
| Generic (any) | ✓ | ✓ | ✓ |

## Choose Your Path

| Use Case | Recommended Option | Why |
|----------|-------------------|-----|
| Personal Projects | efp-lite | Free, no API keys, 5 common languages |
| Side Projects | efp-lite | Docker-ready, fast, self-hosted |
| Production Apps | Full API | 15 languages, 99.9% uptime, similarity clustering |
| Error Parser Development | efp-fixtures | 5,212 labeled examples, ground truth data |
| Learning/Research | All Components | Study algorithms, contribute to open source |

---

Built by [Error Fingerprint](https://errorfingerprint.dev) ·
[efp-lite](https://github.com/Linky-Link-Linky/Error-Fingerprint/tree/main/efp-opensource/efp-lite) ·
[efp-fixtures](https://github.com/Linky-Link-Linky/Error-Fingerprint/tree/main/efp-opensource/efp-fixtures) ·
[Full API](https://rapidapi.com/Daymo-W5ovDZJrz/api/error-fingerprint-api) ·
[MIT License](https://github.com/Linky-Link-Linky/Error-Fingerprint/blob/main/efp-opensource/LICENSE)
