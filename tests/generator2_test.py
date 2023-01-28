import os
import logging
import unittest
from datetime import datetime

import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from synthetic_data.generator2.generator import SyntheticDataGenerator

class GeneratorTestSuite(unittest.TestCase):

  def setUp(self):
    timestamp = datetime.now()
    tests_dir = os.path.dirname(os.path.realpath(__file__))

    #
    self.bundle_dir =  os.path.join(tests_dir, 'bundles', 'generator', 'v1.1.0') # TODO: check if exists, otherwise logging.error "request bundle installation"

    # For this demo, this is the directory that holds the files that are to be evaluated
    self.output_dir = os.path.join(tests_dir, 'out', timestamp.strftime('%Y%m%d%H%M%S'))
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)

  def test_generate(self):
    syntdatag = SyntheticDataGenerator(self.bundle_dir)
    syntdatag.generate(self.output_dir, 1, 1)


if __name__ == '__main__':
    unittest.main()
