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


Citing the Menpo Project
========================
If you are using the Menpo Project, please cite the following paper:

> J. Alabort-i-Medina<sup font-size: 75%;	line-height: 0;	position: relative; vertical-align: baseline; top: -0.5em;>\*</sup>, 
> E. Antonakos<sup font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; top: -0.5em;>\*</sup>, 
> J. Booth<sup>\*</sup>, P. Snape<sup>\*</sup>, and S. Zafeiriou. _(\* Joint first authorship)_<br/>
> **Menpo: A Comprehensive Platform for Parametric Image Alignment and Visual Deformable Models**,
> *In Proceedings of the ACM International Conference on Multimedia, MM ’14*, New York, NY, USA, pp. 679-682, 2014. ACM.<br/>
[<a href="citation/menpo14.pdf"><font color="1A75FF">pdf</font></a>]
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

<center>
  <img src="../img/logo/menpo_small.png" alt="The Menpo Project"><br/>
</center>
