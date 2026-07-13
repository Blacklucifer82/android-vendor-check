from vendorcheck.compatibility import check_blob


def suggest(blob, src_index):
    """
    Generate repair suggestions for one blob.
    """

    suggestions = []

    result = check_blob(blob, src_index)

    if result is None:
        return suggestions

    bp = result.get("bp")

    #
    # Blob has no Android.bp module
    #
    if bp is None:
        if blob.has_fixup:
            suggestions.append("Blob has extract-files.py fixup")

        for lib in blob.missing_libs:
            suggestions.append(f"Missing dependency: {lib}")

        return suggestions

    #
    # Missing shared_libs
    #
    for lib in bp.get("missing", []):
        suggestions.append(f"Add shared_lib: {lib}")

    #
    # Unused shared_libs
    #
    for lib in bp.get("unused", []):
        suggestions.append(f"Remove shared_lib: {lib}")

    #
    # Blob fixup
    #
    if blob.has_fixup:
        suggestions.append("SHA mismatch expected (blob_fixup present)")

    #
    # Missing DT_NEEDED
    #
    for lib in blob.missing_libs:
        suggestions.append(f"Missing dependency: {lib}")

    return suggestions
