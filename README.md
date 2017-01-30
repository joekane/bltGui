# bltGUI  (Formerly bltColor)

![Example](/example.png)

A GUI Module for BearLibTerminal

## Features:

### bltColor
* Set alpha of a color.
* Multiply by float.
* Multiply two colors.
* Add two colors.
* Subtract two colors.
* Blend two colors with a bias.
* Generate a custom gradient using color_map
This class is fully compatible with any function that BLT wants a color parameter, including [color] formatting tags.

### bltControls
* Buttons
* Radio butttons
* Checkboxes
* Sliders
* TextBoxes
* List Boxes

### bltFrames
* Can contain a list of controls
* Draggable
* Resizable
* Show/Hide

### Skins
* Each control is fuly skinable
* Glyphs are stored in one set
* Color sets in another

### Additional Features
* Controls can Publish and Subscribe to changes made from any other control
* All elements are only drawn when updated (or dirty)

