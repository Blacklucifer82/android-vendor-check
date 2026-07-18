---

# Project Philosophy

VendorCheck aims to provide reliable static analysis for Android vendor trees.

The primary goals are:

- Accuracy over quantity
- Practical analysis for Android ROM development
- Minimal false positives
- Clear and actionable reports
- Maintainable and well-documented code

Contributions should align with these goals.



# Contributing to VendorCheck

First off, thank you for your interest in contributing to VendorCheck!

VendorCheck is an open-source static analysis toolkit for Android proprietary
vendor blobs. Contributions that improve reliability, accuracy, and usability
are always welcome.

---

# Ways to Contribute

You can contribute by:

- Reporting bugs
- Suggesting new features
- Improving documentation
- Fixing bugs
- Improving existing analyzers
- Adding support for newer Android versions
- Writing tests
- Improving performance

---

# Before You Start

Please check existing Issues and Pull Requests before opening a new one.

If you are planning a large feature, open an issue first so it can be discussed.

---

# Development Setup

Clone the repository

```bash
git clone https://github.com/Blacklucifer82/android-vendor-check.git
cd android-vendor-check
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run VendorCheck

```bash
python3 vendor_check.py --help
```

---

# Coding Guidelines

Please follow these guidelines:

- Use Python 3.10+
- Follow PEP 8 style conventions
- Keep functions small and focused
- Add comments only where necessary
- Prefer readable code over clever code
- Keep modules independent when possible

---

# Commit Messages

Use clear commit messages.

Examples:

```text
parser: improve proprietary-files parser

elf: fix DT_NEEDED parsing

bp: improve shared_lib detection

resolver: reduce false positives

docs: update README

tests: add parser unit tests
```

Avoid messages like:

```text
fix

update

changes

misc
```

---

# Pull Requests

Before submitting a Pull Request, please ensure:

- The project runs without errors
- New code is documented
- Existing functionality is not broken
- README is updated if necessary
- New features include appropriate tests (when applicable)

Provide a clear description of:

- What changed
- Why it changed
- Any limitations
- Related issue number (if applicable)

---

# Reporting Bugs

When reporting a bug, include:

- Android version
- Device name
- Vendor source
- Python version
- Complete terminal output
- JSON report (if available)
- Steps to reproduce

This helps reproduce and resolve issues more quickly.

---

# Feature Requests

Feature requests are welcome.

Please explain:

- The problem you're trying to solve
- Why the feature is useful
- Possible implementation ideas (optional)

Features that improve vendor tree analysis are preferred over cosmetic additions.

---

# Code of Conduct

Please read the
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
before contributing.

---

# License

By contributing to VendorCheck, you agree that your contributions will be
licensed under the MIT License.
