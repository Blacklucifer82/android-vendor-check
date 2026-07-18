from vendorcheck.compatibility import check_blob
from vendorcheck.patch import generate_bp_patch


def add(suggestions, text):
    """
    Add a suggestion only once.
    """
    if text not in suggestions:
        suggestions.append(text)


def suggest(blob, src_index):
    """
    Generate repair suggestions for a blob.
    """

    suggestions = []

    #
    # Android.bp compatibility
    #
    result = check_blob(blob, src_index)

    if result is None:
        return suggestions

    bp = result.get("bp")

    #
    # No Android.bp module
    #
    if bp is None:

        if getattr(blob, "has_fixup", False):
            add(
                suggestions,
                "Blob has extract-files.py fixup",
            )

        for lib in getattr(blob, "missing_libs", []):

            add(
                suggestions,
                f"Missing dependency: {lib}",
            )

        return suggestions

    #
    # Missing shared_libs
    #
    for lib in bp.get("missing", []):

        add(
            suggestions,
            f"Add shared_lib: {lib}",
        )

    #
    # Unused shared_libs
    #
    for lib in bp.get("unused", []):

        add(
            suggestions,
            f"Remove shared_lib: {lib}",
        )

    #
    # blob_fixup
    #
    if getattr(blob, "has_fixup", False):

        add(
            suggestions,
            "Blob has extract-files.py fixup",
        )

    #
    # Missing DT_NEEDED
    #
    for lib in getattr(blob, "missing_libs", []):

        add(
            suggestions,
            f"Missing dependency: {lib}",
        )

    #
    # Android.bp patch
    #
    patch = generate_bp_patch(result)

    if patch:

        add(
            suggestions,
            "",
        )

        for line in patch:

            add(
                suggestions,
                line,
            )

    return suggestions
