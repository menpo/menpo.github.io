"""Learn the mean arc-length fraction of every interior iBUG point from annotated faces.

    python learn_fractions.py /path/to/300W/01_Indoor /path/to/300W/02_Outdoor ...   > mean_fractions.json
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

from spline68 import fractions


def read_pts(path):
    text = Path(path).read_text()
    body = text[text.index("{") + 1 : text.index("}")]
    return np.array([[float(v) for v in line.split()] for line in body.strip().splitlines()])


all_fractions = {}
n = 0
for folder in sys.argv[1:]:
    for path in sorted(Path(folder).glob("*.pts")):
        shape = read_pts(path)
        if shape.shape != (68, 2):
            continue
        n += 1
        for point, f in fractions(shape).items():
            all_fractions.setdefault(point, []).append(f)
print(json.dumps({"n_images": n, "mean": {str(k): float(np.mean(v)) for k, v in sorted(all_fractions.items())},
                  "std": {str(k): float(np.std(v)) for k, v in sorted(all_fractions.items())}}, indent=1))
