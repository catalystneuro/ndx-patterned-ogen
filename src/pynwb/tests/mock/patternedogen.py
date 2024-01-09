from typing import Optional
import numpy as np
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing.mock.device import mock_Device
from pynwb.testing.mock.ophys import (
    mock_ImagingPlane,
    mock_OpticalChannel,
    mock_PlaneSegmentation,
)
from pynwb.testing.mock.utils import name_generator
from hdmf.common.table import DynamicTableRegion
from pynwb import NWBFile
from pynwb.device import Device
from pynwb.ophys import (
    PlaneSegmentation,
)
from ndx_patterned_ogen import (
    PatternedOptogeneticStimulusTable,
    PatternedOptogeneticMethod,
    OptogeneticStimulusPattern,
    SpiralScanning,
    TemporalFocusing,
    SpatialLightModulator,
    LightSource,
    Hologram,
)


def mock_OptogeneticStimulusPattern(
    name: Optional[str] = None,
    description: str = "Generic description for optogenetic stimulus pattern",
    time_per_sweep: float = 10e-3,  # Duration of a single stimulus in sec
    sweep_size: float = 5,  # um
    number_of_sweeps: int = 10,  # Number of times the stimulus is repeated
    inter_sweep_interval: float = 0.02,  # Inter stimulus time duratrion in sec
    nwbfile: Optional[NWBFile] = None,
) -> OptogeneticStimulusPattern:
    stimulus_pattern = OptogeneticStimulusPattern(
        name=name or name_generator("OptogeneticStimulusPattern"),
        description=description,
        time_per_sweep=time_per_sweep,
        sweep_size=sweep_size,
        number_of_sweeps=number_of_sweeps,
        inter_sweep_interval=inter_sweep_interval,
    )
    nwbfile.add_lab_meta_data(stimulus_pattern)
    return stimulus_pattern


def mock_TemporalFocusing(
    name: Optional[str] = None,
    description: str = "Generic description for optogenetic stimulus pattern",
    time_per_sweep: float = 10e-3,  # Duration of a single stimulus in sec
    number_of_sweeps: int = 10,  # Number of times the stimulus is repeated
    inter_sweep_interval: float = 0.02,  # Inter stimulus time duratrion in sec
    lateral_point_spread_function: str = "9e-6 m ± 0.7e-6 m",
    axial_point_spread_function: str = "32e-6 m ± 1.6e-6 m",
    nwbfile: Optional[NWBFile] = None,
) -> TemporalFocusing:
    stimulus_pattern_temporal_focusing = TemporalFocusing(
        name=name or name_generator("TemporalFocusing"),
        description=description,
        time_per_sweep=time_per_sweep,
        number_of_sweeps=number_of_sweeps,
        inter_sweep_interval=inter_sweep_interval,
        lateral_point_spread_function=lateral_point_spread_function,
        axial_point_spread_function=axial_point_spread_function,
    )
    nwbfile.add_lab_meta_data(stimulus_pattern_temporal_focusing)
    return stimulus_pattern_temporal_focusing


def mock_SpiralScanning(
    name: Optional[str] = None,
    description: str = "Generic description for optogenetic stimulus pattern",
    time_per_sweep: float = 10e-3,  # Duration of a single stimulus in sec
    number_of_sweeps: int = 10,  # Number of times the stimulus is repeated
    inter_sweep_interval: float = 0.02,  # Inter stimulus time duratrion in sec
    diameter: float = 15e-6,  # diameter of a single spiral
    height: float = 10e-6,  # height of a single spira (if 3D pattern)
    number_of_revolutions: float = 5,  # number of revolution of a single spira
    nwbfile: Optional[NWBFile] = None,
) -> SpiralScanning:
    stimulus_pattern_spiral_scanning = SpiralScanning(
        name=name or name_generator("SpiralScanning"),
        description=description,
        time_per_sweep=time_per_sweep,
        number_of_sweeps=number_of_sweeps,
        inter_sweep_interval=inter_sweep_interval,
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
    filter_description: str = "short pass 1040 nm filter",
    peak_power: float = 700.0,  # the peak power of stimulation in Watts
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
        filter_description=filter_description,
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
    model: Optional[str] = None,
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


def mock_PatternedOptogeneticMethod(
    name: Optional[str] = None,
    description: str = "optogenetic stimulus site",
    device: Optional[Device] = None,
    spatial_light_modulator: Optional[SpatialLightModulator] = None,
    light_source: Optional[LightSource] = None,
    stimulus_pattern: Optional[OptogeneticStimulusPattern] = None,
    excitation_lambda: float = 500.0,
    location: str = "part of the brain",
    effector: str = "ChR2",
    nwbfile: Optional[NWBFile] = None,
) -> PatternedOptogeneticMethod:
    optogenetic_stimulus_site = PatternedOptogeneticMethod(
        name=name or name_generator("PatternedOptogeneticMethod"),
        description=description,
        device=device or mock_Device(nwbfile=nwbfile),
        light_source=light_source or mock_LightSource(nwbfile),
        spatial_light_modulator=spatial_light_modulator or mock_SpatialLightModulator(nwbfile),
        excitation_lambda=excitation_lambda,
        stimulus_pattern=stimulus_pattern or mock_OptogeneticStimulusPattern(nwbfile),
        location=location,
        effector=effector,
    )

    if nwbfile is not None:
        nwbfile.add_ogen_site(optogenetic_stimulus_site)

    return optogenetic_stimulus_site


def mock_Hologram(
    name: Optional[str] = None,
    rois=None,
    n_rois=None,
    plane_segmentation: Optional[PlaneSegmentation] = None,
    nwbfile: Optional[NWBFile] = None,
) -> Hologram:
    hologram = Hologram(
        name=name or name_generator("Hologram"),
        rois=rois
        or DynamicTableRegion(
            name="rois",
            description="rois",
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
    power_per_target: list = [700.0, 800.0, 900.0],
    method=None,
    hologram=None,
    nwbfile: Optional[NWBFile] = None,
) -> PatternedOptogeneticStimulusTable:
    optogenetic_stimulus_table = PatternedOptogeneticStimulusTable(
        name=name or name_generator("PatternedOptogeneticStimulusTable"), description="Patterned stimulus"
    )
    for i, start in enumerate(start_time):
        optogenetic_stimulus_table.add_interval(
            start_time=start,
            stop_time=stop_time[i],
            power_per_target=power_per_target[i],
            method=method[i] or mock_PatternedOptogeneticMethod(nwbfile),
            hologram=hologram[i] or mock_Hologram(nwbfile),
        )

    if nwbfile is not None:
        nwbfile.add_time_intervals(optogenetic_stimulus_table)

    return optogenetic_stimulus_table
