from vendorcheck.hashcheck import check_hashes
from vendorcheck.fixups import parse_fixups
from vendorcheck.elf import analyze_blob
from vendorcheck.androidbp import parse_android_bp
from vendorcheck.index import build_bp_index
from vendorcheck.compatibility import check_blob
from vendorcheck.resolver import resolve_undefined
from vendorcheck.dependency import check_needed
from vendorcheck.suggestions import suggest
from vendorcheck.resolverdb import build_library_db
from vendorcheck.romindex import build_rom_index


class Analyzer:

    def __init__(
        self,
        blobs,
        vendor,
        extract,
        bp,
        rom=None,
        elf=True,
    ):
        self.blobs = blobs
        self.vendor = vendor
        self.extract = extract
        self.bp = bp
        self.rom = rom
        self.rom_index = None
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

        if self.rom:
            self.rom_index = build_rom_index(
                self.rom,
        )
    
        if self.elf:

            # Analyze every ELF
            for blob in self.blobs:
                analyze_blob(blob, self.vendor)

            # Build library database
            self.library_db = build_library_db(
                self.blobs,
                self.modules,
            )

            # Resolve symbols
            self.symbol_map = resolve_undefined(
                self.blobs,
            )

            # Check DT_NEEDED
            self.missing_libs = check_needed(
                self.blobs,
                self.library_db,
            )

            for blob in self.blobs:
                blob.missing_libs = self.missing_libs.get(
                    blob.path,
                    [],
                )

            # Compatibility + Suggestions
            self.compatibility = []

            for blob in self.blobs:

                blob.suggestions = suggest(
                    blob,
                    self.src_index,
                )

                self.compatibility.append(
                    check_blob(
                        blob,
                        self.src_index,
                    )
                )

        return self
