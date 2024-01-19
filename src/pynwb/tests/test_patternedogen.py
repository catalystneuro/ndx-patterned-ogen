"""Unit and integration tests for the PatternedOptogeneticStimulusTable extension neurodata type.
"""

import numpy as np
from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing import TestCase, remove_test_file, NWBH5IOFlexMixin

from ndx_patterned_ogen import PatternedOptogeneticStimulusTable
from .mock.patternedogen import (
    mock_OptogeneticStimulus2DPattern,
    mock_OptogeneticStimulusTarget,
    mock_PatternedOptogeneticStimulusSite,
)


def set_up_nwbfile(nwbfile: NWBFile = None):
    """Create an NWBFile with a Device"""
    nwbfile = nwbfile or mock_NWBFile()
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
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.assertEqual(stimulus_table.name, "PatternedOptogeneticStimulusTable")
        self.assertEqual(stimulus_table.description, "description")
        np.testing.assert_array_equal(stimulus_table.start_time[:], [start_time])
        np.testing.assert_array_equal(stimulus_table.stop_time[:], [stop_time])

    def test_constructor_power_as_array(self):
        """Test that the constructor for PatternedOptogeneticStimulusTable sets values as expected."""

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0

        targets = mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile)
        power = np.random.uniform(50e-3, 70e-3, targets.targeted_rois.shape[0])
        frequency = np.random.uniform(20.0, 100.0, targets.targeted_rois.shape[0])
        pulse_width = np.random.uniform(0.1, 0.2, targets.targeted_rois.shape[0])

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=targets,
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.assertEqual(stimulus_table.name, "PatternedOptogeneticStimulusTable")
        self.assertEqual(stimulus_table.description, "description")
        np.testing.assert_array_equal(stimulus_table.power[:], [power])
        np.testing.assert_array_equal(stimulus_table.frequency[:], [frequency])
        np.testing.assert_array_equal(stimulus_table.pulse_width[:], [pulse_width])

    def test_constructor_power_as_array_fail(self):
        """Test that the constructor for PatternedOptogeneticStimulusTable sets values as expected."""

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0

        targets = mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile)
        power = np.random.uniform(50e-3, 70e-3, targets.targeted_rois.shape[0] + 2)
        frequency = np.random.uniform(20.0, 100.0, targets.targeted_rois.shape[0])
        pulse_width = np.random.uniform(0.1, 0.2, targets.targeted_rois.shape[0])

        interval_parameter = dict(
            start_time=start_time,
            stop_time=stop_time,
            power=[power],
            frequency=[frequency],
            pulse_width=[pulse_width],
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=targets,
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        with self.assertRaises(ValueError):
            stimulus_table.add_interval(**interval_parameter)


class TestPatternedOptogeneticStimulusTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for PatternedOptogeneticStimulusTable."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it to file,
        read the file, and test that the PatternedOptogeneticStimulusTable from the
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
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])

    def test_roundtrip_power_as_array(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it
        to file, read the file, and test that the PatternedOptogeneticStimulusTable
        from the file matches the original PatternedOptogeneticStimulusTable.
        """

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        targets = mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile)
        power = np.random.uniform(50e-3, 70e-3, targets.targeted_rois.shape[0])
        frequency = np.random.uniform(20.0, 100.0, targets.targeted_rois.shape[0])
        pulse_width = np.random.uniform(0.1, 0.2, targets.targeted_rois.shape[0])

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=targets,
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])


class TestPatternedOptogeneticStimulusTableRoundtripPyNWB(NWBH5IOFlexMixin, TestCase):
    """
    Complex, more complete roundtrip test for PatternedOptogeneticStimulusTable
    using pynwb.testing infrastructure.
    """

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
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

    def getContainer(self, nwbfile: NWBFile):
        return nwbfile.intervals["PatternedOptogeneticStimulusTable"]
