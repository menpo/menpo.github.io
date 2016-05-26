<center>
  <img src="../../logo/menpofit_white_medium.png" alt="menpofit" width="30%"><br/>
  <strong style="font-size: 250%">menpofit</strong>
</center>

`menpofit` is a Python package for building, fitting and manipulating state-of-the-art 2D deformable models. In practice, `menpofit` is providing solutions to the following problems:

#### Affine Image Alignment
> An Affine Image Alignment algorithm aims to find the optimal alignment between an input image and a template image with respect to the parameters of an affine transform.

The methods that are implemented in `menpofit` are:
- **Lucas-Kanade (LK)**
  - _Optimization Algorithms:_ Forward Additive, Forward/Inverse Compositional
  - _Residuals:_ SSD, Fourier SSD, ECC, Gradient Correlation, Gradient Images


#### Deformable Image Alignment
> Deformable Image Alignment aims to get the otpimal alignment between an input image and a template image with respect to the parameters of a statistical parametric shape model.

The methods that are implemented in `menpofit` are:
- **Active Template Model (ATM)**
  - _Model Variants:_ Holistic, Patch-based, Masked, Linear, Linear Masked
  - _Optimization Algorithm:_ Lucas-Kanade Gradient Descent


#### Landmark Localization
A deformable object is commonly represented with a set of landmarks which correspond to semantically meaningful parts.

> Landmark Localization is the problem of localizing the landmark points that correspond to a deformable model in an input image.

The models that are implemented in `menpofit` are:
- **Active Appearance Model (AAM)**
  - _Model Variants:_ Holistic, Patch-based, Masked, Linear, Linear Masked
  - _Optimization Algorithms:_ Lucas-Kanade, Cascaded-Regression
- **Active Pictorial Structures (APS)**
  - _Model Variant:_ Generative
  - _Optimization Algorithm:_ Weighted Gauss-Newton Optimisation with fixed Jacobian and Hessian
- **Constrained Local Model (CLM)**
  - Active Shape Model
  - Regularised Landmark Mean Shift
- **Ensemble of Regression Trees (ERT)**
  - \[provided by [DLib](http://dlib.net/ "dlib C++ Library")\]
- **Supervised Descent Method (SDM)**
  - _Model Variants:_ Non Parametric, Parametric Shape, Parametric Appearance, Fully Parametric

Please see the [References](references.md "List of implemented papers.") for an indicative list of papers that are implemented in `menpofit`.
