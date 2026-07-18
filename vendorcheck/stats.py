from collections import Counter


def collect_stats(blobs):
    """
    Collect statistics about analyzed blobs.

    Returns:
        dict[str, int]
    """

    stats = Counter()

    stats["total_blobs"] = len(blobs)

    for blob in blobs:

        #
        # ELF blobs
        #
        if getattr(blob, "is_elf", False):
            stats["elf_blobs"] += 1

        #
        # SHA verification
        #
        if getattr(blob, "verified", False):
            stats["verified"] += 1
        else:
            stats["sha_mismatch"] += 1

        #
        # extract-files.py fixups
        #
        if getattr(blob, "has_fixup", False):
            stats["blob_fixups"] += 1

        #
        # Missing DT_NEEDED
        #
        if getattr(blob, "missing_libs", []):
            stats["blobs_with_missing_libs"] += 1
            stats["missing_dependencies"] += len(blob.missing_libs)

        #
        # Suggestions
        #
        if getattr(blob, "suggestions", []):
            stats["blobs_with_suggestions"] += 1
            stats["total_suggestions"] += len(blob.suggestions)

    #
    # Derived values
    #
    stats["verified_percent"] = round(
        stats["verified"] * 100 / max(1, stats["total_blobs"]),
        1,
    )

    stats["elf_percent"] = round(
        stats["elf_blobs"] * 100 / max(1, stats["total_blobs"]),
        1,
    )

    return dict(stats)
