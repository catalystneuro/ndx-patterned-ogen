import os
from pynwb import load_namespaces, get_class

try:
    from importlib.resources import files
except ImportError:
    # TODO: Remove when python 3.9 becomes the new minimum
    from importlib_resources import files

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-patterned-ogen.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-patterned-ogen.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-patterned-ogen")`
OptogeneticStimulusPattern = get_class("OptogeneticStimulusPattern", "ndx-patterned-ogen")
PatternedOptogeneticMethod = get_class("PatternedOptogeneticMethod", "ndx-patterned-ogen")
PatternedOptogeneticStimulusTable = get_class("PatternedOptogeneticStimulusTable", "ndx-patterned-ogen")
SpiralScanning = get_class("SpiralScanning", "ndx-patterned-ogen")
TemporalFocusing = get_class("TemporalFocusing", "ndx-patterned-ogen")
SpatialLightModulator = get_class("SpatialLightModulator", "ndx-patterned-ogen")
LightSource = get_class("LightSource", "ndx-patterned-ogen")
Hologram = get_class("Hologram", "ndx-patterned-ogen")
# Remove these functions from the package
del load_namespaces, get_class
