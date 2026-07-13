def build_symbol_index(blobs):
    """
    Build a map:
        exported symbol -> list of blobs exporting it
    """
    index = {}

    for blob in blobs:
        if not blob.is_elf:
            continue

        for symbol in blob.exports:
            index.setdefault(symbol, []).append(blob)

    return index


def resolve_undefined(blobs):
    """
    Resolve undefined symbols to providers.
    """

    index = build_symbol_index(blobs)
    results = {}

    for blob in blobs:

        if not blob.is_elf:
            continue

        providers = {}

        for symbol in blob.undefined:

            providers[symbol] = index.get(symbol, [])

        results[blob.path] = providers

    return results
