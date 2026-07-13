import os

from vendorcheck.androidbp import parse_android_bp
from vendorcheck.index import build_bp_index


def build_rom_index(root):
    """
    Scan the whole ROM for Android.bp files.
    """

    modules = {}

    for path, _, files in os.walk(root):

        if "Android.bp" not in files:
            continue

        bp = os.path.join(path, "Android.bp")

        try:
            parsed = parse_android_bp(bp)
            modules.update(parsed)

        except Exception:
            pass

    names, srcs = build_bp_index(modules)

    return {
        "modules": modules,
        "names": names,
        "srcs": srcs,
    }
