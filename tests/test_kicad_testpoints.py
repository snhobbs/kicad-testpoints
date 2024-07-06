"""Tests for `kicad_testpoints` package."""

import pathlib
import unittest

import kicad_testpoints
import pcbnew

data_dir = pathlib.Path(__file__).parent / "data"


class TestKicad_testpoints(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_pad_position_file_origin(self):
        settings = kicad_testpoints.Settings()
        settings.use_aux_origin = False

        board = pcbnew.LoadBoard((data_dir / "demo_2_pads.kicad_pcb").as_posix())
        pads = kicad_testpoints.get_pads((("TP1", 1), ("TP2", 1)), board)

        positions = [kicad_testpoints.get_pad_position(pad, settings) for pad in pads]
        expectations = ((113.25, -75.5), (135.75, -104.1))
        for position, expected in zip(positions, expectations, strict=False):
            self.assertAlmostEqual(position[0], expected[0])
            self.assertAlmostEqual(position[1], expected[1])

    def test_get_pad_position_file_origin_no_origin(self):
        settings = kicad_testpoints.Settings()
        settings.use_aux_origin = True

        board = pcbnew.LoadBoard((data_dir / "demo_2_pads.kicad_pcb").as_posix())
        pads = kicad_testpoints.get_pads((("TP1", 1), ("TP2", 1)), board)
        expectations = ((113.25, -75.5), (135.75, -104.1))
        positions = [kicad_testpoints.get_pad_position(pad, settings) for pad in pads]
        for position, expected in zip(positions, expectations, strict=False):
            self.assertAlmostEqual(position[0], expected[0])
            self.assertAlmostEqual(position[1], expected[1])

    def test_get_pad_position_file_origin_with_origin(self):
        settings = kicad_testpoints.Settings()
        settings.use_aux_origin = True

        board = pcbnew.LoadBoard((data_dir / "demo_2_pads.kicad_pcb").as_posix())
        ds = board.GetDesignSettings()
        ds.SetAuxOrigin(pcbnew.VECTOR2I_MM(100, 100))
        pads = kicad_testpoints.get_pads((("TP1", 1), ("TP2", 1)), board)
        positions = [kicad_testpoints.get_pad_position(pad, settings) for pad in pads]
        expectations = ((13.25, 24.5), (35.75, -4.1))
        for position, expected in zip(positions, expectations, strict=False):
            self.assertAlmostEqual(position[0], expected[0])
            self.assertAlmostEqual(position[1], expected[1])
