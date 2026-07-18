import json


def export_json(path, analysis):
    data = {
        "health": analysis.health,
        "stats": dict(analysis.stats),
        "compatibility": analysis.compatibility,
        "missing_libs": analysis.missing_libs,
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=4)
