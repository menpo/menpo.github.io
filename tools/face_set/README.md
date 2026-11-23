# The face set of the examples

The examples that train and fit models need annotated faces. This folder builds that set: about 49
images of the FairFace validation split (K. Karkkainen and J. Joo, CC BY 4.0), seven per race group of the
dataset, chosen by a seeded draw, with 68 iBUG landmarks.

FairFace has no landmarks, so they start as MediaPipe Face Landmarker output (Apache-2.0) and are meant to be
**corrected by hand**. MediaPipe's own points are not the iBUG points, so they are mapped onto the 68 point layout
with the convention of the 300-W annotators:

* every facial contour of the layout is a centripetal Catmull-Rom curve (`spline68.py`, from the olp-cr probes);
* the anchors (contour ends, eye corners, mouth corners, lip middles) are the MediaPipe points that correspond to them;
* the points between two anchors sit at the mean fraction of the arc length between them, learned from the 600 images of
  300-W (`learn_fractions.py`, `mean_fractions_300w.json`).

```
python learn_fractions.py /path/to/300W/01_Indoor /path/to/300W/02_Outdoor > mean_fractions_300w.json
python build_face_set.py validation.parquet face_landmarker.task OUT_DIR 49
```

`validation.parquet` is `0.25/validation-*.parquet` of https://huggingface.co/datasets/HuggingFaceM4/FairFace and
`face_landmarker.task` the float16 model from `storage.googleapis.com/mediapipe-models/face_landmarker/`.
Needs `mediapipe==0.10.21`, `pyarrow`, `pandas`, `pillow`. (mediapipe 1.2.x was killed with SIGKILL while creating the
landmarker on the machine this was written on, with 65 MB in use; 0.10.21 works. It needs numpy < 2, hence `pyarrow<20`.)
