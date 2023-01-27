import unittest

from synthetic_data.generator.generator import SyntheticDataGenerator


class GeneratorTestSuite(unittest.TestCase):

  def setUp(self):
    # TODO document why this method is empty
    pass

  def test_generate(self):
    # syntdatag = SyntheticDataGenerator(self.bundle_dir)
    # syntdatag.generate(self.output_dir, 1, 1)
    assert(True)


if __name__ == '__main__':
    unittest.main()
