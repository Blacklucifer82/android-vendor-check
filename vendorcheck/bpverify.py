def verify_bp(blob, module):
    """
    Compare ELF DT_NEEDED against Android.bp shared_libs.
    """

    needed = set()

    for lib in blob.needed:

        if not lib.endswith(".so"):
            continue

        needed.add(lib[:-3])

    shared = set(module["shared_libs"])

    return {
        "missing": sorted(needed - shared),
        "unused": sorted(shared - needed),
    }
