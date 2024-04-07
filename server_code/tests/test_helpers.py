# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 The Anvil Extras project team members listed at
# https://github.com/anvilistas/media-manager/graphs/contributors
#
# This software is published at https://github.com/anvilistas/media-manager
import unittest

import helpers


class TestBooleanFromString(unittest.TestCase):
    truthy = ["true", "True", "TRUE", "yes", "Yes", "YES", "1"]
    falsy = ["false", "False", "FALSE", "no", "No", "NO", "0"]
    empty = ["", None]

    def test_truthy(self):
        for value in self.truthy:
            self.assertTrue(helpers.boolean_from_string(value))

    def test_falsy(self):
        for value in self.falsy:
            self.assertFalse(helpers.boolean_from_string(value))

    def test_default_true(self):
        for value in self.empty:
            self.assertTrue(helpers.boolean_from_string(value, default=True))

    def test_default_false(self):
        for value in self.empty:
            self.assertFalse(helpers.boolean_from_string(value, default=False))
