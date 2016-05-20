<center>
  <img src="../../img/logo/menpo.png" alt="menpofit" width="30%"><br/>
  <strong style="font-size: 250%">menpofit</strong>
</center>

`menpofit` is a Python package for building, fitting and manipulating state-of-the-art 2D deformable models. In practice, `menpofit` is providing solutions to the following problems:

### Affine Image Alignment
An Affine Image Alignment algorithm aims to find the optimal alignment between an input image and a template image with respect to the parameters of an affine transform.


### Deformable Image Alignment
Deformable Image Alignment aims to get the otpimal alignment between an input image and a template image with respect to the parameters of a statistical parametric shape model.

### Landmark Localization
A deformable object is commonly represented with a set of landmarks which correspond to semantically meaningful parts. Landmark Localization is the problem of localizing the landmark points that correspond to a deformable model in an input image.





It includes state-of-the-art deformable modelling techniques implemented on top of the **Menpo** project. Currently, the techniques that have been implemented include:

-   Active Appearance Model (AAM) &lt;api-aam-index&gt;
    -   Holistic &lt;menpofit-aam-HolisticAAM&gt;, Patch-based &lt;menpofit-aam-PatchAAM&gt;, Masked &lt;menpofit-aam-MaskedAAM&gt;, Linear &lt;menpofit-aam-LinearAAM&gt;, Linear Masked &lt;menpofit-aam-LinearMaskedAAM&gt;
    -   Lucas-Kanade Optimisation
    -   Cascaded-Regression Optimisation
-   Active Pictorial Structures (APS) &lt;api-aps-index&gt;
    -   Weighted Gauss-Newton Optimisation with fixed Jacobian and Hessian
-   Active Template Model (ATM) &lt;api-atm-index&gt;
    -   Holistic &lt;menpofit-atm-HolisticATM&gt;, Patch-based &lt;menpofit-atm-PatchATM&gt;, Masked &lt;menpofit-atm-MaskedATM&gt;, Linear &lt;menpofit-atm-LinearATM&gt;, Linear Masked &lt;menpofit-atm-LinearMaskedATM&gt;
    -   Lucas-Kanade Optimisation
-   Lucas-Kanade Image Alignment (LK) &lt;api-lk-index&gt;
    -   Forward Additive, Forward Compositional, Inverse Additive, Inverse Compositional
    -   Residuals: SSD, Fourier SSD, ECC, Gradient Correlation, Gradient Images
-   Constrained Local Model (CLM) &lt;api-clm-index&gt;
    -   Active Shape Model
    -   Regularised Landmark Mean Shift
-   Ensemble of Regression Trees (ERT) &lt;api-dlib-index&gt; \[provided by [DLib](http://dlib.net/)\]
-   Supervised Descent Method (SDM) &lt;api-sdm-index&gt;
    -   Non Parametric
    -   Parametric Shape
    -   Parametric Appearance
    -   Fully Parametric

Please see the to References &lt;ug-references&gt; for an indicative list of papers that are relevant to the methods implemented in MenpoFit.
