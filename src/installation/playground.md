
<link rel="stylesheet" type="text/css"  href="menpoinstall.css">
<style>
.download_button {
  background: rgb(103, 167, 243);
  color: white;
  margin: 5px 15px;
  padding: 12px;
  border: none;
  box-shadow: 2px 2px 5px #C7C7C7;
  height: 50px;
  width: 150px;
  font-weight: 300;
  font-size: large;
  transition: all .2s ease-in-out;
}
.download_button_container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-around;
}
</style>
<center>
  <div class="header_container">
    <strong style="font-size: 200%; font-family: 'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif; font-weight: 500;">Menpo Playground</strong>
    <div class="menpochoose">an isolated, standalone build of Menpo.</div>
    <div class="menpochoose">choose your operating system.</div>
    <br>
    <div class="download_button_container">
        <a style="text-decoration: none; color: grey" href="http://static.menpo.org/playground/mac/menpo_playground.tar.xz" download>
          <div class="download_button">OS X</div>
        </a>
        <a style="text-decoration: none; color: grey" href="http://static.menpo.org/playground/linux64/menpo_playground.tar.xz" download>
          <div class="download_button">Linux 64 bit</div>
        </a>
        <a style="text-decoration: none; color: grey" href="http://static.menpo.org/playground/win64/menpo_playground.zip" download>
          <div class="download_button">Windows 64 bit</div>
        </a>
    </div>
  </div>
</center>
<br>
A Menpo Playground is an archived directory you can download that contains:

1. A full isolated Python installation containing the Menpo Project with all its dependencies ready to go
2. A set of notebooks that you can run immediately to see how to use Menpo
3. Two command line tools, `menpofit`, and `menpodetect` (provided by [`menpocli`](../menpocli/index.md)), that can be used to locate bounding boxes and landmarks in challenging in-the-wild facial images
4. Detailed documentation on how to use the provided tools

There is no installation procedure for a playground, just download, extract, and use. When you are done with it, just delete the folder.

A playground is great from newcomers to Menpo, or just for anyone needing a hassle-free standalone build of Menpo (say, to deploy on a server).
