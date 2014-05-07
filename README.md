OctoBlend
=========

Blender addon for sending models to an [OctoPrint](http://octoprint.org) server

Requirements
------------

- OctoPrint development version with Cura support enabled
- Blender 2.70 (probably works with older versions as well)

Configuration
-------------

- Add the octoblend-folder to your addons directory. Detailed instructions can be found [here](http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Add-Ons)
- Start blender with a fresh scene
- Open the user preferences and search for octoblend in the addons tab
- Enable the addon and configure server name and api key for OctoPrint
- Save user preferences

Usage
-----

- Select an object
- Run the "Send to OctoPrint" operator (just hit spacebar and search for "octo")

Notes
-----

- Object is exported in world-space coordinates
- 1 blender unit = 1 mm
- Uploaded file will be named after the active object.

Known issues
------------

On windows, Blender shows an error dialog when loading the addon the first time each session. This is a known [bug](https://developer.blender.org/T35379), and will be resolved in upcoming releases of Blender. Just ignore the error. It should work anyway.
