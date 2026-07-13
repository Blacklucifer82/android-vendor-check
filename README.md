# Vendor Check

Vendor Check is a Python utility for Android ROM developers to validate extracted vendor blobs.

## Planned Features

- SHA1 verification against `proprietary-files.txt`
- Blob fixup detection
- ELF dependency analysis
- Undefined symbol detection
- Missing DT_NEEDED libraries
- Android.bp validation
- Compatibility group analysis (GNSS, Camera, Audio, etc.)

## Current Features

- SHA1 verification
- Missing blob detection
- Duplicate entry detection
