import os


def find_module(blob, src_index):
    """
    Find Android.bp module corresponding to a blob.
    """

    name = os.path.basename(blob.path)

    return src_index.get(name)


def build_bp_index(modules):
    """
    Build indexes for Android.bp modules.
    """

    by_name = {}
    by_src = {}

    for module in modules.values():

        by_name[module["name"]] = module

        for src in module["srcs"]:

            src = os.path.basename(src)

            by_src[src] = module

    return by_name, by_src
