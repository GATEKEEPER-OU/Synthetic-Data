import os
import logging
import unittest
from datetime import datetime

from synthetic_data.generator.generator import SyntheticDataGenerator

class GeneratorTestSuite(unittest.TestCase):

  def setUp(self):
    timestamp = datetime.now()
    tests_dir = os.path.dirname(os.path.realpath(__file__))

    #
    self.bundle_dir =  os.path.join(tests_dir, 'bundles', 'generator', 'v0.1.0') # TODO: check if exists, otherwise logging.error "request bundle installation"

    # For this demo, this is the directory that holds the files that are to be evaluated
    self.output_dir = os.path.join(tests_dir, 'out', timestamp.strftime('%Y%m%d%H%M%S'))
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)

  def test_generate(self):
    syntdatag = SyntheticDataGenerator(self.bundle_dir)
    syntdatag.generate(self.output_dir, 1, 1)


if __name__ == '__main__':
    unittest.main()
