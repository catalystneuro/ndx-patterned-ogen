from collections.abc import Iterable
from hdmf.utils import docval, popargs_to_dict, get_docval#, popargs
from pynwb import register_class
from pynwb.core import DynamicTableRegion
from pynwb.device import Device
from pynwb.file import LabMetaData, TimeIntervals
from pynwb.ogen import OptogeneticStimulusSite
import numpy as np

namespace = "ndx-patterned-ogen"


@register_class("SpatialLightModulator3D", namespace)
class SpatialLightModulator3D(Device):
    """
    Spatial light modulator used in the experiment.
    """

    __nwbfields__ = ("model", "spatial_resolution")

    @docval(
        {"name": "name", "type": str, "doc": "Name of SpatialLightModulator3D object."},
        *get_docval(Device.__init__, "description", "manufacturer"),
        {
            "name": "model",
            "type": str,
            "doc": "The model specification of the spatial light modulator (e.g. 'NeuraLight 3D Ultra', from Bruker).",
        },
        {
            "name": "spatial_resolution",
            "type": Iterable,
            "doc": "Resolution of spatial light modulator (in pixels), formatted as [width, height, depth].",
            "default": None,
            "shape": (3,),
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("model", "spatial_resolution")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("SpatialLightModulator2D", namespace)
class SpatialLightModulator2D(Device):
    """
    Spatial light modulator used in the experiment.
    """

    __nwbfields__ = ("model", "spatial_resolution")

    @docval(
        {"name": "name", "type": str, "doc": "Name of SpatialLightModulator3D object. "},
        *get_docval(Device.__init__, "description", "manufacturer"),
        {
            "name": "model",
            "type": str,
            "doc": "The model specification of the spatial light modulator (e.g. 'X15213 series', from Hamamatsu).",
        },
        {
            "name": "spatial_resolution",
            "type": Iterable,
            "doc": "Resolution of spatial light modulator (in pixels), formatted as [width, height].",
            "default": None,
            "shape": (2,),
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("model", "spatial_resolution")
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
        "filter_descriptionpeak_pulse_energy",
        "intensity",
        "pulse_rate",
        "exposure_time",
    )

    @docval(
        {"name": "name", "type": str, "doc": "Name of LightSource object."},
        *get_docval(Device.__init__, "description", "manufacturer"),
        {"name": "model", "type": str, "doc": "Model of light source device."},
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
            "name": "filter_description",
            "type": str,
            "doc": (
                "Filter used to obtain the excitation wavelength of stimulation light, e.g. 'Short pass at 1040 nm'."
            ),
            "default": None,
        },
        {
            "name": "peak_pulse_energy",
            "type": (int, float),
            "doc": "If device is pulsed light source, pulse energy (in Joules).",
            "default": None,
        },
        {
            "name": "intensity",
            "type": (int, float),
            "doc": "Intensity of the excitation in W/m^2, if known.",
            "default": None,
        },
        {
            "name": "pulse_rate",
            "type": (int, float),
            "doc": "If device is pulsed light source, pulse rate (in Hz) used for stimulation.",
            "default": None,
        },
        {"name": "exposure_time", "type": (int, float), "doc": "Exposure time of the sample (in sec)", "default": None},
    )
    def __init__(self, **kwargs):
        keys_to_set = (
            "model",
            "stimulation_wavelength",
            "peak_power",
            "filter_description",
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
            "type": (SpatialLightModulator3D, SpatialLightModulator2D),
            "doc": "Spatial light modulator used to generate photostimulation pattern.",
        },
        {"name": "light_source", "type": LightSource, "doc": "Light source used to apply photostimulation."},
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
            "type": (SpatialLightModulator3D, SpatialLightModulator2D),
            "doc": "Spatial light modulator used to generate photostimulation pattern. ",
        }
    )
    def add_spatial_light_modulator(self, spatial_light_modulator):
        """
        Add a spatial light modulator to the photostimulation method.
        """
        if self.spatial_light_modulator is not None:
            raise ValueError("SpatialLightModulator already exists in this PatternedOptogeneticStimulusSite container.")
        else:
            self.spatial_light_modulator = spatial_light_modulator

    @docval({"name": "light_source", "type": LightSource, "doc": "Light source used to apply photostimulation."})
    def add_light_source(self, light_source):
        """
        Add a light source to the photostimulation method.
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
        {"name": "targeted_rois", "child": True},
        {"name": "segmented_rois", "child": True},
    )

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "segmented_rois",
            "type": DynamicTableRegion,
            "doc": (
                "A table region referencing a PlaneSegmentation object storing segmented ROIs that receive"
                " photostimulation."
            ),
            "default": None,
        },
        {
            "name": "targeted_rois",
            "type": DynamicTableRegion,
            "doc": "A table region referencing a PlaneSegmentation object storing targeted ROIs.",
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("segmented_rois", "targeted_rois")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("OptogeneticStimulus2DPattern", namespace)
class OptogeneticStimulus2DPattern(LabMetaData):
    """
    Container to store the information about a generic 2D stimulus pattern (spatial information).
    """

    __nwbfields__ = ("description", "sweep_size", "sweep_mask")

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "description",
            "type": str,
            "doc": (
                "Description of the scanning or scanless method for shaping optogenetic light. Examples include"
                " diffraction limited points, 3D shot, disks, etc."
            ),
        },
        {
            "name": "sweep_size",
            "type": (int, float, Iterable),
            "doc": (
                "Size of the scanning sweep pattern in micrometers. If a scalar is provided, the sweep pattern is"
                " assumed to be a circle (for 2D patterns) with diameter 'sweep_size'."
                " If 'sweep_size' is a two dimensional array, the the sweep pattern is assumed to be a"
                " rectangle, with dimensions [width, height]."
            ),
            "default": None,
        },
        {
            "name": "sweep_mask",
            "type": Iterable,
            "doc": (
                "Scanning sweep pattern designated using a mask of size [width, height] for 2D stimulation,"
                " where for a given pixel a value of 1 indicates stimulation, and a"
                " value of 0 indicates no stimulation."
            ),
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = ("description", "sweep_size", "sweep_mask")
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)


@register_class("OptogeneticStimulus3DPattern", namespace)
class OptogeneticStimulus3DPattern(LabMetaData):
    """
    Container to store the information about a generic 3D stimulus pattern (spatial information).
    """

    __nwbfields__ = ("description", "sweep_size", "sweep_mask")

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "description",
            "type": str,
            "doc": (
                "Description of the scanning or scanless method for shaping optogenetic light. Examples include"
                " diffraction limited points, 3D shot, disks, etc."
            ),
        },
        {
            "name": "sweep_size",
            "type": (int, float, Iterable),
            "doc": (
                "Size of the scanning sweep pattern in micrometers. If a scalar is provided, the sweep pattern is"
                " assumed to be a cylinder (for 3D patterns), with diameter 'sweep_size'."
                " If 'sweep_size' is a three dimensional array, the the sweep pattern is assumed to be a"
                " cuboid, with dimensions [width, height, depth]."
            ),
            "default": None,
        },
        {
            "name": "sweep_mask",
            "type": Iterable,
            "doc": (
                "Scanning sweep pattern designated using a mask of size [width, height, depth] for 3D stimulation,"
                " where for a given pixel a value of 1 indicates stimulation, and a"
                " value of 0 indicates no stimulation."
            ),
            "default": None,
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
            "doc": "Describe any additional details about the pattern.",
            "default": None,
        },
        {
            "name": "lateral_point_spread_function",
            "type": str,
            "doc": "Estimated lateral spatial profile or point spread function, expressed as mean [um] ± s.d [um].",
            "default": None,
        },
        {
            "name": "axial_point_spread_function",
            "type": str,
            "doc": "Estimated axial spatial profile or point spread function, expressed as mean [um] ± s.d [um]",
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
    Container to store the parameters defining a spiral scanning pattern.
    """

    __nwbfields__ = ("description", "diameter", "height", "number_of_revolutions")

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "description",
            "type": str,
            "doc": "Describe any additional details about the pattern.",
            "default": None,
        },
        {
            "name": "diameter",
            "type": (int, float),
            "doc": "Spiral diameter (in micrometers).",
            "default": None,
        },
        {
            "name": "height",
            "type": (int, float),
            "doc": "Spiral height of each sweep (in micrometers).",
            "default": None,
        },
        {
            "name": "number_of_revolutions",
            "type": int,
            "doc": "Number of turns within a spiral.",
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
            "description": "Power (in Watts) defined as a scalar. All rois in target receive the same photostimulation power.",
            "required": False,
        },
        {
            "name": "frequency",
            "description": "Frequency (in Hz) defined as a scalar. All rois in target receive the photostimulation at the same"
                " frequency.",
            "required": False,
        },
        {
            "name": "pulse_width",
            "description": "Pulse Width (in sec/phase) defined as a scalar. All rois in target receive the photostimulation with"
                " the same pulse width.",
            "required": False,
        },
        {
            "name": "power_per_rois",
            "description": "Power (in Watts) defined as an array. Each power value refers to each roi in target.",
            "required": False,
        },
        {
            "name": "frequency_per_rois",
            "description": "Frequency (in Hz) defined as an array. Each frequency value refers to each roi in target.",
            "required": False,
        },
        {
            "name": "pulse_width_per_rois",
            "description": "Pulse Width (in sec/phase) defined as an array. Each pulse width value refers to each roi in target.",
            "required": False,
        },
        {"name": "targets", "description": "Targeted rois for the stimulus onset.", "required": True},
        {
            "name": "stimulus_pattern",
            "description": "Link to the stimulus pattern.",
            "required": True,
        },
        {
            "name": "stimulus_site",
            "description": "Link to the stimulus site.",
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
        # columns = popargs('columns', kwargs)
        # if columns is not None:
        #     colset = {c.name: c for c in columns}
        #     if "power_per_rois" in colset.keys() and "power" in colset.keys():
        #         raise ValueError(
        #             "Both 'power' and 'power_per_rois' has been defined. Only one of them must be defined"
        #         )
        #     print(colset)
        #     for column in columns:
        #         for row in range(len(column)):
        #             if "power" in colset.keys() and isinstance(colset["power"][row], (list, np.ndarray, tuple)):
        #                 raise ValueError(
        #                     "'power' should be defined as scalar. Use 'power_per_rois' to store photostimulation at different"
        #                     " powers, for each rois in target."
        #                 )
        #             if "frequency" in colset.keys() and isinstance(colset["frequency"][row], (list, np.ndarray, tuple)):
        #                 raise ValueError(
        #                     "'frequency' should be defined as scalar. Use 'frequency_per_rois' to store photostimulation at"
        #                     " different frequency, for each rois in target."
        #                 )

        #             if "pulse_width" in colset.keys() and  isinstance(colset["pulse_width"][row], (list, np.ndarray, tuple)):
        #                 raise ValueError(
        #                     "'pulse_width' should be defined as scalar. Use 'pulse_width_per_rois' to store photostimulation with"
        #                     " different pulse width, for each rois in target."
        #                 )

        #             n_targets = len(colset["targets"][row].targeted_rois[:])

        #             if "power_per_rois" in colset.keys():
        #                 n_elements = len(colset["power_per_rois"][row])
        #                 if n_elements != n_targets:
        #                     raise ValueError(
        #                         f"'power_per_rois' has {n_elements} elements but it must have"
        #                         f" {n_targets} elements as 'targeted_roi'."
        #                     )

        #             if "frequency_per_rois" in colset.keys():
        #                 n_elements = len(colset["frequency_per_rois"][row])
        #                 if n_elements != n_targets:
        #                     raise ValueError(
        #                         f"'frequency_per_rois' has {n_elements} elements but it must have"
        #                         f" {n_targets} elements as 'targeted_roi'."
        #                     )

        #             if "pulse_width_per_rois" in colset.keys():
        #                 n_elements = len(colset["pulse_width_per_rois"][row])
        #                 if n_elements != n_targets:
        #                     raise ValueError(
        #                         f"'pulse_width_per_rois' has {n_elements} elements but it must have"
        #                         f" {n_targets} elements as 'targeted_roi'."
        #                     )
                    


    @docval(
        {"name": "start_time", "doc": "Start time of stimulation, in seconds.", "type": float},
        {"name": "stop_time", "doc": "Stop time of stimulation, in seconds.", "type": float},
        {
            "name": "power",
            "doc": "Power (in Watts) defined as a scalar. All rois in target receive the same photostimulation power.",
            "type": (int, float, Iterable),
            "default": None,
        },
        {
            "name": "frequency",
            "doc": "Frequency (in Hz) defined as a scalar. All rois in target receive the photostimulation at the same"
                " frequency.",
            "type": (int, float, Iterable),
            "default": None,
        },
        {
            "name": "pulse_width",
            "doc": "Pulse Width (in sec/phase) defined as a scalar. All rois in target receive the photostimulation with"
                " the same pulse width.",
            "type": (int, float, Iterable),
            "default": None,
        },
        {
            "name": "power_per_rois",
            "doc": "Power (in Watts) defined as an array. Each power value refers to each roi in target.",
            "type": (int, float, Iterable),
            "default": None,
        },
        {
            "name": "frequency_per_rois",
            "doc": "Frequency (in Hz) defined as an array. Each frequency value refers to each roi in target.",
            "type": (int, float, Iterable),
            "default": None,
        },
        {
            "name": "pulse_width_per_rois",
            "doc": "Pulse Width (in sec/phase) defined as an array. Each pulse width value refers to each roi in target.",
            "type": (int, float, Iterable),
            "default": None,
        },
        {
            "name": "targets",
            "doc": "Targeted rois for the stimulus onset.",
            "type": OptogeneticStimulusTarget,
        },
        {
            "name": "stimulus_pattern",
            "doc": "Link to the stimulus pattern.",
            "type": (OptogeneticStimulus3DPattern, OptogeneticStimulus2DPattern, TemporalFocusing, SpiralScanning),
        },
        {
            "name": "stimulus_site",
            "doc": "Link to the stimulus site.",
            "type": PatternedOptogeneticStimulusSite,
        },
        allow_extra=True,
    )
    def add_interval(self, **kwargs):
        """
        Add a stimulation parameters for a specific stimulus onset.
        """
        super(PatternedOptogeneticStimulusTable, self).add_interval(**kwargs)

        if isinstance(kwargs["power"], (list, np.ndarray, tuple)):
            raise ValueError(
                "'power' should be defined as scalar. Use 'power_per_rois' to store photostimulation at different"
                " powers, for each rois in target."
            )
        if isinstance(kwargs["frequency"], (list, np.ndarray, tuple)):
            raise ValueError(
                "'frequency' should be defined as scalar. Use 'frequency_per_rois' to store photostimulation at"
                " different frequency, for each rois in target."
            )

        if isinstance(kwargs["pulse_width"], (list, np.ndarray, tuple)):
            raise ValueError(
                "'pulse_width' should be defined as scalar. Use 'pulse_width_per_rois' to store photostimulation with"
                " different pulse width, for each rois in target."
            )

        n_targets = len(kwargs["targets"].targeted_rois[:])

        if kwargs["power_per_rois"] is not None:
            n_elements = len(kwargs["power_per_rois"])
            if n_elements != n_targets:
                raise ValueError(
                    f"'power_per_rois' has {n_elements} elements but it must have"
                    f" {n_targets} elements as 'targeted_roi'."
                )

        if kwargs["frequency_per_rois"] is not None:
            n_elements = len(kwargs["frequency_per_rois"])
            if n_elements != n_targets:
                raise ValueError(
                    f"'frequency_per_rois' has {n_elements} elements but it must have"
                    f" {n_targets} elements as 'targeted_roi'."
                )

        if kwargs["pulse_width_per_rois"] is not None:
            n_elements = len(kwargs["pulse_width_per_rois"])
            if n_elements != n_targets:
                raise ValueError(
                    f"'pulse_width_per_rois' has {n_elements} elements but it must have"
                    f" {n_targets} elements as 'targeted_roi'."
                )
            
        if kwargs["power_per_rois"] is None and kwargs["power"] is None:
            raise ValueError(
                "Nor 'power' or 'power_per_rois' has been defined. At least one of the two must be defined"
            )
        
        if kwargs["power_per_rois"] is not None and kwargs["power"] is not None:
            raise ValueError(
                "Both 'power' and 'power_per_rois' has been defined. Only one of them must be defined"
            )