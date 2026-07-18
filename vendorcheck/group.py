from collections import defaultdict


def group_missing(blobs):
    """
    Group missing DT_NEEDED libraries by library name.

    Returns:
    {
        "libfoo.so": [
            "vendor/bin/foo",
            "vendor/lib64/bar.so",
        ],
        ...
    }
    """

    groups = defaultdict(list)

    for blob in blobs:

        if not getattr(blob, "is_elf", False):
            continue

        for lib in getattr(blob, "missing_libs", []):

            groups[lib].append(blob.path)

    return dict(groups)


def group_fixups(blobs):
    """
    Group blobs that have extract-files.py fixups.

    Returns:
    {
        "replace_needed(...)": [
            "vendor/bin/foo",
            ...
        ]
    }
    """

    groups = defaultdict(list)

    for blob in blobs:

        if not getattr(blob, "has_fixup", False):
            continue

        for fixup in getattr(blob, "fixups", []):

            groups[fixup].append(blob.path)

    return dict(groups)


def group_module_scores(compatibility):
    """
    Group Android.bp modules by compatibility score.

    Returns:
    {
        100: ["libfoo", "libbar"],
        90:  ["camera.qcom"],
        ...
    }
    """

    groups = defaultdict(list)

    for result in compatibility:

        module = result.get("module")

        if module is None:
            continue

        score = result.get("score", 0)

        groups[score].append(module)

    return dict(groups)
