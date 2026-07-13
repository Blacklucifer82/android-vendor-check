from vendorcheck.systemlibs import (
    SYSTEM_LIBS,
    OPTIONAL_SYSTEM_LIBS,
)

ANDROID_PREFIXES = (
    "android.",
    "vendor.",
)

def should_ignore(lib: str) -> bool:
    if lib.startswith("android."):
        return True

    if lib.startswith("vendor."):
        return True

    if lib.endswith("-V1-ndk.so"):
        return True

    if lib.endswith("-V2-ndk.so"):
        return True

    if lib.endswith("-V3-ndk.so"):
        return True

    if lib.endswith("-V4-ndk.so"):
        return True

    if lib == "libgcc.so":
        return True

    return False


import os

def build_soname_index(blobs):

    index = {}

    for blob in blobs:

        if not blob.is_elf:
            continue

        # SONAME
        if blob.soname:
            index[blob.soname] = blob

        # filename fallback
        filename = os.path.basename(blob.path)
        index.setdefault(filename, blob)

    return index

def check_needed(blobs):
    sonames = build_soname_index(blobs)

    results = {}

    for blob in blobs:

        if not blob.is_elf:
            continue

        missing = []

        for lib in blob.needed:

            if should_ignore(lib):
                continue

            if lib in SYSTEM_LIBS:
                continue
            if lib in OPTIONAL_SYSTEM_LIBS:
                continue

            if lib not in sonames:
                missing.append(lib)

        results[blob.path] = missing

    return results
