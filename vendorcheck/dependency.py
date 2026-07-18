from vendorcheck.systemlibs import (
    SYSTEM_LIBS,
    OPTIONAL_SYSTEM_LIBS,
)


def should_ignore(lib: str) -> bool:
    """
    Libraries that should never be reported as missing.
    """

    if not lib:
        return True

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


def check_needed(blobs, library_db):
    """
    Verify that every DT_NEEDED library is provided by
    either:
        • Vendor blobs
        • Known system libraries

    Returns:
        {
            blob.path: [
                missing_lib1,
                missing_lib2,
                ...
            ]
        }
    """

    results = {}

    for blob in blobs:

        if not blob.is_elf:
            continue

        missing = []

        for lib in sorted(blob.needed):

            #
            # Ignore Android generated libs
            #
            if should_ignore(lib):
                continue

            #
            # Core platform libraries
            #
            if lib in SYSTEM_LIBS:
                continue

            #
            # Optional libraries
            #
            if lib in OPTIONAL_SYSTEM_LIBS:
                continue

            #
            # Vendor provides it
            #
            if library_db.has(lib):
                continue

            #
            # Really missing
            #
            missing.append(lib)

        results[blob.path] = missing

    return results
