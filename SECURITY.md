# Security Policy

## Supported Versions

| Version | Supported | Security Updates |
|---------|-----------|------------------|
| Latest (main branch) | ✅ Yes | ✅ Yes |
| Previous major version | ❌ No | ❌ No |

## Reporting a Vulnerability

### 🚨 Private Disclosure Process

**Do NOT open a public issue for security vulnerabilities!**

Instead, please report vulnerabilities privately to:

- **Email**: security@errorfingerprint.dev
- **PGP Key**: Available upon request

### What to Include in Your Report

Please include the following information in your security report:

1. **Vulnerability Type**
   - Brief description of the vulnerability
   - CVSS score (if known)
   - Attack vector and complexity

2. **Affected Components**
   - Specific version(s) affected
   - Components involved (efp-lite, efp-fixtures, API)
   - Configuration details

3. **Reproduction Steps**
   - Step-by-step reproduction guide
   - Minimal code example
   - Expected vs actual behavior

4. **Impact Assessment**
   - Potential impact on users/data
   - Scope of affected deployments
   - Any mitigations already in place

5. **Proof of Concept**
   - Working exploit or test case
   - Screenshots/logs if applicable
   - Environmental details

### Response Timeline

| Severity Level | Initial Response | Fix Timeline |
|---------------|-----------------|--------------|
| **Critical** | ≤ 24 hours | ≤ 7 days |
| **High** | ≤ 48 hours | ≤ 14 days |
| **Medium** | ≤ 72 hours | ≤ 30 days |
| **Low** | ≤ 5 days | ≤ 60 days |

### Severity Classification

- **Critical**: Remote code execution, privilege escalation, data breach
- **High**: Authentication bypass, injection vulnerabilities, DoS
- **Medium**: Information disclosure, CSRF, XSS
- **Low**: Configuration issues, weak cryptography, minor info leaks

## Security Scope

### In Scope

The following components are covered by this security policy:

#### efp-lite (Self-hostable Engine)
- Language detection algorithms
- Template generation logic
- Docker container security
- Dependency vulnerabilities

#### efp-fixtures (Dataset)
- Data injection vulnerabilities
- Schema validation bypasses
- File parsing security

#### Core API
- Authentication mechanisms
- Input validation
- Error message sanitization
- Rate limiting bypasses

#### Infrastructure
- CI/CD pipeline security
- Supply chain attacks
- Dependency management

### Out of Scope

The following are NOT covered by this security policy:

- Vulnerabilities in third-party dependencies (reported upstream)
- Issues requiring physical access to systems
- Social engineering attacks
- Vulnerabilities in user applications using our API
- Denial of service attacks against the public API (use rate limiting)

## Security Best Practices

### For Users of efp-lite

1. **Container Security**
   ```bash
   # Use non-root user
   docker run --user 1000:1000 ghcr.io/errorfingerprint/efp-lite
   
   # Limit resources
   docker run --memory=512m --cpus=1.0 ghcr.io/errorfingerprint/efp-lite
   
   # Read-only filesystem
   docker run --read-only ghcr.io/errorfingerprint/efp-lite
   ```

2. **Network Security**
   - Bind to localhost only: `-p 127.0.0.1:8080:8080`
   - Use reverse proxy with TLS termination
   - Implement firewall rules

3. **API Keys**
   - Use environment variables, not command line args
   - Rotate keys regularly
   - Use different keys for different environments

### For API Users

1. **API Key Management**
   - Never commit API keys to repositories
   - Use environment variables or secret managers
   - Implement key rotation policies

2. **Input Validation**
   - Sanitize error messages before sending
   - Remove sensitive data (passwords, tokens, PII)
   - Validate response data

3. **Error Handling**
   - Implement retry logic with exponential backoff
   - Handle rate limit responses gracefully
   - Log errors without exposing sensitive data

## Security Features

### Built-in Protections

#### Input Sanitization
- Maximum message length limits (10,000 characters)
- Regex pattern validation
- Unicode normalization

#### Authentication
- HMAC-based API key validation
- Constant-time comparison
- Key format validation

#### Error Handling
- No sensitive data in error messages
- Generic error responses
- Request ID tracking for debugging

#### Rate Limiting
- Per-key rate limiting
- Burst protection
- Automatic cleanup

### Security Headers (API)
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

## Dependency Security

### Vulnerability Scanning
- Weekly automated dependency scans
- GitHub Dependabot integration
- Manual security reviews for major updates

### Supply Chain Security
- Signed Docker images
- Provenance metadata
- Reproducible builds

### Third-Party Dependencies
| Component | Scanner | Frequency |
|-----------|---------|-----------|
| Python packages | Safety, Bandit | Weekly |
| Docker images | Trivy | Weekly |
| Node packages | npm audit | Weekly |
| Rust crates | cargo-audit | Weekly |

## Security Updates

### Update Process

1. **Vulnerability Discovery**
   - Private disclosure received
   - Triage and assessment
   - Severity classification

2. **Fix Development**
   - Private branch created
   - Fix implemented and tested
   - Security review conducted

3. **Coordination**
   - Maintainer notification (if applicable)
   - Update timeline agreed
   - Disclosure date set

4. **Release**
   - Security advisory published
   - Patch released
   - Documentation updated

5. **Post-Disclosure**
   - Monitor for exploitation
   - Support users with updates
   - Lessons learned review

### Update Channels

- **GitHub Security Advisories**: For vulnerability notifications
- **GitHub Releases**: For patched versions
- **Docker Hub**: For updated container images
- **PyPI**: For updated Python packages

## Security Team

### Core Security Team
- **Lead Maintainer**: security@errorfingerprint.dev
- **Security Engineers**: security@errorfingerprint.dev
- **Community Liaison**: conduct@errorfingerprint.dev

### Security Advisors
- External security researchers (confidential)
- Industry security experts (confidential)
- Community contributors (public acknowledgment)

## Recognition Program

### Bounty Program

| Severity | Bounty Range | Recognition |
|----------|--------------|-------------|
| Critical | $500 - $2,000 | Hall of Fame, Blog post |
| High | $200 - $1,000 | Hall of Fame, Twitter mention |
| Medium | $50 - $500 | Hall of Fame |
| Low | $25 - $100 | Thank you note |

### Hall of Fame
Security researchers who contribute valid vulnerability reports will be acknowledged (with permission) in:
- Project README
- Security advisories
- Annual security report
- Conference talks (with permission)

## Compliance

### Standards Compliance
- **OWASP Top 10**: Addressed in design
- **CIS Controls**: Implemented where applicable
- **NIST Cybersecurity Framework**: Aligned with principles
- **SOC 2**: Planning for Type II compliance

### Data Protection
- **GDPR**: No personal data processed
- **CCPA**: No personal data collected
- **Data Minimization**: Only error messages processed
- **Right to Deletion**: Data not retained

## Contact Information

### Security Team
- **Primary**: security@errorfingerprint.dev
- **PGP**: Available upon request
- **Response Time**: Within 24 hours for critical issues

### General Inquiries
- **Project**: conduct@errorfingerprint.dev
- **Business**: contact@errorfingerprint.dev
- **Support**: support@errorfingerprint.dev

### Social Media
- **Twitter**: @errorfingerprint
- **GitHub**: github.com/Linky-Link-Linky/Error-Fingerprint

---

Thank you for helping keep Error Fingerprint secure! 🛡️

We appreciate your efforts in responsibly disclosing security vulnerabilities and helping us maintain a secure ecosystem for all users.
