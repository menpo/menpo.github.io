# User guide

1. <a href="#annotating_assets">Annotating assets</a>
2. <a href="#switching_assets">Switching assets and data source</a>
3. <a href="#annotating">Annotating</a>  
4. <a href="#view_options">View options</a>
5. <a href="#landmark_sidebar">Landmark sidebar</a>
6. <a href="#curves">Curves: spacing points and closing loops</a>
7. <a href="#fit">Fit: let a model place the landmarks</a>
8. <a href="#autosave">Autosave behaviour</a>
9. <a href="#shortcuts">Keyboard shortcuts</a>
10. <a href="#data_sources">Data sources</a>
11. <a href="#server">The landmarker server</a>
12. <a href="#security">Note on security</a>

---------------------------------------

<a id="annotating_assets"></a>

## 1. Annotating assets
The landmarker can be used to annotate either 2D assets (images) or 3D assets (meshes).

However, in its current state, it can currently only work in one 2 modes image or mesh and annotate the corresponding type of assets at any one time. (This is a legacy concern we plan to adress).

The annotations are saved as landmark groups compliant with a given template.

<a id="switching_assets"></a>

## 2. Switching assets and data source
Regardless of the data source, the assets are identifiable by their name (id) or by their index. They are organized into a collection in which you can navigate with the arrow buttons at the bottom of the screen or the `j` and `k` keys.

You can quickly identify this data in the top left of the screen and click on any of these elements to switch asset:

![](http://i.imgur.com/eERY2pm.png)

+ Data source (click to logout)
+ Collection name and current mode
+ Asset name
+ Asset index

If they appear greyed out, there is no possibility to change them (for example a one item collection will not allow changing the asset)

<a id="annotating"></a>

## 3. Annotating
_Video demonstrating everything to come soon_

Once logged in and working on an asset, landmarking is pretty straightforward:

+ Right click to insert a landmark if there exists an unset landmark
+ Left click to move the closest landmark (hold ctrl to lock to selected landmark)
+ Click and drag to move a landmark
+ Shift click + drag allows you to select a group of landmark that you can move by dragging them or using the arrow keys
+ Hold left click to rotate a mesh
+ Hold right click to translate the mesh or the image (left click as well for images)

<a id="view_options"></a>

## 4. View options
![](http://i.imgur.com/VVFVYd0.png)

Some view options are available in the bottom left corner of the screen to hide/show the texture of the mesh and the links between connected landmarks.

The `snap` setting will disable the auto selection of closest landmark as well as the visual feedback. This is useful in cases with densely packed landmarks where click and drag can be more precise.

The slider controls the size of the landmarks relative to the asset's dimensions. You can also update this in increments by hitting `+` or `-`.

On an image, a **zoom view** in the top right corner shows a magnified view of the area around the cursor, so that you can place a landmark to the pixel.

<a id="landmark_sidebar"></a>

## 5. Landmark sidebar
The sidebar in the bottom right of the screen mirrors what is happening on the screen. Landmarks in blue are existing landmarks, they are highlighted in purple once selected (by hovering near them or clicking them with snap disabled). Empty landmarks or in clear grey and the next one to be inserted is highlighted in orange. You can click on any empty landmark to set it to be inserted next, otherwise the default logic is to take the first available one from the top.

The top bar has undo / redo buttons on the left and the current template name on the right. You can click on the template name to change the template if applicable.

The save button, gives you the ability to save landmarks **remotely** and displays a red dot if there are any unsaved changes.

The download button will generate a json file of the current landmarks and initiate a download (on older browsers and Safari this will open a new tab/window with the json content).

If the current asset is not the first one in the collection, a `LOAD PREVIOUS` button is available, this will fetch the landmarks from the previous asset to replace the current set with. This is a destructive operation and can be undone, however for added security it will not save afterwards.

<a id="curves"></a>

## 6. Curves: spacing points and closing loops
Most of the groups of a face are curves: the jaw and the brows are chains, the eyes and the mouth are loops. Two tools work on the curves of the template (the lines of the *links*), so that you place a few points by hand and the rest follow:

+ **Space evenly** (`s`) moves the points of a curve to equal steps along it. The *anchors* of the curve stay where they are: by default the ends of a chain and the first point of a loop, or the points that the template names (the jaw ends and the chin, say). A template can also give where the other points go, for instance the mean spacing of the 300-W annotators; see the [specifications](specifications.md). The curve is a smooth (Catmull-Rom) spline through the points, which is what is drawn between them.
+ **Auto-space** (the switch in the top toolbar) does the same for the curves of a landmark each time you have moved it, as part of the same undo step.
+ **Snap to line** (`f`) closes every loop into one curve, like a shut eye or mouth: the two corners stay, and the points of the two lids meet half way between where they were, each pair exactly on top of each other. A curved lid stays curved.

Both act on the curves with a selected landmark, or on all of them if nothing is selected; the button says which (*Space selected (jaw)*). With snap mode on (see [Snap mode](snap_mode.md)) the landmark nearest to the mouse counts as selected, so to act on everything turn snap mode off (`e`) and press `q`. Each is a single undo step (`z`). When all the points of a loop are on top of each other in pairs you can drag a pair at once: select both with a box (`shift` + drag) and drag one.

<a id="fit"></a>

## 7. Fit: let a model place the landmarks
When the server was started with a model (`lmio image ./images --fit`; see [the server](server.md)), the **Fit…** button opens a panel for it. The server can have several models, and you choose between them:

+ **Models.** Each model has a status: *pretrained* (it fits already, and may say *pretrained + 6* for the images of yours it has learnt from), *learnt from 12*, *needs 8 images* (it has to learn first), or the job it is running.
+ **Fit this image** starts from the current landmarks if they are all placed, otherwise from a box you draw (**Draw a box…**) or from the model's own guess. **Start from the previous image's landmarks** is for the frames of a video. Nothing is saved: the result is on the screen like anything you have moved, and `z` takes it back.
+ **Compare models…** fits the image with two models and draws both (cyan and orange). Choose one to keep, or press `esc` to leave the landmarks as they were.
+ **Learn.** A model learns only from landmarks that you have **saved**, never from what it predicted. *Learn from this image* adds the saved image, *Learn from all annotations* trains on all of them, and *Learn from each image when I save it* does it on every save (off unless you ask).
+ **Pre-fit.** The server can fit all the images that have no landmarks, up front, so that each starts from a decent guess (for example MediaPipe on a set of faces, then an AAM that learns from the ones you correct). An image with such a *proposal* opens with the landmarks in place and a **predicted: model** mark, and its Save button is highlighted. **If it is right, save it as it is** (one click, `ctrl + s`): it becomes a normal saved image, reviewed, with the model recorded as `fitted_by`. A proposal that you leave unsaved stays a proposal.

<a id="autosave"></a>

## 8. Autosave behaviour
If the autosave switch is on (it is by default), anytime you leave an asset, the changes will be saved (you should see a notification in the center of the screen). This currently applies to navigating with `j/k`, the pager at the bottom or changing asset manually by clicking on the index or name.

An untouched proposal from a pre-fit counts as saved here: leaving it does not accept it, so save it when it is right.

If it is off, it will not be possible to leave an asset with unsaved changes, a confirmation modal will be displayed allowing to leave or go back and save. This adds security if you want to ensure that saving changes remotely is a conscious operation.

<a id="shortcuts"></a>

## 9. Keyboard shortcuts
A list of keyboard shortcuts is available by clicking the help button in the bottom right corner of the screen or hitting `?`. The main ones to be aware of are:

| Key | Action |
| --- | ------ |
| j / k | go to the next / previous asset |
| a | select all landmarks |
| q / ESC | deselect landmarks if applicable (`esc` also ends a Compare) |
| s | space the curves evenly between their anchors (the curves with a selected landmark, or all) |
| f | snap the loops (eyes, mouth) into one curve (the loops with a selected landmark, or all) |
| g | select all landmarks in a group with already selected landmarks |
| d | delete all selected landmarks |
| ctrl + s | save current landmark |
| z / y | undo / redo last operation |
| r | reset camera to it's default position |

<a id="data_sources"></a>

## 10. Data sources
The landmarker works with a **server** that holds your assets and keeps the landmarks (see [the server](server.md)), or in **demo** mode, which needs nothing
at all: open [`?server=demo`](https://menpo.github.io/landmarker.io/?server=demo) to annotate a textured 3D head. Choose one on the landing page, or give the
address in the URL as described next.

(Earlier versions could also annotate the files of a Dropbox folder. That needed a Dropbox app registered for the address of the site and is gone.)

<a id="server"></a>

## 11. The landmarker server
See [the server page](server.md) for running your own server: `pip install landmarkerio-server` and `lmio image ./my_images`.

You can access a server by clicking on the first button of the landing page and entering a URL in the prompt, or directly with the URL query string:

`https://menpo.github.io/landmarker.io/?server=SERVERURL&t=TEMPLATENAME&c=COLLECTIONNAME&i=ASSETINDEX`

Apart from the `server` parameter, which needs to be a valid and reachable URL, you can specify the template name with `t`, the collection name with `c` and the asset index
with `i` on load. If they are not specified or invalid (as in not present in the server's data), the landmarker will pick the first available item.

The mode is fetched automatically from the server.

The server generates empty landmark groups that follow the selected template when an asset has none. As such it is not possible to give a custom template when working from the server.

<a id="security"></a>

## 12. Note on security
The app is served over https, and a browser does not let an https page talk to a plain http server (this is called *mixed content*). There is one exception, which is the one that matters here:
**a server on your own machine** (`http://localhost:5000` or `http://127.0.0.1:5000`) is allowed. So the usual way of annotating your own files is to run `lmio` on your machine and open
`https://menpo.github.io/landmarker.io/?server=http://localhost:5000`. Chrome may ask you to allow the page to reach devices on your local network; the server answers
that request.

To use a server on another machine, give it an https address, or tunnel its port to your own machine with SSH (`ssh -L 5000:localhost:5000 host`) and use `localhost` as above.
