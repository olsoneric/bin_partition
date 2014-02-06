

# Copyright 2012-2013 Eric Olson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from binpartition.binpartition import Bin
from pedemath.rect import Rect


class BinInitTestCase(unittest.TestCase):
    """Test Bin constructor."""

    def test_init_world(self):
        """Ensure constructor is executed with no errors."""

        Bin(5, 5, 600, 600)


class BinInsertTestCase(unittest.TestCase):
    """Test Bin constructor."""

    def test_insert(self):
        """Ensure insert works."""

        binpart = Bin(1, 1, 600, 600)
        rect1 = Rect(22, 34, 32, 32)
        obj = object()
        binpart.insert(rect1, obj)
        self.assertIn(obj, binpart.columns[0][0])

    def test_insert_outside_of_bounds(self):
        """Ensure no errors occur if insert rect is outside of boundaries."""

        binpart = Bin(1, 1, 600, 600)

        rect1 = Rect(2000, 2000, 32, 32)
        obj1 = object()
        binpart.insert(rect1, obj1)

        self.assertNotIn(obj1, binpart.columns[0][0])

        rect2 = Rect(-2000, -2000, 32, 32)
        obj2 = object()
        binpart.insert(rect2, obj2)

        self.assertNotIn(obj2, binpart.columns[0][0])


class BinGetStartColRowEndColRowRange(unittest.TestCase):
    """Test Bin._get_col_row_range()"""

    def test_get_col_row_range(self):
        """Ensure Bin._col_row_range returns the correct
        start and end.
        """

        binpart = Bin(6, 6, 600, 600)
        rect = Rect(22, 34, 32, 32)
        start_col, start_row, end_col, end_row = (
            binpart._get_col_row_range(rect))
        self.assertEqual((start_col, start_row, end_col, end_row),
                         (0, 0, 1, 1))

    def test_insert_outside_of_bounds(self):
        """Ensure no errors occur if insert rect is outside of boundaries."""

        binpart = Bin(1, 1, 600, 600)

        rect1 = Rect(2000, 2000, 32, 32)
        obj1 = object()
        binpart.insert(rect1, obj1)

        self.assertNotIn(obj1, binpart.columns[0][0])

        rect2 = Rect(-2000, -2000, 32, 32)
        obj2 = object()
        binpart.insert(rect2, obj2)

        self.assertNotIn(obj2, binpart.columns[0][0])


class BinGetAllObjsTestCase(unittest.TestCase):
    """Test Bin.get_all_objs()."""

    def test_get_all_objs(self):
        """Ensure all objs are returned."""

        binpart = Bin(5, 5, 600, 600)

        rect1 = Rect(22, 34, 32, 32)
        obj1 = object()
        binpart.insert(rect1, obj1)

        rect2 = Rect(511, 300, 32, 32)
        obj2 = object()
        binpart.insert(rect2, obj2)

        self.assertEqual(binpart.get_all_objs(), [obj1, obj2])

    def test_get_all_objs_when_in_multiple_bins(self):
        """Ensure all objs are returned only once.
        The objects are large enough to be in multiple bins.
        """

        binpart = Bin(5, 5, 600, 600)

        rect1 = Rect(22, 34, 300, 300)
        obj1 = object()
        binpart.insert(rect1, obj1)

        rect2 = Rect(511, 300, 400, 400)
        obj2 = object()
        binpart.insert(rect2, obj2)

        # Both options should be returned and not duplicated.
        self.assertEqual(binpart.get_all_objs(), [obj2, obj1])






