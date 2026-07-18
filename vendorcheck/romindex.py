import os

from vendorcheck.androidbp import parse_android_bp
from vendorcheck.index import build_bp_index


class RomIndex:

    def __init__(self):
        self.modules = {}
        self.names = {}
        self.srcs = {}

    def scan(self, root):

        for path, _, files in os.walk(root):

            if "Android.bp" not in files:
                continue

            bp = os.path.join(path, "Android.bp")

            try:
                mods = parse_android_bp(bp)

                if isinstance(mods, dict):
                    self.modules.update(mods)
                else:
                    for m in mods:
                        self.modules[m["name"]] = m

            except Exception:
                pass

        self.names, self.srcs = build_bp_index(self.modules)
