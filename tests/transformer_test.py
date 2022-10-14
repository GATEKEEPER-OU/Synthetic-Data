import os
import logging
import unittest
from datetime import datetime

import sys

fpath = os.path.join(os.path.dirname(__file__), "..", "..", "synthetic-data")
fpath = os.path.abspath(fpath)
sys.path.append(fpath)

from synthetic_data.transformers.SAM_GK_FHIR_1.generator import SyntheticDataGenerator

class GeneratorTestSuite(unittest.TestCase):

  def setUp(self):
    timestamp = datetime.now()
    tests_dir = os.path.dirname(os.path.realpath(__file__))

    #
    self.bundle_dir =  os.path.join(tests_dir, 'bundles', 'transformers')
    self.transformer_vers = "PT_1" # TODO: check if exists, otherwise logging.error "request bundle installation"

    # For this demo, this is the directory that holds the files that are to be evaluated
    self.output_dir = os.path.join(tests_dir, 'out', timestamp.strftime('%Y%m%d%H%M%S'))
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)

  def test_generate(self):
    syntdatag = SyntheticDataGenerator(self.bundle_dir, self.transformer_vers)
    syntdatag.generate(self.output_dir, 1, 1, 1)

if __name__ == '__main__':
    unittest.main()
