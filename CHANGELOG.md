# Changelog

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog and this project adheres to Semantic Versioning.

---

## [1.0.0] - 2026-07-17

### Overview

This is the first public release of **VendorCheck**, a static analysis toolkit
designed to help Android ROM developers validate proprietary vendor trees before
building AOSP-based ROMs.

### Added

#### SHA Verification
- Initial SHA-1 verification framework
- Missing blob detection
- Fixed SHA support
- Blob integrity validation

#### ELF Analysis
- ELF binary detection
- DT_NEEDED parsing
- SONAME extraction
- Undefined symbol detection
- Exported symbol indexing

#### Android.bp Analysis
- Android.bp parser
- Module extraction
- shared_libs verification
- Missing dependency detection
- Unused shared library detection

#### Compatibility Framework
- Android.bp compatibility scoring
- Vendor Health calculation
- Dependency verification
- Suggestions engine
- JSON report generation

#### Project
- MIT License
- Initial project documentation
- Command-line interface
- GitHub repository

### Supported

- Android 10
- Android 11
- Android 12
- Android 13
- Android 14
- Android 15
- Android 16
