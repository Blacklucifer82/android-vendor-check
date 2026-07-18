def generate_bp_patch(result):
    """
    Generate a suggested Android.bp patch from a compatibility result.

    Returns:
        list[str]
    """

    if not result:
        return []

    bp = result.get("bp")

    if bp is None:
        return []

    patch = []

    missing = bp.get("missing", [])
    unused = bp.get("unused", [])

    #
    # Nothing to change
    #
    if not missing and not unused:
        return []

    patch.append("Android.bp patch:")

    #
    # Missing shared_libs
    #
    if missing:

        patch.append("")

        patch.append("Add to shared_libs:")

        for lib in sorted(missing):
            patch.append(f'    "{lib}",')

    #
    # Unused shared_libs
    #
    if unused:

        patch.append("")

        patch.append("Remove from shared_libs:")

        for lib in sorted(unused):
            patch.append(f'    "{lib}",')

    return patch
