from vendorcheck.hashcheck import check_hashes
from vendorcheck.fixups import parse_fixups
from vendorcheck.elf import analyze_blob
from vendorcheck.androidbp import parse_android_bp
from vendorcheck.index import build_bp_index
from vendorcheck.compatibility import check_blob
from vendorcheck.resolver import resolve_undefined
from vendorcheck.dependency import check_needed


class Analyzer:

    def __init__(self, blobs, vendor, extract, bp, elf=True):
        self.blobs = blobs
        self.vendor = vendor
        self.extract = extract
        self.bp = bp
        self.elf = elf

        self.modules = {}
        self.src_index = {}
        self.symbol_map = {}
        self.missing_libs = {}
        self.compatibility = []

    def run(self):

        # SHA verification
        check_hashes(self.blobs, self.vendor)

        # Parse blob fixups
        fixups = parse_fixups(self.extract)

        for blob in self.blobs:
            if blob.path in fixups:
                blob.has_fixup = True
                blob.fixups = fixups[blob.path]

        # Parse Android.bp
        self.modules = parse_android_bp(self.bp)
        _, self.src_index = build_bp_index(self.modules)

        if self.elf:

            # Analyze every ELF
            for blob in self.blobs:
                analyze_blob(blob, self.vendor)

            # Resolve undefined symbols
            self.symbol_map = resolve_undefined(self.blobs)

            # Check DT_NEEDED
            self.missing_libs = check_needed(self.blobs)

            # Compatibility
            self.compatibility = []

            for blob in self.blobs:
                self.compatibility.append(
                    check_blob(
                        blob,
                        self.src_index,
                    )
                )

        return self
