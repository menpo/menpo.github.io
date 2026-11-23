---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Migrating to menpo 0.13

menpo 0.13 changes how PCA models are trimmed, and the packages that use them (menpofit, menpo3d, menpowidgets) follow. This page lists what
breaks and what to write instead. The full list of changes is in each package's changelog:
[menpo](https://menpo.readthedocs.io/en/latest/changelog.html),
[menpofit](https://menpofit.readthedocs.io/en/latest/changelog.html),
[menpo3d](https://menpo3d.readthedocs.io/en/latest/changelog.html) and
[menpowidgets](https://menpowidgets.readthedocs.io/en/latest/changelog.html).

The packages need each other at the matching versions: menpofit, menpo3d and menpowidgets require `menpo>=0.13`.

## PCA models are not modified any more

A model's arrays are never written to. Anything that changes a model returns a new one, or, for the `*_inplace` methods, rebinds the model to new arrays.
That is what makes it safe to share a trained model between fitters, and it is why the active-components API had to go.

| Before (0.12) | Now (0.13) |
|---|---|
| `model.n_active_components = n` | `model = model.trim_components(n)` |
| `model.trim_components(n)` (which trimmed in place) | `model.trim_components_inplace(n)`, or use the returned model of `trim_components(n)` |
| `model.n_active_components` | `model.n_components` (the components that the model has) |
| `model.components = array` (setter) | build a new model, or `model.trim_components(n)` |
| `model.increment(...)` on `PCAModel` | build the model again, or use `PCAModel.increment`'s replacement (see the menpo changelog) |

```{warning}
`trim_components(n)` used to change the model it was called on, and now returns the trimmed model instead. Old code that calls it and ignores the
result silently does nothing.
```

```{code-cell} ipython3
import numpy as np
from menpo.model import PCAModel
from menpo.shape import PointCloud

rng = np.random.RandomState(0)
model = PCAModel([PointCloud(rng.randn(10, 2)) for _ in range(20)])

small = model.trim_components(5)
print(model.n_components, small.n_components)        # the original is untouched

print(hasattr(model, "n_active_components"))         # False: removed
print(hasattr(model, "trim_components_inplace"))
```

## menpofit

* Fitters take `n_shape` and `n_appearance` as before, but work on a *trimmed copy* of the model, so the model you pass in is no longer changed by constructing a fitter.
  The copy is `fitter.aam` (or `fitter.atm`, `fitter.clm`...).
* `menpofit.checks.trimmed_copy(model, **n)` is the helper that does it, if you write your own fitter.
* `OrthoPDM`/`GlobalPDM` have `trim_components(n)` and no `n_active_components`.

## menpo3d

* The morphable model fitters and `MultilinearModel` use trimmed models. `ShapeModel.project` no longer sets and restores `n_active_components`.
* The viewers use moderngl instead of Mayavi, see [menpo3d](menpo3d/index.md).

## menpowidgets

The widgets read the number of components in use with `len(model.eigenvalues)`. The widget functions were renamed when the Mayavi widgets became 3D widgets:

```{code-cell} ipython3
import menpowidgets

renames = {
    "visualize_pointclouds": "visualize_shapes_2d",
    "visualize_shape_model": "visualize_shape_model_2d",
    "visualize_fitting_result": "visualize_fitting_results",
}
rows = ["| Before | Now | Exists |", "|---|---|---|"]
for old, new in renames.items():
    rows.append("| `{}` | `{}` | {} |".format(old, new, "yes" if hasattr(menpowidgets, new) else "NO"))
    assert not hasattr(menpowidgets, old), old
from IPython.display import Markdown
Markdown("\n".join(rows))
```

New 3D widgets: `visualize_shapes_3d`, `visualize_landmarks_3d`, `visualize_meshes_3d`, `visualize_shape_model_3d` and `visualize_morphable_model`.

## Landmark files import as a dictionary of groups

`menpo.io.import_landmark_file(path)` returns a dictionary `{group: PointCloud}`. Pass `group='PTS'` to get the shape itself, as in the [Point Distribution Model](menpofit/pdm.md) guide.
The old guides used `landmark_group['all']`, which raises a `KeyError` now: the key is the name of the group in the file (`'PTS'` for `.pts` files). They also used `.lms` to get the points of a landmark group;
landmark groups are plain point clouds now, so `.lms` is not needed (it is kept as an alias).
