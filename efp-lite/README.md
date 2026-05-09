# efp-lite

> Self-hostable error fingerprinting. Same logical error, always gets same ID.

![License](https://img.shields.io/badge/license-MIT-blue)
![Docker](https://img.shields.io/badge/docker-ghcr.io%2Ferrorfingerprint%2Fefp--lite-blue)
![Languages](https://img.shields.io/badge/languages-5-green)
![CI](https://img.shields.io/github/actions/workflow/status/errorfingerprint/efp-lite/ci.yml)

```bash
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite
```

```bash
curl -X POST http://localhost:8080/v1/fingerprint \
  -H "Content-Type: application/json" \
  -d '{"message": "TypeError: Cannot read properties of undefined (reading '\''id'\'')"}'
```

```json
{
  "fingerprint": "js_null_ref_a3f2c1d8",
  "template": "Cannot read properties of {type} (reading '{property}')",
  "language": "javascript",
  "category": "null_reference",
  "severity": "error",
  "variables": { "type": "undefined", "property": "id" },
  "similar_to": null,
  "processing_ms": 6
}
```

The alert storm problem. Your app threw the same error 10,000 times overnight. Different user IDs, different request paths, different timestamps. Your log aggregator shows 10,000 individual log lines. Your on-call engineer gets 10,000 Slack notifications. They are not having a good morning.

Error fingerprinting strips the dynamic parts — the IDs, the timestamps, the paths — and generates a stable ID for the underlying error pattern. Those 10,000 alerts collapse into one. You route it once. You fix it once. You sleep.

You could write a regex to strip numbers. It would work for your one error. Then you'd need another regex for UUIDs. Then one for file paths. Then one for IP addresses. Then one for JWT tokens. Sentry has been building this list for 9 years. There is no weekend project that catches all of the edge cases across 15 languages.

efp-lite gives you a correct noise-stripping pipeline for 5 languages that you can run yourself, for free, with one Docker command. No API key. No rate limits. No vendor lock-in. If you hit the limits of what it handles, there is a fully managed API that picks up where this leaves off.

**Path 1 — Docker (recommended):**
```bash
# Pull and run
docker run -p 8080:8080 ghcr.io/errorfingerprint/efp-lite

# Test it
curl -X POST http://localhost:8080/v1/fingerprint \
  -H "Content-Type: application/json" \
  -d '{"message": "panic: runtime error: index out of range [3] with length 2"}'
```

**Path 2 — Docker Compose (for existing docker-compose projects):**
```yaml
# docker-compose.yml
services:
  efp-lite:
    image: ghcr.io/errorfingerprint/efp-lite
    ports:
      - "8080:8080"
```
```bash
docker-compose up -d efp-lite
```

**Path 3 — pip (for Python projects):**
```bash
pip install efp-lite
efp-lite serve --port 8080
```

**POST /v1/fingerprint**

Request:
```json
{
  "message": "string (required) — raw error string or full stack trace, max 32,000 chars",
  "context": {
    "language": "string (optional) — hint: javascript | python | java | go | generic",
    "framework": "string (optional) — hint: express | django | spring | gin"
  }
}
```

Response fields table:

| Field | Type | Description |
|---|---|---|
| fingerprint | string | Stable ID for this error pattern. Format: `{lang}_{category}_{hash}` |
| template | string | The error message with dynamic values replaced by `{placeholders}` |
| language | string | Detected or provided language |
| framework | string\|null | Detected or provided framework |
| category | string | One of 16 canonical error categories |
| severity | string | `critical`, `error`, `warning`, or `info` |
| variables | object | The dynamic values that were extracted during noise stripping |
| similar_to | null | Always null in efp-lite. Available in the full API. |
| processing_ms | int | Time taken to process this request |

Fingerprint stability guarantee: The same logical error — same error type, same message structure — will always produce the same fingerprint, regardless of the values of `variables`. This is the core contract. If two fingerprints differ, the errors are logically different. If they match, they are the same underlying problem.

**GET /health**
```json
{"status": "ok", "version": "0.1.0", "mode": "lite"}
```

**Supported (returns accurate fingerprint):**

| Language | Auto-detected | Notes |
|---|---|---|
| JavaScript / Node.js | ✓ | V8 and SpiderMonkey stack traces |
| Python | ✓ | Full tracebacks, chained exceptions |
| Java / Kotlin | ✓ | `caused by` chains, Spring/Android |
| Go | ✓ | Goroutine panics, `runtime error:` |
| Generic | ✓ (fallback) | Any language — noise stripping only |

**Not supported in efp-lite (use the full API):**

| Language | Why it's hard |
|---|---|
| Ruby | `.rb:N:in` trace format + Rails-specific exception hierarchy |
| PHP | Fatal errors vs exceptions vs warnings behave differently |
| Rust | Panic messages vary significantly by build mode |
| C# | Inner exception chains need deep parsing |
| Swift | Crash reports vs runtime errors are different formats |
| Scala | Akka actor paths look like noise but aren't |
| Elixir | GenServer crash reports have their own structure |

efp-lite is a correct, fast implementation for the common case. It is not a drop-in replacement for the full EFP API. The things it does not do are not oversights — they are deliberate scope limits that keep the codebase small enough to read in an afternoon.

| Feature                         | efp-lite  | Full API  |
|---------------------------------|-----------|-----------|
| JavaScript / Python / Java / Go | ✓         | ✓         |
| Ruby, PHP, Rust, C#             | ✗         | ✓         |
| Swift, Scala, Elixir            | ✗         | ✓         |
| Minified JS stack traces        | ✗         | ✓         |
| Source map resolution           | ✗         | ✓         |
| Similarity clustering           | ✗         | ✓         |
| Obfuscated path normalization   | ✗         | ✓         |
| p99 latency                     | < 20ms    | < 8ms     |
| Rate limiting                   | None      | 10K/min   |
| Uptime SLA                      | None      | 99.9%     |
| Support                         | GitHub issues | Email + Slack |

If you need anything in the right column, the full API has a free tier at 50K calls/month — no credit card required.

version: "3.9"
services:
  efp-lite:
    image: ghcr.io/errorfingerprint/efp-lite
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      - WORKERS=4
      - LOG_LEVEL=warning
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 128M
```

efp-lite and the full API share the same request/response contract. Migrating is a one-line change:

```python
# Before (efp-lite self-hosted)
BASE_URL = "http://localhost:8080"

# After (full API)
BASE_URL = "https://api.errorfingerprint.dev"
# Add header: X-API-Key: efp_your_key_here
```

That is the entire migration. Fingerprint IDs are stable across both — the algorithm is the same, so `js_null_ref_a3f2c1d8` in efp-lite will always be `js_null_ref_a3f2c1d8` in the full API.

Sign up for a free tier key (50K calls/month, no credit card):
`https://errorfingerprint.dev` 

How to run tests: `pytest` 
How to add support for a new language: create `src/efp_lite/languages/{lang}.py`, implement the `LanguageParser` interface, add to `PARSERS` list in `engine.py` 
The test requirement: any new language parser must pass 95% of the relevant efp-fixtures entries for that language
PRs welcome for: new language parsers, edge case fixes, performance improvements
PRs not accepted for: similarity clustering, source map resolution (these are features of the full API, not efp-lite)

MIT License — Copyright (c) 2025 Error Fingerprint
