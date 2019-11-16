Specifications
==============
`landmarker.io` uses simple JSON and YAML based file formats for describing landmarks and templates.

A template is a specification for future landmarks. It specifies how many landmarks should be placed, labels that should be attached to the landmarks, and any connectivity information for visualising groupings of landmarks.

1. [LJSON landmark file specification](#ljson)
2. [Template specification](#template)

---------------------------------------

### 1. LJSON landmark file specification {#ljson}
Landmarks are loaded and saved as `.ljson` files, as understood by the [`menpo`](../menpo/index.md) package. The current version of the format is `v2`.

You can see an example in the demo data for the landmarker ([https://github.com/menpo/landmarker.io/blob/master/api/v2/landmarks/james/ibug68.json](https://github.com/menpo/landmarker.io/blob/master/api/v2/landmarks/james/ibug68.json)).

Though a template is used to generate empty landmark files, the json file contains all the information necessary including the point groups and their labels.

#### Fields
The file contains a json object containing the following fields:

+  `landmarks` (object)
   + `points` (array) - the ordered locations of each points on the resource (2d or 3d as long as it consistent). Similar to the list of points in a `pts` file.
   + `connectivity`: (array) - list of tuples `[a, b]` where `a` and `b` are valid indices for 2 points which should appear connected.
+  `labels` (array of objects) - the `label` field is the name of the group, while the `mask` field is a list of the indices for the points which belong to this group, they do not need to be contiguous.
+  `version` (integer) - for validation.

#### JSON Schema
Here's a minimal [json schema](http://json-schema.org/) you can use to validate your files (see http://json-schema-validator.herokuapp.com/):

```.json
{
  "type": "object",
  "properties": {
    "landmarks": {
      "id": "landmarks",
      "type": "object",
      "properties": {
        "points": {
          "id": "points",
          "type": "array",
          "items": {
            "type": "array",
            "items": {
              "type": "number"
            }
          }
        },
        "connectivity": {
          "id": "connectivity",
          "type": "array",
          "items": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
              "type": "integer"
            }
          }
        }
      }
    },
    "labels": {
      "id": "labels",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": {
            "id": "label",
            "type": "string"
          },
          "mask": {
            "id": "mask",
            "type": "array",
            "items": {
              "type": "integer"
            }
          }
        }
      }
    },
    "version": {
      "id": "version",
      "type": "integer"
    }
  }
}
```


### 2. Template specification {#template}
Templates are YAML files which formalise a landmark set by specifying it's size, connectivity and labels.

The file must contain a `groups` array containing dictionaries. Each dictionary describe a group of landmarks with the fields:

+ `label` - the name of the group (required)
+ `points` - the number of points in the group (required)
+ `connectivity` - an array of tuples that can be of the form (where a and b are between 0 and the group size)
  + `a b` - a is connected to b
  + `a:b` - a is connected to a+1, which is connected to a+2, and so on until b

In order to get all points to be connected in a cycle, you can use the shortcut `connectivity: cycle`, which is equivalent to:

```.yaml
connectivity:
  - 0:size-1
  - size-1 0
```

_`json` files following the same structure are also valid templates for the landmarker client (although not for the server)_

#### Landmark files

**Ordering is important**: the template is used to generate / validate landmarks files, as such it is important to maintain consistency i.e if order of the groups is changed, the landmarks files will not correspond anymore.

As landmarks files contain all the information necessary, the landmarker will also accept `ljson` file as templates by inferring the template.

A cli script is available in `meta/template`, you can use it as such:

```.bash
./meta/template convert asset01.ljson dummy_template.yaml
```

to convert an `ljson` file into a valid `yaml` template. Read the top comment in the script file for more detailed usage information.

#### Examples

A minimal template with no groups:

```.yaml
groups:
  - label: all
    points: 36
```

A simple facial landmarks templates:

```.yaml
groups:
  - label: mouth
    points: 6
  - label: nose
    points: 3
    connectivity:
      - 0 1
      - 1 2
  - label: left_eye
    points: 8
    connectivity:
      - 0:7
      - 7 0
  - label: right_eye
    points: 8
    connectivity: cycle
  - label: chin
    points: 1
```
