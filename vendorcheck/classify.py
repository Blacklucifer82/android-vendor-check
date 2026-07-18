def classify_library(lib, library_db, rom_index=None):
    """
    Classify one DT_NEEDED library.
    """

    if library_db.has(lib):
        return "vendor"

    if rom_index and rom_index.has(lib):
        return "rom"

    if lib.endswith("_shim.so"):
        return "shim"

    return "missing"
