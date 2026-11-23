"""MediaPipe Face Landmarker (478 points) to the 68 point iBUG layout, on Catmull-Rom curves.

For every iBUG contour (spline68.CONT) a ring or line of MediaPipe landmarks follows the same facial
curve. The anchors of the contour are the MediaPipe points that correspond to them; everything else is
placed on the Catmull-Rom curve through the MediaPipe points, at the mean arc-length fractions of the
300-W annotators (mean_fractions_300w.json). The iBUG order of the points along each contour, and the
person's right being the image's left, are kept.
"""
import json
from pathlib import Path

import numpy as np

from spline68 import CONT, resample

MEAN_FRACTIONS = {int(k): v for k, v in json.loads((Path(__file__).parent / "mean_fractions_300w.json").read_text())["mean"].items()}

# per contour, in the order of spline68.CONT: the MediaPipe landmarks of the curve (ordered like the iBUG
# points) and, for each anchor of the contour, which MediaPipe landmark it is.
JAW = [234, 93, 132, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454]
RIGHT_EYE = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
LEFT_EYE = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
OUTER_LIP = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]
INNER_LIP = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
CURVES = [
    JAW,
    [70, 63, 105, 66, 107],          # right eyebrow, outer end to inner end
    [336, 296, 334, 293, 300],       # left eyebrow, inner end to outer end
    [168, 6, 197, 195, 5, 4],        # nose bridge, between the eyes to the tip
    [98, 97, 2, 326, 327],           # under the nose, right nostril to left nostril
    RIGHT_EYE,
    LEFT_EYE,
    OUTER_LIP,
    INNER_LIP,
]
ANCHOR_LANDMARKS = [
    [234, 152, 454],
    [70, 107],
    [336, 300],
    [168, 4],
    [98, 2, 327],
    [33, 133],
    [362, 263],
    [61, 0, 291, 17],
    [78, 13, 308, 14],
]


def mediapipe_to_68(points):
    """points: (478, 2) MediaPipe landmarks in pixels. Returns the 68 iBUG points (68, 2)."""
    shape = np.zeros((68, 2))
    for (pts, closed, anchors), curve, anchor_lms in zip(CONT, CURVES, ANCHOR_LANDMARKS):
        controls = points[curve]
        slots = [curve.index(lm) for lm in anchor_lms]
        for number, position in resample(controls, closed, anchors, slots, pts, MEAN_FRACTIONS).items():
            shape[number] = position
    return shape
