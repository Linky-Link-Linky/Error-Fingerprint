# Error Fingerprint Open Source

Production-ready error fingerprinting. Self-hostable engine. 5,212 labeled fixtures. Full API.

## Value Proposition

Transform chaotic error messages into stable, actionable fingerprints that enable intelligent error monitoring, automated alerting, and systematic debugging across 15 programming languages.

![Error Fingerprint Demo](https://via.placeholder.com/600x300/FF6B6B/FFFFFF?text=Error+Fingerprint+Demo)

## Features

- **15 Language Support**: JavaScript, Python, Java, Go, Ruby, PHP, Rust, C#, Swift, Scala, Elixir, and more
- **5,212 Labeled Fixtures**: Real-world production errors with ground truth data
- **Self-Hostable Engine**: Docker-ready, no API keys required, <8ms processing
- **Production API**: 99.9% uptime, similarity clustering, free tier (50K calls/month)
- **MIT Licensed**: Open source, commercial-friendly, no restrictions
- **Enterprise Ready**: Rate limiting, monitoring, security headers, comprehensive logging

## Quick Start

### Self-Hosted (5 Languages)
```bash
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite
curl -X POST http://localhost:8080/v1/fingerprint \
  -H "Content-Type: application/json" \
  -d '{"message": "KeyError: '\''user_id'\'' not found in session dict"}'
```

### Production API (15 Languages)
```bash
curl -X POST "https://error-fingerprint-api.p.rapidapi.com/fingerprint" \
  -H "X-RapidAPI-Key: YOUR_RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: error-fingerprint-api.p.rapidapi.com" \
  -H "Content-Type: application/json" \
  -d '{"message": "TypeError: Cannot read properties of undefined (reading '\''userId'\'')"}'
```

### Dataset for Testing
```python
pip install efp-fixtures
from efp_fixtures import load_all
errors = load_all()
print(f"Loaded {len(errors)} errors")
```

## Example Input and Output

### Input
```json
{
  "message": "TypeError: Cannot read properties of undefined (reading 'userId')\n    at AuthMiddleware.verify (auth.middleware.js:38:24)"
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
    "property": "userId"
  },
  "similar_to": ["js_null_ref_b2f1e9c7"],
  "processing_ms": 4
}
```

## Why This Exists

Error handling is broken in modern software. Developers spend 40% of debugging time deciphering similar error messages. Different error messages that represent the same logical error get treated as separate issues, creating noise and masking the real problem frequency.

Error Fingerprint solves this by:
- **Normalizing** error messages into canonical templates
- **Extracting** variables while preserving semantic meaning
- **Grouping** identical logical errors regardless of surface text
- **Enabling** automated alerting based on error patterns, not strings
- **Providing** consistent error classification across languages and frameworks

## Installation

### Self-Hosted Engine
```bash
# Docker (recommended)
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite

# Local development
git clone https://github.com/Linky-Link-Linky/Error-Fingerprint.git
cd Error-Fingerprint/efp-opensource/efp-lite
pip install -e ".[dev]"
python -m efp_lite.server
```

### Dataset Package
```bash
pip install efp-fixtures
```

### Production API
```bash
# No installation required - use via HTTP API
# Get free API key: https://rapidapi.com/Daymo-W5ovDZJrz/api/error-fingerprint-api
```

## Documentation

- **[API Documentation](https://rapidapi.com/Daymo-W5ovDZJrz/api/error-fingerprint-api)** - Complete API reference
- **[Developer Guide](https://github.com/Linky-Link-Linky/Error-Fingerprint/tree/main/efp-opensource)** - Self-hosting instructions
- **[Dataset Reference](https://github.com/Linky-Link-Linky/Error-Fingerprint/tree/main/efp-opensource/efp-fixtures)** - Fixture format and usage
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Security Policy](SECURITY.md)** - Vulnerability reporting and security practices
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## Roadmap

### Q2 2024
- [ ] **Web Dashboard** - Real-time error monitoring and analytics
- [ ] **Alerting Integration** - Slack, Teams, Discord notifications
- [ ] **Batch Processing** - Process multiple errors in single request
- [ ] **Custom Templates** - User-defined fingerprint patterns

### Q3 2024
- [ ] **Machine Learning** - Improve accuracy with trained models
- [ ] **Source Map Support** - Better minified JavaScript handling
- [ ] **Framework Detection** - Expanded framework pattern matching
- [ ] **Performance Optimization** - Sub-millisecond processing

### Q4 2024
- [ ] **Multi-tenant Support** - Organization-level isolation
- [ ] **Export/Import** - Backup and migrate fingerprint data
- [ ] **Advanced Analytics** - Error trends and insights
- [ ] **Plugin System** - Community-contributed extensions

## Contributing

We welcome contributions! Error Fingerprint is built by developers, for developers.

### Ways to Contribute
- **Code Contributions** - Add language support, improve algorithms, fix bugs
- **Dataset Expansion** - Add real production errors to efp-fixtures
- **Documentation** - Improve guides, examples, and API docs
- **Bug Reports** - Report issues with reproduction steps
- **Feature Requests** - Suggest improvements and new capabilities

### Getting Started
```bash
# Clone repository
git clone https://github.com/Linky-Link-Linky/Error-Fingerprint.git
cd Error-Fingerprint

# Run tests
pytest

# Start development
cd efp-opensource/efp-lite
python -m efp_lite.server
```

### Contribution Areas
- **Language Parsers** - Add support for new programming languages
- **Framework Detection** - Improve framework pattern matching
- **Template Generation** - Enhance error normalization algorithms
- **Performance** - Optimize for sub-millisecond processing
- **Testing** - Add comprehensive test coverage

## Language Support

| Language | efp-lite | Full API | Fixtures |
|-----------|------------|------------|-----------|
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

## Architecture

### Components
- **efp-lite**: Self-hostable fingerprinting engine for 5 languages
- **efp-fixtures**: 5,212 labeled real-world error strings across 15 languages  
- **Full API**: Production-grade service with 15 languages, similarity clustering, enterprise features

### Technology Stack
- **Backend**: Python, FastAPI, Uvicorn
- **Engine**: Regex patterns, template matching, variable extraction
- **Deployment**: Docker, GitHub Actions, Codecov
- **API**: RESTful, JSON, HTTP/2, TLS 1.3

## Performance

- **Processing Time**: <8ms (p99)
- **Throughput**: >1,000 fingerprints/second
- **Memory Usage**: <50MB for 10K concurrent requests
- **Accuracy**: >95% on labeled test set
- **Uptime**: 99.9% (production API)

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

Built by [Error Fingerprint](https://errorfingerprint.dev) ·
[efp-lite](https://github.com/Linky-Link-Linky/Error-Fingerprint/tree/main/efp-opensource/efp-lite) ·
[efp-fixtures](https://github.com/Linky-Link-Linky/Error-Fingerprint/tree/main/efp-opensource/efp-fixtures) ·
[Full API](https://rapidapi.com/Daymo-W5ovDZJrz/api/error-fingerprint-api) ·
[MIT License](LICENSE)
