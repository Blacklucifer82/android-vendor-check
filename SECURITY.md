# Security Policy

## Supported Versions

The following versions currently receive security updates.

| Version | Supported |
|----------|:---------:|
| 1.x.x | ✅ Yes |
| < 1.0 | ❌ No |

---

# Reporting a Vulnerability

If you discover a security vulnerability in VendorCheck, please do **not**
open a public GitHub issue immediately.

Instead, report it privately by one of the following methods:

- GitHub Security Advisories (preferred)
- Contact the repository maintainer directly

Please include:

- A description of the vulnerability
- Steps to reproduce
- A proof of concept (if available)
- Potential impact
- Suggested mitigation (optional)

We will acknowledge reports as quickly as possible and work to resolve
confirmed vulnerabilities.

---

# Scope

Examples of security issues include:

- Arbitrary code execution
- Command injection
- Unsafe file handling
- Path traversal
- Denial of service caused by malformed input
- Unsafe parsing of Android vendor files

Issues outside the scope of this policy include:

- False positives in analysis results
- Documentation mistakes
- Feature requests
- Cosmetic issues
- Performance improvements

---

# Security Best Practices

VendorCheck analyzes files provided by the user.

For best security:

- Only analyze vendor trees from trusted sources.
- Review generated suggestions before applying them.
- Do not execute generated output without verification.
- Keep Python and dependencies up to date.

---

# Third-Party Dependencies

VendorCheck relies on Python and third-party libraries.

Please ensure dependencies are kept up to date and report any known
vulnerabilities affecting them.

---

# Disclosure Policy

We follow a responsible disclosure process.

After a vulnerability has been verified and a fix is available, details may be
disclosed publicly through the project's GitHub Releases or Changelog.

---

# Contact

For security-related concerns, please use GitHub Security Advisories if
available or contact the project maintainer directly.

Thank you for helping keep VendorCheck secure.
