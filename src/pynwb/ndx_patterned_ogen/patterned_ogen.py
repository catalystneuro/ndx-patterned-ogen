from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from hdmf.utils import docval, getargs, popargs, popargs_to_dict, get_docval
from pynwb import register_class
from pynwb.base import TimeSeries
from pynwb.core import DynamicTable, DynamicTableRegion, VectorData
from pynwb.device import Device
from pynwb.file import NWBContainer, LabMetaData, TimeIntervals
from pynwb.ogen import OptogeneticStimulusSite

namespace = "ndx-patterned-ogen"


@register_class("SpatialLightModulator", namespace)
class SpatialLightModulator(Device):
    """
    Spatial light modulator used in the experiment.
    """

    __nwbfields__ = ("model", "size")

    @docval(
        {"name": "name", "type": str, "doc": "Name of SpatialLightModulator object. "},
        *get_docval(Device.__init__, "description", "manufacturer"),
        {"name": "model", "type": str, "doc": "Model of SpatialLightModulator."},
        {
            "name": "size",
            "type": Iterable,
            "doc": (
                "Resolution of SpatialLightModulator (in pixels), formatted as [width, height] or [width, height, "
                "depth]."
            ),
            "default": None,
            "shape": ((2,), (3,)),
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("model", "size")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("LightSource", namespace)
class LightSource(Device):
    """
    Light source used in the experiment.
    """

    __nwbfields__ = (
        "model",
        "stimulation_wavelength",
        "peak_power",
        "peak_pulse_energy",
        "intensity",
        "pulse_rate",
        "exposure_time",
    )

    @docval(
        {"name": "name", "type": str, "doc": "Name of LightSource object."},
        *get_docval(Device.__init__, "description", "manufacturer"),
        {"name": "model", "type": str, "doc": "Model of LightSource."},
        {
            "name": "stimulation_wavelength",
            "type": (int, float),
            "doc": "Excitation wavelength of stimulation light (nanometers).",
            "default": None,
        },
        {
            "name": "peak_power",
            "type": (int, float),
            "doc": "Incident power of stimulation device (in Watts).",
            "default": None,
        },
        {
            "name": "peak_pulse_energy",
            "type": (int, float),
            "doc": "If device is pulsed laser, pulse energy (in Joules).",
            "default": None,
        },
        {
            "name": "intensity",
            "type": (int, float),
            "doc": "intensity of the excitation, if known (in W/mm^2).",
            "default": None,
        },
        {
            "name": "pulse_rate",
            "type": (int, float),
            "doc": "If device is pulsed laser, pulse rate (in Hz) used for stimulation.",
            "default": None,
        },
        {"name": "exposure_time", "type": (int, float), "doc": "Exposure time of the sample (in sec)", "default": None},
    )
    def __init__(self, **kwargs):
        keys_to_set = (
            "model",
            "stimulation_wavelength",
            "peak_power",
            "peak_pulse_energy",
            "intensity",
            "pulse_rate",
            "exposure_time",
        )
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("PatternedOptogeneticStimulusSite", namespace)
class PatternedOptogeneticStimulusSite(OptogeneticStimulusSite):
    """
    Patterned optogenetic stimulus site.
    """

    __nwbfields__ = ("effector", "spatial_light_modulator", "light_source")

    @docval(
        *get_docval(OptogeneticStimulusSite.__init__, "name", "description", "device", "location", "excitation_lambda"),
        {
            "name": "effector",
            "type": str,
            "doc": "Light-activated effector protein expressed by the targeted cell (eg. ChR2).",
            "default": None,
        },
        {
            "name": "spatial_light_modulator",
            "type": SpatialLightModulator,
            "doc": "SpatialLightModulator used to generate holographic pattern.",
        },
        {"name": "light_source", "type": LightSource, "doc": "LightSource used to apply photostimulation."},
    )
    def __init__(self, **kwargs):
        keys_to_set = ("effector", "spatial_light_modulator", "light_source")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)

    @docval(
        {
            "name": "spatial_light_modulator",
            "type": SpatialLightModulator,
            "doc": "SpatialLightModulator used to generate holographic pattern. ",
        }
    )
    def add_spatial_light_modulator(self, spatial_light_modulator):
        """
        Add a spatial light modulator to the photostimulation method.
        """
        if self.spatial_light_modulator is not None:
            raise ValueError("SpatialLightMonitor already exists in this PatternedOptogeneticStimulusSite container.")
        else:
            self.spatial_light_modulator = spatial_light_modulator

    @docval({"name": "light_source", "type": LightSource, "doc": "LightSource used to apply photostimulation."})
    def add_light_source(self, light_source):
        """
        Add a light_source to the photostimulation method.
        """

        if self.light_source is not None:
            raise ValueError("LightSource already exists in this PatternedOptogeneticStimulusSite container.")
        else:
            self.light_source = light_source


@register_class("OptogeneticStimulusTarget", namespace)
class OptogeneticStimulusTarget(LabMetaData):
    """
    Container to store the targated rois in a photostimulation experiment.
    """

    __nwbfields__ = (
        {"name": "stimulated_rois", "child": True},
        "additional_targeted_rois",
    )

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "stimulated_rois",
            "type": DynamicTableRegion,
            "doc": "a table region corresponding to the ROIs that were targeted and stimulated",
        },
        {
            "name": "additional_targeted_rois",
            "type": Iterable,
            "doc": (
                "additional targeted ROIs designated as a list specifying the pixel ([x1, y1], [x2, y2], …) or"
                " voxel ([x1, y1, z1], [x2, y2, z2], …) centroid of each ROI"
            ),
            "default": None,
            "shape": ((None, 2), (None, 3)),
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("stimulated_rois", "additional_targeted_rois")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("OptogeneticStimulusPattern", namespace)
class OptogeneticStimulusPattern(LabMetaData):
    """
    Container to store the information about a generic stimulus pattern (spatial information)
    """

    __nwbfields__ = ("description", "sweep_size", "sweep_mask")

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "description",
            "type": str,
            "doc": (
                "Scanning or scanless method for shaping optogenetic light "
                "(ex., diffraction limited points,3D shot, disks, etc.)."
            ),
        },
        {
            "name": "sweep_size",
            "type": (int, float, Iterable),
            "doc": (
                "Size of the scanning sweep pattern in micrometers. If a scalar is provided, the sweep pattern is"
                " assumed to be a circle (for 2D patterns) or cylinder (for 3D patterns), with diameter 'sweep_size'."
                " If 'sweep_size' is a two or three dimensional array, the the sweep pattern is assumed to be a"
                " rectangle or cuboid, with dimensions [width, height] or [width, height, depth]."
            ),
            "default": None,
        },
        {
            "name": "sweep_mask",
            "type": Iterable,
            "doc": (
                "Scanning sweep pattern designated using a mask of size [width, height] (2D stimulation) or [width,"
                " height, depth] (3D stimulation), where for a given pixel a value of 1 indicates stimulation, and a"
                " value of 0 indicates no stimulation."
            ),
            "default": None,
            "shape": ([None] * 2, [None] * 3),
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("description", "sweep_size", "sweep_mask")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("TemporalFocusing", namespace)
class TemporalFocusing(LabMetaData):
    """
    Container to store the parameters defining a temporal focusing beam-shaping
    """

    __nwbfields__ = ("description", "lateral_point_spread_function", "axial_point_spread_function")

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "description",
            "type": str,
            "doc": "description of the pattern",
            "default": None,
        },
        {
            "name": "lateral_point_spread_function",
            "type": str,
            "doc": "estimated lateral spatial profile or point spread function, expressed as mean [um] ± s.d [um].",
            "default": None,
        },
        {
            "name": "axial_point_spread_function",
            "type": str,
            "doc": "estimated axial spatial profile or point spread function, expressed as mean [um] ± s.d [um].",
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("description", "lateral_point_spread_function", "axial_point_spread_function")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("SpiralScanning", namespace)
class SpiralScanning(LabMetaData):
    """
    Container to store the parameters defining a spiral scanning pattern
    """

    __nwbfields__ = ("description", "diameter", "height", "number_of_revolutions")

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "description",
            "type": str,
            "doc": "description of the pattern",
            "default": None,
        },
        {
            "name": "diameter",
            "type": (int, float),
            "doc": "spiral diameter of each sweep (in micrometers)",
            "default": None,
        },
        {
            "name": "height",
            "type": (int, float),
            "doc": "spiral height of each sweep (in micrometers)",
            "default": None,
        },
        {
            "name": "number_of_revolutions",
            "type": int,
            "doc": "number of turns within a spiral",
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("description", "diameter", "height", "number_of_revolutions")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("PatternedOptogeneticStimulusTable", namespace)
class PatternedOptogeneticStimulusTable(TimeIntervals):
    """
    Parameters corresponding to events of patterned optogenetic stimulation with indicated targeted rois.
    """

    __fields__ = ()
    __columns__ = (
        {"name": "start_time", "description": "Start time of stimulation, in seconds", "required": True},
        {"name": "stop_time", "description": "Stop time of stimulation, in seconds", "required": True},
        {
            "name": "power",
            "description": "Power (in Watts) applied to each target during patterned photostimulation.",
            "required": True,
        },
        {
            "name": "frequency",
            "description": "Frequency of stimulation if the stimulus delivered is pulsed (in Hz)",
            "required": False,
        },
        {
            "name": "pulse_width",
            "description": "Pulse width of stimulation if the stimulus delivered is pulsed, in seconds/phase",
            "required": False,
        },
        {"name": "targets", "description": "Targeted rois for the stimulus onset", "required": True},
        {
            "name": "stimulus_pattern",
            "description": "link to the stimulus pattern",
            "required": True,
        },
        {
            "name": "stimulus_site",
            "description": "link to the stimulus site",
            "required": True,
        },
    )

    @docval(
        {
            "name": "name",
            "type": str,
            "doc": "Name of this PatternedOptogeneticStimulusTable",
            "default": "PatternedOptogeneticStimulusTable",
        },
        {
            "name": "description",
            "type": str,
            "doc": "Description of what is in this PatternedOptogeneticStimulusTable",
            "default": "stimulation parameters",
        },
        *get_docval(TimeIntervals.__init__, "id", "columns", "colnames"),
    )
    def __init__(self, **kwargs):
        keys_to_set = ()
        args_to_set = popargs_to_dict(keys_to_set, kwargs)

        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)

    @docval(
        {"name": "start_time", "doc": "Start time of stimulation, in seconds", "type": float},
        {"name": "stop_time", "doc": "Stop time of stimulation, in seconds", "type": float},
        {
            "name": "power",
            "doc": "Power (in Watts) applied to each target during patterned photostimulation.",
            "type": (int, float, Iterable),
            "default": 0.0,
        },
        {
            "name": "frequency",
            "doc": "Frequency of stimulation if the stimulus delivered is pulsed (in Hz)",
            "type": (int, float, Iterable),
            "default": 0.0,
        },
        {
            "name": "pulse_width",
            "doc": "Pulse width of stimulation if the stimulus delivered is pulsed, in seconds/phase",
            "type": (int, float, Iterable),
            "default": 0.0,
        },
        {
            "name": "targets",
            "doc": "Targeted rois for the stimulus onset",
            "type": OptogeneticStimulusTarget,
        },
        {
            "name": "stimulus_pattern",
            "doc": "link to the stimulus pattern",
            "type": (OptogeneticStimulusPattern, TemporalFocusing, SpiralScanning),
        },
        {
            "name": "stimulus_site",
            "doc": "link to the stimulus site",
            "type": PatternedOptogeneticStimulusSite,
        },
        allow_extra=True,
    )
    def add_interval(self, **kwargs):
        """
        Add a stimulation parameters for a specific run.
        """
        super(PatternedOptogeneticStimulusTable, self).add_interval(**kwargs)
