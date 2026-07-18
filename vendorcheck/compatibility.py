from vendorcheck.bpverify import verify_bp
from vendorcheck.index import find_module


def calculate_score(bp):
    """
    Calculate Android.bp compatibility score.

    Penalties:
      -10 for each missing shared_lib
      -5  for each unused shared_lib

    Score is clamped between 0 and 100.
    """

    score = 100

    score -= len(bp["missing"]) * 10
    score -= len(bp["unused"]) * 5

    if score < 0:
        score = 0

    return score


def check_blob(blob, src_index):
    """
    Analyze one blob against Android.bp.

    Returns:
    {
        "module": str | None,
        "bp": {
            "missing": [],
            "unused": [],
        } | None,
        "score": int,
    }
    """

    result = {
        "module": None,
        "bp": None,
        "score": 0,
    }

    #
    # Find Android.bp module
    #
    module = find_module(blob, src_index)

    if module is None:
        return result

    result["module"] = module["name"]

    #
    # Verify shared_libs
    #
    bp = verify_bp(blob, module)

    result["bp"] = bp

    #
    # Calculate compatibility score
    #
    score = calculate_score(bp)

    result["score"] = score

    #
    # Store on blob for later reporting
    #
    blob.module_name = module["name"]
    blob.compatibility_score = score

    return result
