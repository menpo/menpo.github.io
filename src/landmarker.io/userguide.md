User Guide
==========

1. [Annotating assets](#annotating_assets)
2. [Switching assets and data source](#switching_assets)
3. [Annotating](#annotating)  
4. [View options](#view_options)
5. [Landmark sidebar](#landmark_sidebar)
6. [Autosave behaviour](#autsave)
7. [Keyboard shortcuts](#shortcuts)
8. [Data sources](#data_sources)
9. [The landmarker server](#server)
10. [Dropbox](#dropbox)
11. [Note on security](#security)

---------------------------------------

### <a name="annotating_assets"></a>1. Annotating assets
The landmarker can be used to annotate either 2D assets (images) or 3D assets (meshes).

However, in its current state, it can currently only work in one 2 modes image or mesh and annotate the corresponding type of assets at any one time. (This is a legacy concern we plan to adress).

The annotations are saved as landmark groups compliant with a given template.

### <a name="switching_assets"></a>2. Switching assets and data source
Regardless of the data source, the assets are identifiable by their name (id) or by their index. They are organized into a collection in which you can navigate with the arrow buttons at the bottom of the screen or the `j` and `k` keys.

You can quickly identify this data in the top left of the screen and click on any of these elements to switch asset:

![](http://i.imgur.com/eERY2pm.png)

+ Data source (click to logout)
+ Collection name and current mode
+ Asset name
+ Asset index

If they appear greyed out, there is no possibility to change them (for example a one item collection will not allow changing the asset)

### <a name="annotating"></a>3. Annotating
_Video demonstrating everything to come soon_

Once logged in and working on an asset, landmarking is pretty straightforward:

+ Right click to insert a landmark if there exists an unset landmark
+ Left click to move the closest landmark (hold ctrl to lock to selected landmark)
+ Click and drag to move a landmark
+ Shift click + drag allows you to select a group of landmark that you can move by dragging them or using the arrow keys
+ Hold left click to rotate a mesh
+ Hold right click to translate the mesh or the image (left click as well for images)

### <a name="view_options"></a>4. View options
![](http://i.imgur.com/VVFVYd0.png)

Some view options are available in the bottom left corner of the screen to hide/show the texture of the mesh and the links between connected landmarks.

The `snap` setting will disable the auto selection of closest landmark as well as the visual feedback. This is useful in cases with densely packed landmarks where click and drag can be more precise.

The slider controls the size of the landmarks relative to the asset's dimensions. You can also update this in increments by hitting `+` or `-`.

### <a name="landmark_sidebar"></a>5. Landmark sidebar
The sidebar in the bottom right of the screen mirrors what is happening on the screen. Landmarks in blue are existing landmarks, they are highlighted in purple once selected (by hovering near them or clicking them with snap disabled). Empty landmarks or in clear grey and the next one to be inserted is highlighted in orange. You can click on any empty landmark to set it to be inserted next, otherwise the default logic is to take the first available one from the top.

The top bar has undo / redo buttons on the left and the current template name on the right. You can click on the template name to change the template if applicable.

The save button, gives you the ability to save landmarks **remotely** and displays a red dot if there are any unsaved changes.

The download button will generate a json file of the current landmarks and initiate a download (on older browsers and Safari this will open a new tab/window with the json content).

If the current asset is not the first one in the collection, a `LOAD PREVIOUS` button is available, this will fetch the landmarks from the previous asset to replace the current set with. This is a destructive operation and can be undone, however for added security it will not save afterwards.

### <a name="autosave"></a>6. Autosave behaviour
If the autosave switch is on (it is by default), anytime you leave an asset, the changes will be saved (you should see a notification in the center of the screen). This currently applies to navigating with `j/k`, the pager at the bottom or changing asset manually by clicking on the index or name.

If it is off, it will not be possible to leave an asset with unsaved changes, a confirmation modal will be displayed allowing to leave or go back and save. This adds security if you want to ensure that saving changes remotely is a conscious operation.

### <a name="shortcuts"></a>7. Keyboard shortcuts
A list of keyboard shortcuts is available by clicking the help button in the bottom right corner of the screen or hitting `?`. The main ones to be aware of are:

| Key | Action |
| --- | ------ |
| j / k | go to the next / previous asset |
| a | select all landmarks |
| q / ESC | deselect landmarks if applicable |
| g | select all landmarks in a group with already selected landmarks |
| d | delete all selected landmarks |
| ctrl + s | save current landmark |
| z / y | undo / redo last operation |
| r | reset camera to it's default position |

### <a name="data_sources"></a>8. Data sources
The landmarker currently supports 2 data sources: Dropbox and the original custom landmarker server. On first visit, you'll see this landing page:

![](http://i.imgur.com/FhRlSOH.png)

### <a name="server"></a>9. The landmarker server
See the [landmarker-server](https://github.com/menpo/landmarkerio-server) repo for info about running your own server.

You can access a server by clicking on the second button and entering a url in the subsequent prompt, or directly using the url query string:

`https://www.landmarker.io?server=SERVERURL&t=TEMPLATENAME&c=COLLECTIONNAME&i=ASSETINDEX`

Apart the `server` parameter which needs to be a valid and reachable url, you can specify the template name with `t`, collection name with `c` and asset index with `i` on load. If they are not specified or invalid (as in not present in the server's data), the landmarker will pick the first available item.

The mode is fetched automatically from the server.

The server will load templates by itself by generating empty landmark groups compliant with the selected template if none is present. As such it is not possible to specify custom template when working from the server.

### <a name="dropbox"></a>10. Dropbox
If you selected dropbox from the landing page, you'll be presented with a filepicker like this one:

![](http://i.imgur.com/VAbnSYh.png)

Select the type of assets you want to load (images / meshes), as well as the folder - you can can navigate down the true to check the content of the folder. Note that all assets of the selected types will be loaded.

Once this is done, one of the default templates will have been selected for you, you can change this template and / or import one from dropbox by clicking on the template name in the right sidebar and then on the `+` button. To avoid collisions, importing a template with the same name as one which already exits will import it with as `[name]-1` and so on, so you can work with different versions of a template.

Landmarks will be saved in the same folder under a `landmarks` folder with the scheme `[asset-name]_[template-name].ljson`

### <a name="security"></a>11. Note on security
The main application runs on a secure connection at [https://www.landmarker.io](https://www.landmarker.io), on this version we disallow using a non secure server in this mode due to the mixed content security concerns (see [this article](https://developer.mozilla.org/en/docs/Security/MixedContent) from Mozilla or [this one](http://www.howtogeek.com/181911/htg-explains-what-exactly-is-a-mixed-content-warning/) from How To Geek for more information).

As a result it is not possible to use a local server from this connection, however another version is deployed on a regular http connection at [http://insecure.landmarker.io/](http://insecure.landmarker.io/) which will allow it. This version will however not allow you to connect to dropbox which is only possible on the https version. You can use [ngrok](https://ngrok.com/) in order to expose a local server behind https.
