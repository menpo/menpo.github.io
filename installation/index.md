<style>
button:focus {
  outline: none;
}
a:hover {
  text-decoration: none;
}
.menpostrong {
  font-size: 200%; 
  font-family: 'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif; 
  font-weight: 500;
}
.menpochoose {
  margin-top: 30px;
}
.header_container {
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  flex-wrap: wrap; 
}
.header_columns {
  display: flex; 
  flex-direction: row; 
  flex-wrap: wrap;
  justify-content: center;
}
.column {
  max-width: 256px;
}
.install_card {
  border: none; 
  margin: 5px 15px;
  box-shadow: 2px 2px 5px #C7C7C7;
  flex: 1;
  height: 360px;
  transition: all .2s ease-in-out;
}
.install_card:hover { 
  transform: scale(1.05); 
}
.install_header {
  background: rgb(103, 167, 243); 
  color: white; 
  border: none; 
  padding: 12px; 
  font-weight: 300;
  font-size: large;
}
.install_card li {
  font-size: small;
  text-align: start;
  padding-bottom: 6px;
}
.install_body {
  padding: 5px;
  font-weight: 300;
}
.question {
  height: 86px;
  padding: 0 20px;
  margin-top: 30px;
}
.takeaway {
  margin-top: 15px;
  margin-bottom: 10px;
}
</style>
<center>
  <div class="header_container">
    <strong style="font-size: 200%; font-family: 'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif; font-weight: 500;">Installation</strong>
    <div class="menpochoose">choose an option to find out more.</div>
    <div class="header_columns">
      <div class="column">
        <div class="question">
          <b>new to Python?</b>
            <br>or<br>
          <b>want to quickly try menpo?</b>
        </div>
        <a style="text-decoration: none; color: grey" href="playground.html">
          <div class="install_card">
            <div class="install_header">playground</div>
            <div class="install_body">
              <ul>
                <li>Standalone build of menpo - everything you need in one folder</li>
                <li>No install - just download and use</li>
                <li>Includes pre-trained models, command line tools for face detection and landmark localization, and example notebooks</li>
                <li>Easy to migrate to a full conda installation when you are ready</li>
              </ul>
            </div>
          </div>
        </a>
        <div class="takeaway">isolated & hassle free</div>
      </div>
      <div class="column">
        <div class="question">
          <b>already use conda?</b>
            <br>or<br>
          <b>want to contribute?</b>
        </div>
        <a style="text-decoration: none; color: grey" href="conda.html">
          <div class="install_card">
            <div class="install_header">conda</div>
            <div class="install_body">
              <ul>
                <li>The Python distribution of choice for many researchers</li>
                <li>Quickly and easily install all of the Menpo Project</li>
                <li>Easily install more Python packages with conda and pip</li>
                <li>Define multiple isolated environments and switch between them easily</li>
                <li>Install development versions and contribute to menpo</li>
              </ul>
            </div>
          </div>
        </a>
        <div class="takeaway">flexible & powerful</div>
      </div>
      <div class="column">
        <div class="question">
        <b>have an existing non-conda install you want to use menpo with?</b>
        </div>
        <a style="text-decoration: none; color: grey" href="pip.html">
          <div class="install_card">
            <div class="install_header">pip</div>
            <div class="install_body">
              <ul>
                <li>Use the powerful menpo core library with your existing Python setup</li>
                <li>Great for deep learning researchers - benefit from menpo as a preprocessing library</li>
                <li>Currently limited to the menpo core library due to tricky dependencies for other parts of the project. Wish this weren’t the case? Let us know!</li>
              </ul>
            </div>
          </div>
        </a>
        <div class="takeaway">integrate with what you have</div>
      </div>
    </div>
  </div>
</center>
<br>

