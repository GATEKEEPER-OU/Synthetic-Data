import os
from datetime import datetime
from synthetic_data.generator.generator import SyntheticDataGenerator

def main():
  timestamp = datetime.now()
  tests_dir = os.path.dirname(os.path.realpath(__file__))
  bundle_dir =  os.path.join(tests_dir, 'bundles', 'generator', 'v0.1.0')

  # For this demo, this is the directory that holds the files that are to be evaluated
  output_dir = os.path.join(tests_dir, 'out', timestamp.strftime('%Y%m%d%H%M%S'))
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  syntdatag = SyntheticDataGenerator(bundle_dir)

  print("Generating Data")
  syntdatag.generate(output_dir, 1, 1)
  print()

if __name__ == "__main__":
  main()
