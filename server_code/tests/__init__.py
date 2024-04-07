# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 The Anvil Extras project team members listed at
# https://github.com/anvilistas/media-manager/graphs/contributors
#
# This software is published at https://github.com/anvilistas/media-manager
import sys
import unittest

test_modules = ["tests.test_helpers"]


def run(verbosity=0):
    test = unittest.TestLoader().loadTestsFromNames(test_modules)
    unittest.TextTestRunner(stream=sys.stdout, verbosity=verbosity).run(test)
