Affine Image Alignment
======================
An Affine Image Alignment algorithm aims to find the optimal alignment between an
input image and a template image with respect to the parameters of an affine transform.

The method that is implemented in `menpofit` is:
- [Lucas-Kanade (LK)](lk.md)
  - _Optimization Algorithms:_ Forward Additive, Forward/Inverse Compositional
  - _Residuals:_ SSD, Fourier SSD, ECC, Gradient Correlation, Gradient Images
