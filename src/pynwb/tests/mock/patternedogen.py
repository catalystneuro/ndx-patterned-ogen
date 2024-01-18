from typing import Optional
import numpy as np
from pynwb.testing.mock.device import mock_Device
from pynwb.testing.mock.ophys import mock_PlaneSegmentation
from pynwb.testing.mock.utils import name_generator
from hdmf.common.table import DynamicTableRegion
from pynwb import NWBFile
from pynwb.device import Device
from pynwb.ophys import (
    PlaneSegmentation,
)
from ndx_patterned_ogen import (
    PatternedOptogeneticStimulusTable,
    PatternedOptogeneticStimulusSite,
    OptogeneticStimulusTarget,
    OptogeneticStimulusPattern,
    SpiralScanning,
    TemporalFocusing,
    SpatialLightModulator,
    LightSource,
)


def mock_OptogeneticStimulusPattern(
    name: Optional[str] = None,
    description: str = "Generic description for optogenetic stimulus pattern",
    sweep_size: float = 5,  # um
    sweep_mask=np.zeros((10, 10)),
    nwbfile: Optional[NWBFile] = None,
) -> OptogeneticStimulusPattern:
    stimulus_pattern = OptogeneticStimulusPattern(
        name=name or name_generator("OptogeneticStimulusPattern"),
        description=description,
        sweep_mask=sweep_mask,
        sweep_size=sweep_size,
    )
    nwbfile.add_lab_meta_data(stimulus_pattern)
    return stimulus_pattern


def mock_TemporalFocusing(
    name: Optional[str] = None,
    description: str = "Generic description for optogenetic stimulus pattern",
    lateral_point_spread_function: str = "9e-6 m ± 0.7e-6 m",
    axial_point_spread_function: str = "32e-6 m ± 1.6e-6 m",
    nwbfile: Optional[NWBFile] = None,
) -> TemporalFocusing:
    stimulus_pattern_temporal_focusing = TemporalFocusing(
        name=name or name_generator("TemporalFocusing"),
        description=description,
        lateral_point_spread_function=lateral_point_spread_function,
        axial_point_spread_function=axial_point_spread_function,
    )
    nwbfile.add_lab_meta_data(stimulus_pattern_temporal_focusing)
    return stimulus_pattern_temporal_focusing


def mock_SpiralScanning(
    name: Optional[str] = None,
    description: str = "Generic description for optogenetic stimulus pattern",
    diameter: float = 15e-6,  # diameter of a single spiral
    height: float = 10e-6,  # height of a single spira (if 3D pattern)
    number_of_revolutions: float = 5,  # number of revolution of a single spira
    nwbfile: Optional[NWBFile] = None,
) -> SpiralScanning:
    stimulus_pattern_spiral_scanning = SpiralScanning(
        name=name or name_generator("SpiralScanning"),
        description=description,
        diameter=diameter,
        height=height,
        number_of_revolutions=number_of_revolutions,
    )
    nwbfile.add_lab_meta_data(stimulus_pattern_spiral_scanning)
    return stimulus_pattern_spiral_scanning


def mock_LightSource(
    name: Optional[str] = None,
    manufacturer: Optional[str] = None,
    model: Optional[str] = "laser model",
    stimulation_wavelength: float = 1035.0,  # nm
    description: str = "Generic description for the laser",
    peak_power: float = 0.70,  # the peak power of stimulation in Watts
    peak_pulse_energy: float = 0.70,
    intensity: float = 0.005,  # the intensity of excitation in W/mm^2
    exposure_time: float = 2.51e-13,  # the exposure time of the sample in seconds
    pulse_rate: float = 2.0e6,  # the pulse rate of the laser is in Hz
    nwbfile: Optional[NWBFile] = None,
) -> LightSource:
    light_source = LightSource(
        name=name or name_generator("LightSource"),
        manufacturer=manufacturer,
        model=model,
        stimulation_wavelength=stimulation_wavelength,
        description=description,
        peak_pulse_energy=peak_pulse_energy,
        peak_power=peak_power,
        intensity=intensity,
        exposure_time=exposure_time,
        pulse_rate=pulse_rate,
    )
    nwbfile.add_device(light_source)
    return light_source


def mock_SpatialLightModulator(
    name: Optional[str] = None,
    description: str = "Generic description for the spatial light modulator device",
    model: str = "Generic model for the spatial light modulator device",
    manufacturer: Optional[str] = None,
    size: list = [100, 100],
    nwbfile: Optional[NWBFile] = None,
) -> SpatialLightModulator:
    spatial_light_modulator = SpatialLightModulator(
        name=name or name_generator("SpatialLightModulator"),  # nm
        description=description,
        model=model,
        manufacturer=manufacturer,
        size=size,
    )
    nwbfile.add_device(spatial_light_modulator)
    return spatial_light_modulator


def mock_PatternedOptogeneticStimulusSite(
    name: Optional[str] = None,
    description: str = "optogenetic stimulus site",
    device: Optional[Device] = None,
    spatial_light_modulator: Optional[SpatialLightModulator] = None,
    light_source: Optional[LightSource] = None,
    excitation_lambda: float = 500.0,
    location: str = "part of the brain",
    effector: str = "ChR2",
    nwbfile: Optional[NWBFile] = None,
) -> PatternedOptogeneticStimulusSite:
    optogenetic_stimulus_site = PatternedOptogeneticStimulusSite(
        name=name or name_generator("PatternedOptogeneticMethod"),
        description=description,
        device=device or mock_Device(nwbfile=nwbfile),
        light_source=light_source or mock_LightSource(nwbfile=nwbfile),
        spatial_light_modulator=spatial_light_modulator or mock_SpatialLightModulator(nwbfile=nwbfile),
        excitation_lambda=excitation_lambda,
        location=location,
        effector=effector,
    )

    if nwbfile is not None:
        nwbfile.add_ogen_site(optogenetic_stimulus_site)

    return optogenetic_stimulus_site


def mock_OptogeneticStimulusTarget(
    name: Optional[str] = None,
    segmented_rois: DynamicTableRegion = None,
    targeted_rois=None,
    n_rois: int = 10,
    plane_segmentation: Optional[PlaneSegmentation] = None,
    nwbfile: Optional[NWBFile] = None,
) -> OptogeneticStimulusTarget:
    hologram = OptogeneticStimulusTarget(
        name=name or name_generator("Hologram"),
        targeted_rois=targeted_rois or np.array([[i, i] for i in range(n_rois)]),
        segmented_rois=segmented_rois
        or DynamicTableRegion(
            name="segmented_rois",
            description="segmented_rois",
            table=plane_segmentation or mock_PlaneSegmentation(n_rois=n_rois, nwbfile=nwbfile),
            data=list(range(n_rois)),
        ),
    )
    nwbfile.add_lab_meta_data(hologram)
    return hologram


def mock_PatternedOptogeneticStimulusTable(
    name: Optional[str] = None,
    description: str = "no description",
    start_time: list = [0.0, 0.1, 0.2],
    stop_time: list = [0.7, 0.8, 0.9],
    power: list = [700.0, 800.0, 900.0],
    frequency: list = [7.0, 8.0, 9.0],
    pulse_width: list = [0.1, 0.1, 0.1],
    stimulus_pattern: list = [None, None, None],
    targets: list = [None, None, None],
    stimulus_site: list = [None, None, None],
    nwbfile: Optional[NWBFile] = None,
) -> PatternedOptogeneticStimulusTable:
    optogenetic_stimulus_table = PatternedOptogeneticStimulusTable(
        name=name or name_generator("PatternedOptogeneticStimulusTable"), description="Patterned stimulus"
    )
    for i, start in enumerate(start_time):
        optogenetic_stimulus_table.add_interval(
            start_time=start,
            stop_time=stop_time[i],
            power=power[i],
            frequency=frequency[i],
            pulse_width=pulse_width[i],
            stimulus_pattern=stimulus_pattern[i] or mock_OptogeneticStimulusPattern(nwbfile=nwbfile),
            targets=targets[i] or mock_OptogeneticStimulusTarget(nwbfile=nwbfile),
            stimulus_site=stimulus_site[i] or mock_PatternedOptogeneticStimulusSite(nwbfile=nwbfile),
        )

    if nwbfile is not None:
        nwbfile.add_time_intervals(optogenetic_stimulus_table)

    return optogenetic_stimulus_table