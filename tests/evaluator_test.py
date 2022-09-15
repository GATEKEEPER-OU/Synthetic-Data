import os
from datetime import datetime
from synthetic_data.evaluator.evaluator import SyntheticDataEvaluator

def main():
  bundle_dir =  os.path.join('tests', 'bundles', 'evaluator', 'v0.1.0')

  timestamp = datetime.now()

  # For this demo, this is the directory that holds the files that are to be evaluated
  output_dir = os.path.join('out', 'generated', timestamp.strftime('%Y%m%d%H%M'))
  os.makedirs(output_dir)

  syntdatae = SyntheticDataEvaluator(bundle_dir)

  print("Evaluating Data")
  # syntdatae.evaluate(output_dir) // FIXTHIS
  print()

if __name__ == "__main__":
    main()
