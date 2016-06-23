Landmark Localization
=====================
A deformable object is commonly represented with a set of landmarks points which correspond to semantically meaningful parts.
Landmark Localization is the problem of localizing these landmark points that correspond to a deformable object in an input image.
This problem is commonly faced by training a deformable model of the object and try to fit it to the test image.

The methods that are currently implemented in `menpofit` are:
- [Active Appearance Model (AAM)](aam.md)
  - _Model Variants:_ Holistic, Patch-based, Masked, Linear, Linear Masked
  - _Optimization Algorithms:_ Lucas-Kanade, Cascaded-Regression
- [Active Pictorial Structures (APS)](aps.md)
  - _Model Variant:_ Generative
  - _Optimization Algorithm:_ Weighted Gauss-Newton Optimisation with fixed Jacobian and Hessian
- [Constrained Local Model (CLM)](clm.md)
  - Active Shape Model
  - Regularised Landmark Mean Shift
- [Ensemble of Regression Trees (ERT)](ert.md)
  - \[provided by [DLib](http://dlib.net/ "dlib C++ Library")\]
- [Supervised Descent Method (SDM)](sdm.md)
  - _Model Variants:_ Non Parametric, Parametric Shape, Parametric Appearance, Fully Parametric
