Snap Mode
=========

The landmarker is now by default in the new *snap* mode which will select the landmark closest to the mouse and display visual guides to help locate the target.

The currently selected landmark is highlighted in pink in the viewport and in the right sidebar as well. This selection changes as you move the mouse. In order to lock the current selected landmark, hold the `ctrl` key while moving your mouse: the landmark closest to the mouse will be maintained as long as you keep the key down.

![Snap mode in action](http://i.imgur.com/zxHyVLV.gif)

Once a landmark is selected this way, (left) clicking anywhere will move it to the specified location. This also applies to clicking on the landmark which will nudge it (instead of deselecting as before).

Clicking on a landmark and dragging it still works as expected.

This mode can be disabled by hitting the *e* key or using the switch in the options panel (bottom right). The alternative is similar to how the tool worked before this version by disabling auto-selection and targeting help.

### Inserting new landmarks

**Insertion is now strictly a right click action** which will insert the next unset landmark at the specified location. The next landmark is marked by a white underline in the left sidebar.

You can change the next inserted landmark by clicking on an unset landmark in the right sidebar. The insertion pointer will auto increment to the next logical landmark in the current landmark group, or the next available landmark in the whole set.

### Group editing

In addition to selecting a group by holding `shift` + dragging the mouse, we have added 3 ways to select a set of landmarks:

+ Double click on landmark in the left sidebar will select the entire group this landmark belongs to (the line)
+ `shift` + click in the left sidebar will select all landmarks
+ As long as one landmark is selected (this includes the closest to the mouse as introduced by snap mode), you can hit *g* to complete the group(s), this will select all landmarks in groups which already have selected landmarks

As it was previously the case, `ctrl`/`cmd` + click on a landmark will also start a group selection and hitting `a` will select all landmarks.

Once a set of landmarks has been selected you can drag from any of them as well as use the arrow keys on your keyboard to translate them. You can get out of the group selection by hitting `esc`, `q` or left clicking anywhere that is not a landmark.

### Asset switching

You can now click on the asset id in the top left to be presented with a prompt, you can then enter a valid asset number (from 1 to the number on the right) to directly go to a specific asset.

### New version notifications

As we use caching to make sure your browser doesn't re-download the code needlessly it may happen that the landmarker starts quickly from a cached version while a new version is downloaded in the background. In this case, a top banner will be displayed as soon as the new version is ready and you can reload the landmarker by clicking on the banner.
