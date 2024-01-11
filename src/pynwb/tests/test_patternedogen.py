"""Unit and integration tests for the PatternedOptogeneticStimulusTable extension neurodata type.
"""

import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing.mock.device import mock_Device
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing import TestCase, remove_test_file, NWBH5IOFlexMixin

from ndx_patterned_ogen import PatternedOptogeneticStimulusTable
from .mock.patternedogen import (
    mock_OptogeneticStimulusPattern,
    mock_OptogeneticStimulusTarget,
    mock_PatternedOptogeneticStimulusSite,
    mock_SpiralScanning,
    mock_TemporalFocusing,
    mock_LightSource,
    mock_SpatialLightModulator,
    mock_PatternedOptogeneticStimulusTable,
)


def set_up_nwbfile(nwbfile: NWBFile = None):
    """Create an NWBFile with a Device"""
    nwbfile = nwbfile or mock_NWBFile()
    device = mock_Device(nwbfile=nwbfile)
    return nwbfile


class TestPatternedOgenConstructor(TestCase):
    """Simple unit test for creating a PatternedOptogeneticStimulusTable."""

    def setUp(self):
        """Set up an NWB file."""
        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        """Test that the constructor for PatternedOptogeneticStimulusTable sets values as expected."""

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        power = 70.0
        frequency = 20.0
        pulse_width = 0.1

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulusPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.assertEqual(stimulus_table.name, "PatternedOptogeneticStimulusTable")
        self.assertEqual(stimulus_table.description, "description")
        np.testing.assert_array_equal(stimulus_table.start_time[:], [start_time])
        np.testing.assert_array_equal(stimulus_table.stop_time[:], [stop_time])

class TestPatternedOptogeneticStimulusTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for PatternedOptogeneticStimulusTable."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it to file, read the file, and test that the PatternedOptogeneticStimulusTable from the
        file matches the original PatternedOptogeneticStimulusTable.
        """

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        power = 70.0
        frequency = 20.0
        pulse_width = 0.1

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulusPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])


class TestPatternedOptogeneticStimulusTableRoundtripPyNWB(NWBH5IOFlexMixin, TestCase):
    """Complex, more complete roundtrip test for PatternedOptogeneticStimulusTable using pynwb.testing infrastructure."""

    def getContainerType(self):
        return "PatternedOptogeneticStimulusTable"

    def addContainer(self):
        set_up_nwbfile(self.nwbfile)

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        power = 70.0
        frequency = 20.0
        pulse_width = 0.1

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulusPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

    def getContainer(self, nwbfile: NWBFile):
        return nwbfile.intervals["PatternedOptogeneticStimulusTable"]
