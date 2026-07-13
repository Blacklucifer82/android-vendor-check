import os
import re
import subprocess


def run_readelf(path: str) -> str:
    """
    Return readelf output for an ELF.
    """
    return subprocess.check_output(
        ["readelf", "-dWs", path],
        text=True,
        stderr=subprocess.DEVNULL,
    )


def parse_soname(blob, elf_output: str):
    """
    Populate blob.soname from readelf output.
    """

    blob.soname = None

    for line in elf_output.splitlines():

        m = re.search(r"Library soname: \[(.*?)\]", line)

        if not m:
            continue

        blob.soname = os.path.basename(
            m.group(1)
        )

        return

def parse_needed(blob, elf_output: str):
    """
    Populate blob.needed from readelf output.
    """

    blob.needed.clear()

    for line in elf_output.splitlines():

        m = re.search(r"Shared library: \[(.*?)\]", line)

        if m:
            blob.needed.add(m.group(1))


def parse_undefined(blob, elf_output: str):
    """
    Populate blob.undefined with undefined symbols.
    """

    blob.undefined.clear()

    for line in elf_output.splitlines():

        if " UND " not in line:
            continue

        m = re.match(
            r"\s*\d+:\s+[0-9a-fA-F]+\s+\d+\s+\S+\s+\S+\s+\S+\s+UND\s+(.+)",
            line,
        )

        if not m:
            continue

        symbol = m.group(1)
        symbol = symbol.split("@")[0].strip()

        blob.undefined.add(symbol)


def parse_exports(blob, elf_output: str):
    """
    Populate blob.exports with exported symbols.
    """

    blob.exports.clear()

    for line in elf_output.splitlines():

        if " UND " in line:
            continue

        m = re.match(
            r"\s*\d+:\s+[0-9a-fA-F]+\s+\d+\s+\S+\s+GLOBAL\s+\S+\s+\S+\s+(.+)",
            line,
        )

        if not m:
            continue

        symbol = m.group(1)
        symbol = symbol.split("@")[0].strip()

        if symbol:
            blob.exports.add(symbol)


def analyze_blob(blob, vendor_root):
    """
    Analyze one ELF blob.
    """

    full_path = os.path.join(vendor_root, blob.path)

    if not os.path.isfile(full_path):
        return

    try:
        elf = run_readelf(full_path)
    except Exception:
        # Not an ELF or readelf failed
        return

    blob.is_elf = True

    parse_soname(blob, elf)
    parse_needed(blob, elf)
    parse_undefined(blob, elf)
    parse_exports(blob, elf)
