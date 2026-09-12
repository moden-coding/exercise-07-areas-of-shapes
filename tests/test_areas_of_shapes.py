#!/usr/bin/env python3

import contextlib
import io
import math
import re
import unittest
from unittest.mock import patch

from src.areas_of_shapes import main


class AreasOfShapes(unittest.TestCase):

    def test_empty(self):
        with patch('builtins.input', side_effect=[""]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                main()
            result = buf.getvalue().strip().split('\n')
            self.assertEqual(
                len(result), 1,
                msg="Program should quit immediately, when empty string is "
                    "given!")

    def test_one_query(self):
        with patch('builtins.input', side_effect=["triangle", "20", "5", ""]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                main()
            result = buf.getvalue().strip().split('\n')
            self.assertEqual(
                len(result), 1,
                msg="Expected exactly one result line!")
            pattern = r"^The area is (.*)"
            self.assertRegex(
                result[0], pattern,
                msg="Expected output about the resulting area!")
            m = re.match(pattern, result[0])
            self.assertEqual(
                float(m.group(1)), 20 * 5 / 2,
                msg="Wrong area for a triangle with dimensions 20 and 5!")

    def test_many_queries(self):
        input_sequence = ["triangle", "20", "5", "rectangel",
                           "rectangle", "20", "4", "circle", "10", ""]
        with patch('builtins.input', side_effect=input_sequence):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                main()
            result = buf.getvalue().strip().split('\n')
            self.assertEqual(
                len(result), 4,
                msg="Expected four lines of output for input sequence %s!"
                    % input_sequence)
            pattern = r"^The area is (.*)"
            self.assertRegex(
                result[0], pattern,
                msg="Expected output about the resulting area!")
            m = re.match(pattern, result[0])
            self.assertEqual(
                float(m.group(1)), 20 * 5 / 2,
                msg="Wrong area for a triangle with dimensions 20 and 5!")

            self.assertEqual(
                result[1], "Unknown shape!",
                msg="Incorrect error message for shape 'rectangel'!")

            self.assertRegex(
                result[2], pattern,
                msg="Expected output about the resulting area!")
            m = re.match(pattern, result[2])
            self.assertEqual(
                float(m.group(1)), 20 * 4,
                msg="Wrong area for a rectangle with dimensions 20 and 4!")

            self.assertRegex(
                result[3], pattern,
                msg="Expected output about the resulting area!")
            m = re.match(pattern, result[3])
            self.assertAlmostEqual(
                float(m.group(1)), math.pi * 10 ** 2, places=4,
                msg="Wrong area for circle with radius 10!")


if __name__ == '__main__':
    unittest.main()
