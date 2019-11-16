<html>
<style>
div.noshow { display: none; }
div.bibtex {
	margin-right: 0%;
	margin-top: 1.2em;
	margin-bottom: 1em;
	border: 1px solid silver;
	padding: 0em 1em;
	background: #f9fcff;
}
div.bibtex pre { font-size: 60%; overflow: auto;  width: 100%; padding: 0em 0em;}</style>
<script type="text/javascript">
    function toggleBibtex(articleid) {
        var bib = document.getElementById('bib_'+articleid);
        if (bib) {
            if(bib.className.indexOf('bibtex') != -1) {
                bib.className.indexOf('noshow') == -1?bib.className = 'bibtex noshow':bib.className = 'bibtex';
            }
        } else {
            return;
        }
    }
</script>
</html>

Frequently Asked Questions (FAQ)
================================

  - [What license is Menpo under?](#what-license-is-menpo-under)
  - [How do I cite Menpo?](#citation)
  - [How do I install a development version?](#how-do-i-install-a-development-version)
  - [Can I use the Menpo Project as a black box to detect landmarks on facial images?](#pre_trained_models)
  - [Why 'Menpo'?](#why_menpo)

---------------------------------------

### What license is the Menpo Project under? {#what-license-is-menpo-under}
The Menpo Project is under the 3-clause BSD license which can be found
[here](https://github.com/menpo/menpo/blob/master/LICENSE.txt). This means
that you are free to use Menpo Project's packages (`menpo`, `menpofit`, menpo3d`) in commercial products as long as you retain
our copyright notice and do not use the *Imperial College London* name to promote your product.
The license of `menpodetect` is subject to the licenses of the packages that are wrapped.
Please see the [Menpo Team](team.md) for a list of contributors.


### How do I cite the Menpo Project? {#citation}
A description of the Menpo Project was presented in the [ACM Multimedia 2014](http://acmmm.org/2014/) conference.
Therefore, this publication is the reference paper to cite if you use any package of the Menpo Project within **any academic paper**.

> J. Alabort-i-Medina<sup font-size: 75%;	line-height: 0;	position: relative; vertical-align: baseline; top: -0.5em;>\*</sup>,
> E. Antonakos<sup font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; top: -0.5em;>\*</sup>,
> J. Booth<sup>\*</sup>, P. Snape<sup>\*</sup>, and S. Zafeiriou. _(\* Joint first authorship)_<br/>
> **Menpo: A Comprehensive Platform for Parametric Image Alignment and Visual Deformable Models**,
> *In Proceedings of the ACM International Conference on Multimedia, MM ’14*, New York, NY, USA, pp. 679-682, 2014. ACM.<br/>
[<a href="../menpo14.pdf"><font color="1A75FF">pdf</font></a>]
[<a href="javascript:toggleBibtex('menpo14')"><font color="1A75FF">bibtex</font></a>]
<div id="bib_menpo14" class="bibtex noshow">
<pre>
@inproceedings{menpo14,
author = { {Alabort-i-Medina}, Joan and Antonakos, Epameinondas and Booth, James and Snape, Patrick and Zafeiriou, Stefanos},
title = {Menpo: A Comprehensive Platform for Parametric Image Alignment and Visual Deformable Models},
booktitle = {Proceedings of the ACM International Conference on Multimedia},
series = {MM '14},
year = {2014},
isbn = {978-1-4503-3063-3},
location = {Orlando, FL, USA},
pages = {679--682},
numpages = {4},
url = {http://doi.acm.org/10.1145/2647868.2654890},
doi = {10.1145/2647868.2654890},
acmid = {2654890},
publisher = {ACM},
address = {New York, NY, USA}
}
</pre>
</div>

We request that if you do use the Menpo Project for an academic publication within any displicine that you cite the above paper!


### How do I install a development version? {#how-do-i-install-a-development-version}
Please see the [Setting Up A Development Environment](/installation/development.md) guide.


### Can I use the Menpo Project as a black box to detect landmarks on facial images? {#pre_trained_models}
The Menpo Project provides a command line tool for automatic state-of-the-art landmark detection on facial images using pre-trained models. For more information, please refer to the [`menpocli`](/menpocli/index.md) package. However, note that the purpose of the Menpo Project is to provide solutions for modelling any deformable object; _there is nothing specific at all to human face_.


### Why 'Menpo'? {#why_menpo}

> Menpo were facial armours which covered all or part of the face and provided
> a way to secure the top-heavy kabuto (helmet). The Shinobi-no-o (chin cord)
> of the kabuto would be tied under the chin of the menpo. There were small
> hooks called ori-kugi or posts called odome located on various places to
> help secure the kabuto's chin cord.
>
> --- [Wikipedia, Menpo](https://en.wikipedia.org/wiki/Mempo)
