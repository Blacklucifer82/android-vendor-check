from vendorcheck.bpverify import verify_bp
from vendorcheck.index import find_module


def check_blob(blob, src_index):
    """
    Analyze one blob and return compatibility information.
    """

    result = {
        "module": None,
        "bp": None,
        "score": 0,
    }

    module = find_module(blob, src_index)

    if module is None:
        return result

    result["module"] = module["name"]

    bp = verify_bp(blob, module)

    result["bp"] = bp

    score = 100

    score -= len(bp["missing"]) * 10
    score -= len(bp["unused"]) * 5

    if score < 0:
        score = 0

    result["score"] = score

    return result
