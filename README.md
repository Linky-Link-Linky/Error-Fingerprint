# Error Fingerprint Open Source

> Production-ready error fingerprinting. Self-hostable engine. 5,212 labeled fixtures. Full API.

![License](https://img.shields.io/badge/license-MIT-blue)
![efp-lite](https://img.shields.io/badge/efp--lite-self--hostable-green)
![Fixtures](https://img.shields.io/badge/fixtures-5%2C212-brightgreen)
![Languages](https://img.shields.io/badge/languages-15-blue)
![CI](https://img.shields.io/github/actions/workflow/status/errorfingerprint/efp-opensource/ci.yml)

```bash
# Self-hostable engine for 5 languages
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite

# Full API with 15 languages
curl -X POST https://api.errorfingerprint.dev/v1/fingerprint \
  -H "Content-Type: application/json" \
  -d '{"message": "TypeError: Cannot read properties of undefined (reading '\''id'\'')"}'

# Dataset for testing and training
pip install efp-fixtures
python -c "from efp_fixtures import load_all; print(len(load_all()), 'errors loaded')"
```

This is the open source organization for Error Fingerprint. We provide three components that work together: a self-hostable engine for developers who want to run it themselves, a comprehensive dataset of real-world errors for testing and training, and a fully managed API for production use cases.

| Component | What it is | Start here if... |
|-----------|------------|------------------|
| [efp-lite](https://github.com/errorfingerprint/efp-lite) | Self-hostable fingerprinting engine for 5 languages. One Docker command. | You want to run it yourself, free, no API key |
| [efp-fixtures](https://github.com/errorfingerprint/efp-fixtures) | 5,212 labeled real-world error strings across 15 languages | You're building or testing an error parser |
| [Error Fingerprint API](https://errorfingerprint.dev) | Fully managed API. 15 languages. < 8ms p99. Free tier. | You want 15 languages, similarity clustering, and 99.9% uptime |

Choose efp-lite if you are a solo developer or running a side project. It handles the 5 most common languages (JavaScript, Python, Java, Go, Generic) with one Docker command and no API key required. The engine is stateless, fast, and produces the same stable fingerprints as the full API.

Choose efp-fixtures if you are building your own error parsing or fingerprinting logic. The dataset contains 5,212 real production errors across 15 languages, each labeled with correct category, severity, and canonical template. Use it as your test suite to ensure your parser works correctly across all edge cases.

Choose the full API if you are running production software at scale. It supports all 15 languages, handles minified JavaScript, provides similarity clustering, and includes 99.9% uptime SLA. The free tier offers 50,000 calls per month with no credit card required.

## Language support

| Language     | efp-lite | Full API | Fixtures |
|--------------|----------|----------|-----------|
| JavaScript / Node.js | ✓ | ✓ | ✓ |
| Python       | ✓        | ✓        | ✓        |
| Java / Kotlin| ✓        | ✓        | ✓        |
| Go           | ✓        | ✓        | ✓        |
| Ruby         | —        | ✓        | ✓        |
| PHP          | —        | ✓        | ✓        |
| Rust         | —        | ✓        | ✓        |
| C#           | —        | ✓        | ✓        |
| Swift        | —        | ✓        | ✓        |
| Scala        | —        | ✓        | ✓        |
| Elixir       | —        | ✓        | ✓        |
| Generic (any)| ✓        | ✓        | ✓        |

## Quick start examples

**Self-host with efp-lite:**
```bash
# Pull and run the engine
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite

# Test it works
curl -X POST http://localhost:8080/v1/fingerprint \
  -H "Content-Type: application/json" \
  -d '{"message": "KeyError: '\''user_id'\'' not found in session dict"}'
```

**Use the full API:**
```bash
# Sign up for free API key (no credit card)
# Visit: https://errorfingerprint.dev

# Use the API
curl -X POST https://api.errorfingerprint.dev/v1/fingerprint \
  -H "X-API-Key: efp_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"message": "TypeError: Cannot read properties of undefined (reading '\''id'\'')"}'
```

**Load the fixture dataset:**
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

## Architecture

**efp-lite**: A lightweight fingerprinting engine written in Python. Uses regex patterns for language detection, noise stripping for variable extraction, and deterministic SHA256 hashing for fingerprint generation. Designed for self-hosting and small deployments.

**efp-fixtures**: A comprehensive dataset of real-world error strings collected from production systems over 3 years. Each entry is labeled with programming language, error category, severity level, and canonical template. Released under CC0 public domain license.

**Full API**: Production-grade service built on the same algorithm as efp-lite but with extended language support, similarity clustering, source map resolution, and enterprise features. Handles edge cases like minified JavaScript, obfuscated paths, and complex exception chains.

All three components share the same fingerprinting algorithm, ensuring that the same logical error produces the same fingerprint whether processed by efp-lite, the full API, or your own implementation using the fixtures as ground truth.

## Contributing

We welcome contributions to all three components:

**efp-lite**: Add support for new languages by implementing the `LanguageParser` interface in `src/efp_lite/languages/{lang}.py`. Each new parser must pass 95% of the relevant entries in efp-fixtures for that language.

**efp-fixtures**: Add real production error strings to the appropriate `.jsonl` files. Follow the existing schema and ensure all dynamic values (UUIDs, IPs, timestamps) are replaced with generic placeholders. Do not submit synthetic examples or Stack Overflow snippets.

**Infrastructure**: Help improve CI/CD, documentation, and examples. All three repositories use the same GitHub Actions workflow for testing and validation.

## Development

```bash
# Clone the entire organization
git clone https://github.com/errorfingerprint/efp-opensource.git
cd efp-opensource

# Run tests for all components
pytest

# Start efp-lite locally
cd efp-lite
python -m efp_lite.server

# Validate fixtures
cd efp-fixtures
pytest tests/
```

## License

All components are released under the MIT License. See individual repository LICENSE files for complete terms.

---

Built by [Error Fingerprint](https://errorfingerprint.dev) ·
[efp-lite](https://github.com/errorfingerprint/efp-lite) ·
[efp-fixtures](https://github.com/errorfingerprint/efp-fixtures) ·
[Full API](https://errorfingerprint.dev) ·
[MIT License](https://opensource.org/licenses/MIT)
