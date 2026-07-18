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
from vendorcheck.stats import collect_stats
from vendorcheck.health import calculate_health


class Analyzer:
    """
    Main analysis engine.

    Order of execution:

        SHA
          ↓
        blob_fixups
          ↓
        Android.bp
          ↓
        ELF analysis
          ↓
        Resolver DB
          ↓
        Undefined symbols
          ↓
        DT_NEEDED
          ↓
        Compatibility
          ↓
        Suggestions
          ↓
        Statistics
          ↓
        Health
    """

    def __init__(
        self,
        blobs,
        vendor,
        extract,
        bp,
        elf=True,
    ):
        self.blobs = blobs
        self.vendor = vendor
        self.extract = extract
        self.bp = bp
        self.elf = elf

        #
        # Android.bp
        #
        self.modules = {}
        self.src_index = {}

        #
        # Resolver
        #
        self.library_db = None
        self.symbol_map = {}

        #
        # Dependency results
        #
        self.missing_libs = {}

        #
        # Compatibility
        #
        self.compatibility = []

        #
        # Reports
        #
        self.stats = {}
        self.health = 0

    def run(self):
        """
        Execute complete analysis.
        """

        #
        # --------------------------------------------------
        # SHA verification
        # --------------------------------------------------
        #
        check_hashes(
            self.blobs,
            self.vendor,
        )

        #
        # --------------------------------------------------
        # Parse blob_fixups
        # --------------------------------------------------
        #
        fixups = parse_fixups(
            self.extract,
        )

        for blob in self.blobs:

            if blob.path in fixups:

                blob.has_fixup = True
                blob.fixups = fixups[blob.path]

        #
        # --------------------------------------------------
        # Parse Android.bp
        # --------------------------------------------------
        #
        self.modules = parse_android_bp(
            self.bp,
        )

        _, self.src_index = build_bp_index(
            self.modules,
        )

        #
        # --------------------------------------------------
        # Stop here if ELF analysis disabled
        # --------------------------------------------------
        #
        if not self.elf:
            return self

        #
        # --------------------------------------------------
        # Analyze every ELF blob
        # --------------------------------------------------
        #
        for blob in self.blobs:

            analyze_blob(
                blob,
                self.vendor,
            )

        #
        # --------------------------------------------------
        # Build library database
        # --------------------------------------------------
        #
        self.library_db = build_library_db(
            self.blobs,
            self.modules,
        )

        #
        # Make DB available to blobs
        #
        for blob in self.blobs:

            blob.library_db = self.library_db

        #
        # --------------------------------------------------
        # Resolve undefined symbols
        # --------------------------------------------------
        #
        self.symbol_map = resolve_undefined(
            self.blobs,
        )

        #
        # --------------------------------------------------
        # Check DT_NEEDED
        # --------------------------------------------------
        #
        self.missing_libs = check_needed(
            self.blobs,
            self.library_db,
        )

        for blob in self.blobs:

            blob.missing_libs = self.missing_libs.get(
                blob.path,
                [],
            )

        #
        # --------------------------------------------------
        # Android.bp compatibility
        # --------------------------------------------------
        #
        self.compatibility = []

        for blob in self.blobs:

            result = check_blob(
                blob,
                self.src_index,
            )

            self.compatibility.append(
                result,
            )

            blob.suggestions = suggest(
                blob,
                self.src_index,
            )

        #
        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------
        #
        self.stats = collect_stats(
            self.blobs,
        )

        #
        # --------------------------------------------------
        # Vendor health
        # --------------------------------------------------
        #
        self.health = calculate_health(
            self.blobs,
            self.compatibility,
        )

        return self
