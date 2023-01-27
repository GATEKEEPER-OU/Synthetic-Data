import time


class SyntheticDataGenerator:

  def __init__(self, bundle_path):
    self.bundle_path = bundle_path

  def generate(self, output_dir: str, n_patients=1, n_days=1):
    time.sleep(5)
    # TODO save on file always the same FHIR bundle
