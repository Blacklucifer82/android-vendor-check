def calculate_health(blobs, compatibility):
    """
    Calculate overall vendor health.

    Health is based only on blobs that have an Android.bp module.
    Blobs without modules (firmware, XMLs, APKs, etc.) are ignored.

    Returns:
        int (0-100)
    """

    scores = []

    for result in compatibility:

        #
        # Ignore blobs without Android.bp modules
        #
        if result.get("module") is None:
            continue

        scores.append(result.get("score", 0))

    #
    # Nothing to score
    #
    if not scores:
        return 100

    return round(sum(scores) / len(scores))
