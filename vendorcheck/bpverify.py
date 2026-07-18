from vendorcheck.ignoredlibs import IGNORED_BP_LIBS


def normalize(lib: str) -> str:
    """
    Convert:
        libc.so -> libc
    """
    if lib.endswith(".so"):
        return lib[:-3]
    return lib


def verify_bp(blob, module):
    """
    Compare ELF DT_NEEDED against Android.bp shared_libs.

    Returns:
    {
        "missing": [...],
        "unused": [...]
    }
    """

    #
    # Libraries actually required by ELF
    #
    needed = set()

    for lib in blob.needed:

        lib = normalize(lib)

        if lib in IGNORED_BP_LIBS:
            continue

        needed.add(lib)

    #
    # Libraries declared in Android.bp
    #
    shared = set()

    for lib in module.get("shared_libs", []):

        if lib in IGNORED_BP_LIBS:
            continue

        shared.add(lib)

    #
    # Compute differences
    #
    missing = sorted(needed - shared)

    unused = sorted(shared - needed)

    return {
        "missing": missing,
        "unused": unused,
    }
