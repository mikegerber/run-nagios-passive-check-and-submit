#!/usr/bin/python
from __future__ import division
import glob
import pep8
import sys
import unittest

from run_nagios import run_check


class RunCheckTestCase(unittest.TestCase):
    def testOK(self):
        result = run_check(['/bin/sh', '-c', '/usr/bin/env echo TRUE; /usr/bin/env true'])
        self.assertEqual(result, (0, b'TRUE'))

    def testWARNING(self):
        result = run_check(['/bin/sh', '-c', '/usr/bin/env echo FALSE; /usr/bin/env false'])
        self.assertEqual(result, (1, b'FALSE'))


if __name__ == '__main__':
    unittest.main()
