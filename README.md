# IBEIS 2D Orientation Plug-in
An ibeis plug-in wrapper for https://github.com/hgrov52/2D-Orientation-v2#plugin

![Image of Predictions](###)

# Requirements

* OpenCV (cv2)
* PyTorch and TorchVision
* Numpy
* Pandas
* Matlotlib
* IBEIS and related dependencies: ibeis, utool, vtool, dtool, plottool
* TQDM
* ArgParse
* SciKit Learn and SciKit Image

# Installation

Install this plug-in as a Python module using

```bash
cd ~/code/ibeis-2d-orientation-module/
pip install -e .
```

With the plug-in installed, register the module name with the `IBEISControl.py` file
in the ibeis repository located at `ibeis/ibeis/control/IBEISControl.py`.  Register
the module by adding the string (for example, `ibeis_2d_orientation`) to the
list `AUTOLOAD_PLUGIN_MODNAMES`.

Alternatively, you can start an IBEIS 

# Example
```
$ python -m ibeis_2d_orientation._plugin --test-ibeis_plugin_orientation_2d_render_examples
```