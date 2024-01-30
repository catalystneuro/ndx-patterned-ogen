from collections.abc import Iterable
from hdmf.utils import docval, popargs_to_dict, get_docval
from pynwb import register_class
from pynwb.core import DynamicTableRegion
from pynwb.device import Device
from pynwb.file import LabMetaData, TimeIntervals
from pynwb.ogen import OptogeneticStimulusSite

namespace = "ndx-patterned-ogen"
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
            "type": Device,
            "doc": "Spatial light modulator used to generate photostimulation pattern.",
        },
        {"name": "light_source", "type": Device, "doc": "Light source used to apply photostimulation."},
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
            "type": Device,
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

    @docval({"name": "light_source", "type": Device, "doc": "Light source used to apply photostimulation."})
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
        {"name": "segmented_rois", "child": True},
        {"name": "targeted_rois", "child": True},
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
            "description": "Frequency of stimulation if the stimulus delivered is pulsed (in Hz).",
            "required": False,
        },
        {
            "name": "pulse_width",
            "description": "Pulse width of stimulation if the stimulus delivered is pulsed, in seconds/phase.",
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

    @docval(
        {"name": "start_time", "doc": "Start time of stimulation, in seconds.", "type": float},
        {"name": "stop_time", "doc": "Stop time of stimulation, in seconds.", "type": float},
        {
            "name": "power",
            "doc": "Power (in Watts) applied to each target during patterned photostimulation.",
            "type": (int, float, Iterable),
            "default": 0.0,
        },
        {
            "name": "frequency",
            "doc": "Frequency of stimulation if the stimulus delivered is pulsed (in Hz).",
            "type": (int, float, Iterable),
            "default": 0.0,
        },
        {
            "name": "pulse_width",
            "doc": "Pulse width of stimulation if the stimulus delivered is pulsed, in seconds/phase.",
            "type": (int, float, Iterable),
            "default": 0.0,
        },
        {
            "name": "targets",
            "doc": "Targeted rois for the stimulus onset.",
            "type": OptogeneticStimulusTarget,
        },
        {
            "name": "stimulus_pattern",
            "doc": "Link to the stimulus pattern.",
            "type": LabMetaData,
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
