Deformable Image Alignment
==========================
A Deformable Image Alignment algorithm aims to find the optimal alignment between an
input image and a template image with respect to the parameters of a parametric shape model.

The method that is implemented in `menpofit` is:
- [Active Template Model (ATM)](atm.md)
  - _Model Variants:_ Holistic, Patch-based, Masked, Linear, Linear Masked
  - _Optimization Algorithm:_ Lucas-Kanade Gradient Descent (Forward/Inverse Compositional)
