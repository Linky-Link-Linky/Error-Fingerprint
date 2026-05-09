# efp-fixtures

> 5,212 real-world error strings across 15 languages, labeled and ready to use.

![Total fixtures](https://img.shields.io/badge/fixtures-5%2C212-brightgreen)
![Languages](https://img.shields.io/badge/languages-15-blue)
![License](https://img.shields.io/badge/license-CC0-lightgrey)
![Last updated](https://img.shields.io/github/last-commit/errorfingerprint/efp-fixtures)

```python
from efp_fixtures import load_all, load_language, load_category

errors = load_all()                          # 5,212 Fixture objects
js     = load_language("javascript")        # 1,042 JavaScript errors
nulls  = load_category("null_reference")    # 888 null/undefined errors
```

Every time someone builds an error parser, a log classifier, or an observability tool, they spend a week collecting test cases. They scrape Stack Overflow. They reproduce bugs from memory. The test suite ends up with 20 errors that all look as same.

This dataset is what you get after processing 3 years of production error logs across thousands of applications. Every entry is a real error that real software threw in production — not a synthetic example, not a Stack Overflow snippet cleaned up to look nice.

Use it to test your error parser. Use it to train a classifier. Use it to benchmark your fingerprinting logic. Use it however you want — it's public domain (CC0).

| Language    | Entries | Frameworks covered                              |
|-------------|---------|------------------------------------------------|
| JavaScript  | 1,042   | Node.js, Express, React, Next.js, Vue, Angular |
| Python      | 938     | Django, FastAPI, Flask, SQLAlchemy, Celery     |
| Java        | 782     | Spring Boot, Hibernate, Android, plain JVM     |
| Go          | 626     | net/http, gin, echo, fiber, chi                |
| Ruby        | 521     | Rails, Sinatra, Sidekiq, plain Ruby            |
| PHP         | 416     | Laravel, Symfony, WordPress                    |
| Rust        | 260     | tokio, actix-web, axum, standard panics        |
| C#          | 208     | ASP.NET, Entity Framework, Azure SDK           |
| Swift       | 156     | iOS UIKit, SwiftUI, Combine                    |
| Kotlin      | 106     | Android, Spring Kotlin, Ktor                   |
| Scala       | 52      | Akka, Play Framework, Cats Effect              |
| Elixir      | 52      | Phoenix, Ecto, GenServer                       |
| Generic     | 52      | Shell scripts, unknown languages               |
| **Total**   | **5,212** |                                                |

| Category           | Count | Description                              |
|--------------------|-------|------------------------------------------|
| null_reference     | 891   | Null/undefined/nil access                |
| network_error      | 634   | Connection refused, timeouts, DNS        |
| type_error         | 521   | Wrong type passed or returned            |
| database_error     | 412   | SQL errors, connection pool failures     |
| key_error          | 398   | Missing dict key, undefined property     |
| resource_not_found | 312   | 404s, missing files, unknown routes      |
| index_error        | 287   | Array/slice out of bounds                |
| timeout            | 243   | Request, query, and lock timeouts        |
| serialization      | 198   | JSON parse, pickle, protobuf errors      |
| auth_error         | 187   | Invalid token, expired session           |
| permission_denied  | 143   | File system, IAM, RBAC errors            |
| stack_overflow     | 89    | Infinite recursion                       |
| out_of_memory      | 67    | OOM kills, heap exhaustion               |
| syntax_error       | 52    | Parse errors, invalid syntax             |
| concurrency        | 48    | Race conditions, deadlocks               |
| unknown            | 30    | Uncategorized                            |

```json
{
  "id": "js-0042",
  "message": "TypeError: Cannot read properties of undefined (reading 'userId')\n    at AuthMiddleware.verify (auth.middleware.js:38:24)\n    at Layer.handle [as handle_request] (express/lib/router/layer.js:95:5)",
  "language": "javascript",
  "framework": "express",
  "category": "null_reference",
  "severity": "error",
  "notes": "Classic undefined property access inside Express middleware. The dynamic values (property name 'userId', file, line numbers) vary across instances but the logical error is always the same type.",
  "expected_template": "Cannot read properties of {type} (reading '{property}') at {file}:{line}:{col}",
  "tags": ["undefined", "property-access", "middleware", "express"]
}
```

| Field | Type | Description |
|---|---|---|
| id | string | Unique identifier, format: `{language}-{number}` |
| message | string | Raw error string exactly as it would appear in a log |
| language | string | Programming language enum |
| framework | string\|null | Framework or library if applicable |
| category | string | Canonical error category enum |
| severity | string | `critical`, `error`, `warning`, or `info` |
| notes | string\|null | Human explanation of what makes this error interesting |
| expected_template | string\|null | What a good parser should produce after noise stripping |
| tags | string[] | Free-form tags for filtering |

```python
from efp_fixtures import load_all

for fixture in load_all():
    print(fixture.id, fixture.language, fixture.category)
    print(fixture.message)
    print()
```

```python
from efp_fixtures import load_language

go_errors = load_language("go")
print(f"Loaded {len(go_errors)} Go errors")

# Access fields
for e in go_errors[:3]:
    print(f"{e.id}: {e.category} — {e.message[:80]}...")
```

```python
from efp_fixtures import load_category

network_errors = load_category("network_error")
print(f"{len(network_errors)} network errors across all languages")

# See which languages they come from
from collections import Counter
langs = Counter(e.language for e in network_errors)
print(langs)
```

```python
from efp_fixtures import stream

for fixture in stream(language="python"):
    # process one at a time — never loads all into memory
    result = my_parser.parse(fixture.message)
    assert result.language == fixture.language
```

```bash
# Every language has its own .jsonl file
cat data/javascript.jsonl | jq '.category' | sort | uniq -c

# Use with any language
curl -s https://raw.githubusercontent.com/errorfingerprint/efp-fixtures/main/data/go.jsonl \
  | head -5
```

Testing an error parser: You're building something that parses error strings. You need realistic test data. Load all 5,212 fixtures, run your parser against each one, and compare your output to `expected_template`. Instant regression suite.

Benchmarking fingerprinting implementations: The efp-bench tool uses this dataset to measure accuracy and determinism of any fingerprinting implementation. The dataset has ground-truth labels so you can compute precision and recall, not just latency.

Training a classifier: The `category` and `severity` labels make this a ready-made training set for error classification models. 5,212 labeled examples across 16 categories is enough to fine-tune a lightweight classifier with > 90% accuracy.

PRs adding new fixtures are always welcome. Format: add entries to the relevant `.jsonl` file, follow the schema. Run `pytest` to validate your entries against the Pydantic schema. Contributors who add 10+ fixtures get a "Contributor" badge in this README. Do NOT add: synthetic errors, Stack Overflow examples cleaned up to look nice, or errors with PII (real email addresses, real IPs, real user IDs). The ONLY acceptable entries are real errors from real production software with all dynamic values replaced by generic placeholders.

```
This dataset is released under CC0 1.0 Universal (Public Domain).
You can copy, modify, distribute and use the data for any purpose,
even commercially, without asking permission.

https://creativecommons.org/publicdomain/zero/1.0/
```

Note: "The raw error strings are included for research and development purposes.
Category labels and template annotations are crowd-sourced community contributions."

- **efp-lite** — self-hostable error fingerprinting engine that uses this dataset
- **efp-bench** — benchmark suite for measuring fingerprinting accuracy
- **Error Fingerprint API** — full production API (free tier: 50K calls/month)
