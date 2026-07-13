import re


def _extract_list(block: str, key: str):
    m = re.search(
        rf"{key}\s*:\s*\[(.*?)\]",
        block,
        flags=re.S,
    )

    if not m:
        return []

    return re.findall(r'"([^"]+)"', m.group(1))


def _extract_bool(block: str, key: str):
    m = re.search(
        rf"{key}\s*:\s*(true|false)",
        block,
    )

    if not m:
        return None

    return m.group(1) == "true"


def _extract_string(block: str, key: str):
    m = re.search(
        rf'{key}\s*:\s*"([^"]+)"',
        block,
    )

    if not m:
        return None

    return m.group(1)


def parse_android_bp(path):
    modules = {}

    with open(path, encoding="utf-8") as f:
        text = f.read()

    blocks = re.findall(
        r"(cc_[^{]+?\{.*?\n\})",
        text,
        flags=re.S,
    )

    for block in blocks:

        name = _extract_string(block, "name")

        if not name:
            continue

        modules[name] = {
            "name": name,
            "stem": _extract_string(block, "stem"),
            "srcs": _extract_list(block, "srcs"),
            "shared_libs": _extract_list(block, "shared_libs"),
            "allow_undefined_symbols": _extract_bool(
                block,
                "allow_undefined_symbols",
            ),
            "check_elf_files": _extract_bool(
                block,
                "check_elf_files",
            ),
        }

    return modules
