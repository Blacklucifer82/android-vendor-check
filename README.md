<div align="center">

# VendorCheck

### Static Analysis Toolkit for Android Proprietary Vendor Blobs

Analyze • Verify • Validate • Repair

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg)]()
[![Android](https://img.shields.io/badge/Android-AOSP-brightgreen.svg)]()

A comprehensive static analysis toolkit for Android proprietary vendor blobs.

**VendorCheck** helps Android ROM developers validate vendor trees before
building AOSP-based ROMs by analyzing blob integrity, ELF dependencies,
Android.bp modules, compatibility, symbol resolution, and providing
actionable repair suggestions.

</div>

---

# Overview

Android ROM bring-up often involves spending hours debugging vendor trees,
tracking missing libraries, fixing Android.bp modules, resolving undefined
symbols, and identifying compatibility issues.

VendorCheck automates this process by performing a complete static analysis
of extracted vendor blobs and generating detailed reports that help developers
identify and resolve problems before compilation.

Instead of manually inspecting hundreds or thousands of proprietary binaries,
VendorCheck performs the analysis automatically and produces practical,
developer-friendly output.

---

# Why VendorCheck?

VendorCheck was designed to answer questions such as:

- Is every proprietary blob present?
- Do SHA-1 hashes match the expected values?
- Which blobs require `blob_fixup()` modifications?
- Which ELF libraries are missing dependencies?
- Are Android.bp `shared_libs` correct?
- Which modules contain unused libraries?
- Are there compatibility problems between extracted blobs and Android.bp?
- Which blobs require shim libraries?
- What changes should be made before building the ROM?

Rather than reporting raw data, VendorCheck attempts to provide meaningful,
actionable suggestions that reduce manual debugging during Android bring-up.

---

# Features

## Blob Integrity

- SHA-1 verification
- Missing blob detection
- SHA mismatch detection
- Fixed SHA support
- `blob_fixup()` awareness
- Integrity statistics

---

## ELF Analysis

VendorCheck performs deep inspection of ELF binaries.

Supported analysis includes:

- ELF identification
- SONAME extraction
- DT_NEEDED parsing
- Undefined symbol extraction
- Exported symbol indexing
- Shared library resolution
- Vendor library classification

---

## Android.bp Analysis

VendorCheck parses Android.bp modules and compares them with actual ELF
requirements.

Checks include:

- Module parsing
- Blob-to-module matching
- Missing `shared_libs`
- Unused `shared_libs`
- Android.bp verification
- Automatic repair suggestions

---

## Dependency Resolution

VendorCheck builds a dependency graph for proprietary libraries and validates
their relationships.

Supported checks include:

- Missing DT_NEEDED libraries
- Vendor dependencies
- Platform libraries
- Optional libraries
- Shim libraries
- Compatibility libraries
- ROM libraries

---

## Compatibility Analysis

Every Android.bp module receives a compatibility score based on the agreement
between Android.bp definitions and actual ELF dependencies.

Example:

| Module | Compatibility |
|---------|--------------:|
| libadsprpc | 100% |
| camera.qcom | 85% |
| audio.primary.qcom | 60% |

This helps quickly identify modules that require attention.

---

## Suggestions Engine

Instead of simply reporting issues, VendorCheck recommends possible fixes.

Examples include:

- Add missing `shared_libs`
- Remove unused `shared_libs`
- Missing dependency warnings
- Shim recommendations
- Blob fixup detection
- Android.bp patch generation

---

## Reports

VendorCheck generates both human-readable and machine-readable reports.

Available outputs include:

- Terminal analysis report
- JSON report
- Compatibility report
- Vendor health score
- Dependency statistics
- Suggested Android.bp patches

---

# Architecture

```text
                   proprietary-files.txt
                             │
                             ▼
                  Proprietary File Parser
                             │
                             ▼
                    SHA Verification Engine
                             │
                             ▼
                  extract-files.py Parser
                             │
                             ▼
                    blob_fixup Detection
                             │
                             ▼
                     Android.bp Parser
                             │
                             ▼
                        ELF Analyzer
                             │
                             ▼
                  Library Classification
                             │
                             ▼
                  Dependency Resolution
                             │
                             ▼
                  Compatibility Analysis
                             │
                             ▼
                   Suggestions Generator
                             │
                             ▼
                     Report Generation
```

---

# Analysis Pipeline

VendorCheck performs analysis in multiple independent stages.

```text
Stage 1
──────────────
Read proprietary-files.txt

        │
        ▼

Stage 2
──────────────
Verify SHA-1 hashes

        │
        ▼

Stage 3
──────────────
Parse extract-files.py

        │
        ▼

Stage 4
──────────────
Detect blob_fixups

        │
        ▼

Stage 5
──────────────
Parse Android.bp

        │
        ▼

Stage 6
──────────────
Analyze ELF binaries

        │
        ▼

Stage 7
──────────────
Resolve library dependencies

        │
        ▼

Stage 8
──────────────
Compare Android.bp with ELF

        │
        ▼

Stage 9
──────────────
Generate repair suggestions

        │
        ▼

Stage 10
──────────────
Produce reports
```

Each stage is independent, making VendorCheck modular, extensible, and easy
to debug or enhance.

---

# Supported Analysis

✔ Proprietary blob verification

✔ SHA-1 validation

✔ Missing blob detection

✔ ELF analysis

✔ DT_NEEDED verification

✔ Undefined symbol detection

✔ SONAME extraction

✔ Android.bp verification

✔ Shared library validation

✔ Compatibility scoring

✔ Vendor health calculation

✔ JSON report generation

✔ Android.bp repair suggestions

✔ Blob fixup detection

# Requirements

VendorCheck is designed for Linux environments used for Android ROM
development.

## Supported Platforms

- Linux (recommended)
- WSL2 (untested but should work)
- macOS (experimental)
- Windows (not officially supported)

## Python

- Python 3.10 or newer

## Dependencies

VendorCheck currently depends on:

- pyelftools

Install the project using:

```bash
git clone https://github.com/Blacklucifer82/android-vendor-check.git

cd android-vendor-check

pip install -e .
```

Or install only the runtime dependency:

```bash
pip install pyelftools
```

---

# Getting Started

VendorCheck analyzes an extracted vendor tree together with the associated
Android ROM source files.

A typical setup contains:

```text
device/
└── vendor/
    └── device/
        ├── proprietary-files.txt
        └── extract-files.py

vendor/
└── vendor/
    └── device/
        ├── proprietary/
        └── Android.bp
```

VendorCheck combines information from all of these files to perform
cross-validation.

---

# Basic Usage

Run a complete analysis:

```bash
python3 vendor_check.py \
    --proprietary device/<vendor>/<device>/proprietary-files.txt \
    --vendor vendor/<vendor>/<device>/proprietary \
    --extract device/<vendor>/<device>/extract-files.py \
    --bp vendor/<vendor>/<device>/Android.bp \
    --elf
```

This performs:

- SHA verification
- Blob validation
- Android.bp parsing
- ELF dependency analysis
- Compatibility scoring
- Suggestions generation

---

# Generate a JSON Report

Machine-readable output can be generated with:

```bash
python3 vendor_check.py \
    --proprietary device/<vendor>/<device>/proprietary-files.txt \
    --vendor vendor/<vendor>/<device>/proprietary \
    --extract device/<vendor>/<device>/extract-files.py \
    --bp vendor/<vendor>/<device>/Android.bp \
    --elf \
    --json report.json
```

The generated JSON can be consumed by:

- CI pipelines
- GitHub Actions
- Automation scripts
- Dashboards
- Custom tooling

---

# Command-Line Arguments

| Argument | Description |
|-----------|-------------|
| `--proprietary` | Path to `proprietary-files.txt` |
| `--vendor` | Vendor proprietary blob directory |
| `--extract` | `extract-files.py` used for blob fixups |
| `--bp` | Android.bp containing blob modules |
| `--elf` | Enable ELF analysis |
| `--json` | Export machine-readable JSON report |

---

# Example

Example command:

```bash
python3 vendor_check.py \
    --proprietary device/realme/RMX1851/proprietary-files.txt \
    --vendor vendor/realme/RMX1851/proprietary \
    --extract device/realme/RMX1851/extract-files.py \
    --bp vendor/realme/RMX1851/Android.bp \
    --elf \
    --json report.json
```

---

# Example Terminal Output

```text
========================

OK        : 1058
FIXUP     : 12
Mismatch  : 4
Missing   : 0

========================

=== ELF Summary ===

ELF blobs : 756
SONAMEs   : 677

=== Compatibility ===

camera.qcom                 85%
audio.primary.qcom          60%

=== Vendor Health ===

99%
```

The complete report also includes:

- Missing DT_NEEDED libraries
- Android.bp compatibility
- Blob fixup detection
- Android.bp repair suggestions
- Missing shared libraries
- Unused shared libraries

---

# Typical Workflow

VendorCheck is generally used after extracting proprietary blobs.

```text
Dump firmware
      │
      ▼

Extract proprietary blobs
      │
      ▼

Generate Android.bp
      │
      ▼

Run VendorCheck
      │
      ▼

Review suggestions
      │
      ▼

Fix Android.bp
      │
      ▼

Build ROM
```

Running VendorCheck before every build can help detect issues earlier and
reduce manual debugging.

---

# Typical Output Categories

VendorCheck groups its findings into several categories.

## Integrity

- Verified blobs
- SHA mismatches
- Missing blobs
- Blob fixups

---

## ELF

- DT_NEEDED libraries
- Undefined symbols
- SONAME information
- Exported symbols

---

## Android.bp

- Missing shared libraries
- Unused shared libraries
- Compatibility scores

---

## Suggestions

- Android.bp patches
- Missing dependencies
- Shim recommendations
- Blob fixup information

---

## Reports

- Terminal summary
- JSON report
- Vendor health score
- Compatibility statistics

---

# Exit Status

VendorCheck exits with a standard process status.

| Exit Code | Meaning |
|-----------|---------|
| `0` | Analysis completed successfully |
| Non-zero | Fatal error occurred (invalid input, missing files, parsing failure, etc.) |

This behavior makes VendorCheck suitable for scripting and CI integration.

# Understanding the Results

VendorCheck produces multiple forms of analysis to help identify problems
within a vendor tree. Rather than reporting only raw data, the tool attempts
to summarize the overall health of the vendor and provide actionable
suggestions.

The primary metrics are:

- Vendor Health
- Compatibility Scores
- Dependency Analysis
- Integrity Verification
- Repair Suggestions

---

# Vendor Health Score

The **Vendor Health Score** is an overall indicator of vendor tree quality.

It combines the results of multiple analysis stages into a single percentage,
making it easy to estimate how ready a vendor tree is for ROM development.

The health score considers factors such as:

- SHA verification results
- Missing proprietary blobs
- DT_NEEDED dependency issues
- Android.bp compatibility
- Blob integrity
- Repair suggestions

Example:

```text
========================

Vendor Health

99%

========================
```

## Health Score Interpretation

| Score | Status | Meaning |
|-------:|--------|---------|
| 100% | Excellent | No significant issues detected |
| 90–99% | Production Ready | Minor issues may exist |
| 80–89% | Good | Some improvements recommended |
| 60–79% | Fair | Several issues should be addressed |
| Below 60% | Poor | Major bring-up problems detected |

A lower score does **not** necessarily indicate that the ROM cannot boot.
Instead, it highlights areas that may require investigation.

---

# Compatibility Score

Each Android.bp module receives an independent compatibility score.

The score estimates how closely the module definition matches the actual ELF
dependencies of the proprietary blobs.

Example:

| Module | Score |
|---------|------:|
| libadsprpc | 100% |
| camera.qcom | 85% |
| audio.primary.qcom | 60% |

Higher scores generally indicate better consistency between Android.bp and the
vendor blobs.

---

## Compatibility Penalties

The score may be reduced for issues such as:

- Missing `shared_libs`
- Unused `shared_libs`
- Incorrect dependency declarations
- Missing vendor libraries

For example:

```text
camera.qcom

Missing

libprotobuf-cpp-full-3.9.1

Unused

libprotobuf-cpp-full-3.9.1-vendorcompat

Compatibility

85%
```

Compatibility scores are intended as guidance rather than absolute indicators
of correctness.

---

# Dependency Analysis

VendorCheck analyzes ELF dependencies using the `DT_NEEDED` entries of each
binary.

Typical checks include:

- Missing libraries
- Vendor library references
- Platform library references
- Optional libraries
- Shim libraries
- Compatibility libraries

Example:

```text
libcamera.so

Missing Dependency

libfoo.so
```

A reported dependency should be reviewed before deciding whether it requires
modification. Some libraries may be provided by other partitions or by the
Android platform at runtime.

---

# Blob Integrity

VendorCheck verifies every blob listed in `proprietary-files.txt`.

Checks include:

- SHA-1 verification
- Missing files
- SHA mismatches
- Fixed SHA support
- `blob_fixup()` detection

Example summary:

```text
OK        : 1058
FIXUP     : 12
Mismatch  : 4
Missing   : 0
```

---

# ELF Analysis

VendorCheck automatically identifies ELF binaries and extracts useful
information such as:

- SONAME
- DT_NEEDED libraries
- Undefined symbols
- Exported symbols

Example:

```text
ELF blobs : 756

SONAMEs   : 677
```

This information is used during dependency resolution and compatibility
analysis.

---

# Android.bp Verification

VendorCheck compares Android.bp definitions with the requirements of the
corresponding proprietary blobs.

Checks include:

- Missing `shared_libs`
- Unused `shared_libs`
- Incorrect library declarations
- Compatibility mismatches

Example:

```text
camera.qcom

Missing shared_libs

libprotobuf-cpp-full-3.9.1

Unused shared_libs

libprotobuf-cpp-full-3.9.1-vendorcompat
```

Where possible, VendorCheck recommends appropriate changes.

---

# Suggestions Engine

The Suggestions Engine converts analysis results into practical
recommendations.

Typical suggestions include:

- Add missing `shared_libs`
- Remove unused `shared_libs`
- Review missing dependencies
- Check blob fixups
- Consider shim libraries
- Update Android.bp definitions

Suggestions are intended to reduce manual debugging during ROM bring-up.

---

# JSON Report

VendorCheck can export a machine-readable JSON report for automation and
integration with external tools.

Example command:

```bash
python3 vendor_check.py \
    --proprietary ... \
    --vendor ... \
    --extract ... \
    --bp ... \
    --elf \
    --json report.json
```

Example output:

```json
{
  "health": 99,
  "statistics": {
    "total_blobs": 1062,
    "verified": 1058,
    "verified_percent": 99.6,
    "elf_blobs": 756,
    "missing_dependencies": 170,
    "blob_fixups": 12
  },
  "compatibility": [
    {
      "module": "camera.qcom",
      "score": 85
    },
    {
      "module": "audio.primary.qcom",
      "score": 60
    }
  ]
}
```

The JSON report is designed for:

- CI pipelines
- GitHub Actions
- Build automation
- Dashboards
- Third-party tooling
- Custom scripts

---

# Sample Analysis

The following example shows a real analysis performed on an Android vendor
tree.

| Metric | Result |
|--------|-------:|
| Total blobs | 1062 |
| Verified blobs | 1058 |
| ELF binaries | 756 |
| Blob fixups | 12 |
| Missing dependencies | 170 |
| Vendor Health | 99% |

This demonstrates the scale of analysis that VendorCheck performs during a
single run.

---

# Performance

VendorCheck is designed to analyze large vendor trees efficiently.

Typical execution times for a vendor tree containing approximately 1,000
blobs are shown below.

| Stage | Typical Time |
|--------|-------------:|
| Parse proprietary-files.txt | < 1 second |
| SHA verification | 2–5 seconds |
| Android.bp parsing | < 1 second |
| ELF analysis | 5–20 seconds |
| Dependency resolution | 1–3 seconds |
| Report generation | < 1 second |

Actual execution time depends primarily on the number and size of ELF
binaries being analyzed.

---

# Notes

VendorCheck performs **static analysis only**.

It does **not** execute proprietary binaries, modify vendor blobs, or make
changes to Android.bp automatically.

All reported issues should be reviewed by the developer before applying any
changes.

# Project Structure

The project is organized into small, focused modules that each perform a
specific task during the analysis pipeline.

```text
VendorCheck/
│
├── vendor_check.py          # CLI entry point
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── pyproject.toml
├── requirements.txt
│
└── vendorcheck/
    ├── analyzer.py          # Main analysis engine
    ├── androidbp.py         # Android.bp parser
    ├── bpverify.py          # Android.bp verification
    ├── classifier.py        # Library classification
    ├── classify.py          # Runtime classification helpers
    ├── compatibility.py     # Compatibility scoring
    ├── dependency.py        # Dependency analysis
    ├── elf.py               # ELF parser
    ├── fixups.py            # blob_fixup parsing
    ├── group.py             # Result grouping
    ├── hashcheck.py         # SHA verification
    ├── health.py            # Vendor health calculation
    ├── ignoredlibs.py       # Ignored libraries database
    ├── index.py             # Library indexing
    ├── jsonreport.py        # JSON report generation
    ├── models.py            # Shared data models
    ├── parser.py            # proprietary-files parser
    ├── patch.py             # Android.bp patch generation
    ├── report.py            # Terminal reporting
    ├── resolver.py          # Symbol resolution
    ├── resolverdb.py        # Resolver database
    ├── romindex.py          # ROM library index
    ├── stats.py             # Statistics
    ├── suggestions.py       # Repair suggestions
    ├── systemlibs.py        # Platform library database
    └── utils.py             # Shared utilities
```

Each module has a single responsibility, making VendorCheck easier to
maintain, extend, and test.

---

# Design Goals

VendorCheck is built around a few core principles:

- Fast enough for daily ROM development
- Easy to extend with new analysis stages
- Independent analysis modules
- Developer-friendly reports
- Practical repair suggestions
- Safe, read-only analysis
- Minimal external dependencies

The project focuses on providing useful diagnostics without modifying the
vendor tree.

---

# Typical Use Cases

VendorCheck is useful for:

- Android ROM bring-up
- Vendor tree validation
- Android.bp verification
- Blob extraction review
- Device tree maintenance
- Vendor migration between Android versions
- Dependency auditing
- Compatibility analysis
- Continuous Integration (CI)
- Release verification before building

---

# Known Limitations

VendorCheck currently focuses on static analysis of extracted vendor blobs.

The following are **not** analyzed in the current release:

- Framework JAR files
- Boot or vendor boot images
- SELinux policies
- init.rc scripts
- VINTF manifests
- Runtime linker namespaces
- APEX payloads
- Kernel modules

These areas may be supported in future versions.

---

# Roadmap

The roadmap reflects planned improvements but may change as the project
evolves.

## Version 1.1

Planned improvements:

- Improved ROM library indexing
- Expanded platform library database
- Better dependency classification
- Automatic shim recommendations
- Improved compatibility analysis
- Additional report statistics

---

## Version 1.2

Planned improvements:

- Duplicate blob detection
- Vendor consistency checks
- Symbol version awareness
- Parallel ELF analysis
- Colored terminal output
- Performance optimizations

---

## Version 2.0

Long-term goals:

- Automatic Android.bp repair
- Interactive command-line interface
- HTML report generation
- Dependency graph visualization
- Plugin architecture
- Vendor bring-up assistant

---

# Contributing

Contributions are welcome and appreciated.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Follow the existing coding style.
4. Add or update documentation when necessary.
5. Test your changes before submitting.
6. Open a Pull Request.

Please read **CONTRIBUTING.md** for detailed contribution guidelines.

---

# Reporting Issues

Bug reports are greatly appreciated.

When opening an issue, please include:

- Device name
- Android version
- Vendor tree source
- Python version
- Complete terminal output
- JSON report (if available)
- Steps to reproduce the problem

Providing complete information makes debugging significantly easier.

---

# Security

If you discover a security issue, please follow the instructions in
**SECURITY.md** instead of opening a public issue.

---

# Code of Conduct

To help maintain a welcoming and respectful community, all contributors are
expected to follow the project's **CODE_OF_CONDUCT.md**.

---

# Testing

Before submitting changes, it is recommended to run:

Compile the project:

```bash
python3 -m compileall vendorcheck
```

Run your analysis:

```bash
python3 vendor_check.py \
    --proprietary ... \
    --vendor ... \
    --extract ... \
    --bp ... \
    --elf
```

If unit tests are added in future releases, they should also be executed
before submitting contributions.

---

# License

VendorCheck is released under the **MIT License**.

See the **LICENSE** file for the full license text.

---

# Acknowledgements

VendorCheck is inspired by the Android Open Source Project and the
Android custom ROM development community.

Special thanks to the developers and maintainers of:

- Android Open Source Project (AOSP)
- LineageOS
- PixelExperience
- Evolution X
- crDroid
- Project Matrixx
- DerpFest
- RisingOS
- OmniROM

Their work on open-source Android development has made projects like
VendorCheck possible.

Additional thanks to the authors of **pyelftools**, whose library provides
the foundation for ELF parsing within VendorCheck.

---

# Support

If VendorCheck helps your Android ROM development, consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🔧 Contributing improvements
- 📖 Improving documentation

Every contribution, whether code, documentation, or feedback, helps improve
the project.

---

<div align="center">

# VendorCheck

**Static Analysis Toolkit for Android Proprietary Vendor Blobs**

Built for the Android ROM Development Community.

Made with ❤️ for Android bring-up developers.

</div>
