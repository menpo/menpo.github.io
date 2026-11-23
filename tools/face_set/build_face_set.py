"""Select faces from the FairFace validation split and annotate them with MediaPipe on iBUG curves.

    python build_face_set.py validation.parquet face_landmarker.task OUT_DIR [N]

FairFace (Karkkainen and Joo, 2021) is CC BY 4.0. Every image gets a .pts file with the 68 points; they
come from a detector, to be corrected by hand. The images are chosen to cover the seven race groups of the
dataset evenly, by a seeded random draw; faces the detector is unsure about or that look away are dropped.
"""
import io
import sys
from pathlib import Path

import mediapipe as mp
import numpy as np
import pyarrow.parquet as pq
from PIL import Image
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

from mp68 import mediapipe_to_68

parquet, model, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
n_total = int(sys.argv[4]) if len(sys.argv) > 4 else 49
out.mkdir(parents=True, exist_ok=True)

table = pq.read_table(parquet).to_pandas()
# the class names of the labels, from the file's own metadata
import json
NAMES = json.loads(pq.read_schema(parquet).metadata[b"huggingface"])["info"]["features"]
options = vision.FaceLandmarkerOptions(
    base_options=mp_python.BaseOptions(model_asset_path=model), num_faces=1,
    min_face_detection_confidence=0.7, min_face_presence_confidence=0.7)
landmarker = vision.FaceLandmarker.create_from_options(options)

rng = np.random.RandomState(0)
races = sorted(table["race"].unique())
per_race = n_total // len(races)
chosen = []
for race in races:
    rows = table[table["race"] == race]
    kept = 0
    for i in rng.permutation(len(rows)):
        if kept == per_race:
            break
        row = rows.iloc[i]
        image = Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
        result = landmarker.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(image)))
        if not result.face_landmarks:
            continue
        w, h = image.size
        pts = np.array([[p.x * w, p.y * h] for p in result.face_landmarks[0]])
        # frontal enough: the nose tip between the eye corners, and a face that is not tiny
        yaw = abs((pts[4, 0] - pts[33, 0]) / max(pts[263, 0] - pts[33, 0], 1) - 0.5)
        if yaw > 0.12 or (pts[263, 0] - pts[33, 0]) < 0.25 * w:
            continue
        shape = mediapipe_to_68(pts)
        name = f"fairface_{len(chosen):03d}"
        image.save(out / f"{name}.png")
        # menpo's pts layout: (x, y) with the first pixel at 0
        lines = "\n".join(f"{x:.3f} {y:.3f}" for x, y in shape)
        (out / f"{name}.pts").write_text(f"version: 1\nn_points: 68\n{{\n{lines}\n}}\n")
        chosen.append((name, race, row["age"], row["gender"]))
        kept += 1
(out / "ATTRIBUTION.txt").write_text(
    "Images: FairFace, K. Karkkainen and J. Joo, CC BY 4.0, https://huggingface.co/datasets/HuggingFaceM4/FairFace\n"
    "Landmarks: MediaPipe Face Landmarker (Apache-2.0) on Catmull-Rom curves of the iBUG layout, to be corrected by hand.\n\n"
    + "\n".join("{}: {}, age {}, gender {}".format(c[0], NAMES["race"]["names"][c[1]], NAMES["age"]["names"][c[2]], NAMES["gender"]["names"][c[3]]) for c in chosen) + "\n")
print(len(chosen), "faces in", out)
