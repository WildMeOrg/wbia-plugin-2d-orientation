# IBEIS 2D Orientation Plugin
An ibeis plugin wrapper for https://github.com/hgrov52/2D-Orientation-v2#plugin

# Requirements

* OpenCV (cv2)

# Installation

Install this plugin as a Python module using

```bash
cd ~/code/ibeis-2d-orientation-module/
pip install -e .
```

With the plugin installed, register the module name with the `IBEISControl.py` file
in the ibeis repository located at `ibeis/ibeis/control/IBEISControl.py`.  Register
the module by adding the string (for example, `ibeis_2d_orientation`) to the
list `AUTOLOAD_PLUGIN_MODNAMES`.

# Example
```
$ python
>>> import ibeis_2d_orientation
>>> ibeis_2d_orientation._plugin.ibeis_plugin_2d_orientation_example(None)
```