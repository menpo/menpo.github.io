"""The 68-point iBUG layout as centripetal Catmull-Rom curves with fixed anchors.

Adapted from probes/p_spline_floor.py of the olp-cr work: each facial contour is a centripetal
Catmull-Rom curve through its points; the anchors (contour ends, eye corners, mouth corners, lip
middles...) stay where they are, and the points between two anchors sit at a fixed fraction of the
arc length between them. The fractions are the convention of the annotators, learned from
annotated faces (learn_fractions.py).
"""
import numpy as np

# (iBUG point numbers of the contour, closed?, anchors among them)
CONT = [
    (list(range(0, 17)), False, [0, 8, 16]),     # jaw
    (list(range(17, 22)), False, [17, 21]),      # right eyebrow (image left)
    (list(range(22, 27)), False, [22, 26]),      # left eyebrow
    (list(range(27, 31)), False, [27, 30]),      # nose bridge
    (list(range(31, 36)), False, [31, 33, 35]),  # nose bottom
    (list(range(36, 42)), True, [36, 39]),       # right eye
    (list(range(42, 48)), True, [42, 45]),       # left eye
    (list(range(48, 60)), True, [48, 51, 54, 57]),   # outer lip
    (list(range(60, 68)), True, [60, 62, 64, 66]),   # inner lip
]


def catmull(P, closed, n=40):
    """Centripetal Catmull-Rom through P (m,2): the dense curve (M,2) and the index of each control point in it."""
    Q = np.concatenate([P[-1:], P, P[:2]]) if closed else np.concatenate([2 * P[:1] - P[1:2], P, 2 * P[-1:] - P[-2:-1]])
    segs = len(P) if closed else len(P) - 1
    out, idx = [], []
    for i in range(segs):
        p0, p1, p2, p3 = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
        t0 = 0.0
        t1 = t0 + max(np.linalg.norm(p1 - p0), 1e-6) ** 0.5
        t2 = t1 + max(np.linalg.norm(p2 - p1), 1e-6) ** 0.5
        t3 = t2 + max(np.linalg.norm(p3 - p2), 1e-6) ** 0.5
        t = np.linspace(t1, t2, n, endpoint=False)[:, None]
        A1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
        A2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
        A3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
        B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
        B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
        idx.append(len(out) * n)
        out.append((t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2)
    D = np.concatenate(out)
    if closed:
        D = np.concatenate([D, D[:1]])
        idx.append(len(D) - 1)
    else:
        D = np.concatenate([D, P[-1:]])
        idx.append(len(D) - 1)
    return D, np.array(idx)


def arc_positions(D):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(D, axis=0), axis=1))])


def fractions(S):
    """{iBUG point: arc-length fraction within its anchor interval} for a 68-point shape S (68,2)."""
    result = {}
    for pts, closed, anchors in CONT:
        D, ci = catmull(S[pts], closed)
        sc = arc_positions(D)[ci]
        order = pts + ([pts[0]] if closed else [])
        a_pos = [order.index(a) for a in anchors] + ([len(order) - 1] if closed else [])
        for j in range(len(a_pos) - 1):
            lo, hi = a_pos[j], a_pos[j + 1]
            for k in range(lo + 1, hi):
                result[order[k]] = (sc[k] - sc[lo]) / max(sc[hi] - sc[lo], 1e-9)
    return result


def resample(controls, closed, anchors, anchor_slots, pts, mean_fractions):
    """The iBUG points of a contour on a curve that goes through ``controls`` (m,2).

    anchors: iBUG numbers of the anchors, in order along the contour; anchor_slots: for each, the index
    in ``controls`` of the point that is that anchor. The interior points are placed at the mean fractions.
    """
    D, ci = catmull(np.asarray(controls, dtype=float), closed)
    s = arc_positions(D)
    sc = s[ci]
    order = pts + ([pts[0]] if closed else [])
    out = {}
    slots = list(anchor_slots) + ([len(controls)] if closed else [])  # closed: back to the first anchor
    for a, slot in zip(anchors, anchor_slots):
        out[a] = np.asarray(controls[slot], dtype=float)
    a_pos = [order.index(a) for a in anchors] + ([len(order) - 1] if closed else [])
    for j in range(len(a_pos) - 1):
        lo_arc, hi_arc = sc[slots[j]], sc[slots[j + 1]]
        for k in range(a_pos[j] + 1, a_pos[j + 1]):
            target = lo_arc + mean_fractions[order[k]] * (hi_arc - lo_arc)
            out[order[k]] = np.array([np.interp(target, s, D[:, 0]), np.interp(target, s, D[:, 1])])
    return out
