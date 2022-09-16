import os
from datetime import datetime
from synthetic_data.evaluator.evaluator import SyntheticDataEvaluator

def main():

  tests_dir = os.path.dirname(os.path.realpath(__file__))
  bundle_dir =  os.path.join(tests_dir, 'bundles', 'evaluator', 'v0.1.0')
  
  input_dir = os.path.join(tests_dir, 'out') # The generated data
  
  real_dir = os.path.join(input_dir, 'real')
  if not os.path.exists(real_dir):
      os.makedirs(real_dir)

  discard_dir = os.path.join(input_dir, 'discard')
  if not os.path.exists(discard_dir):
      os.makedirs(discard_dir)

  working_dir = os.path.join(input_dir, 'working')
  if not os.path.exists(working_dir):
      os.makedirs(working_dir)

  syntdatae = SyntheticDataEvaluator(
    bundle_dir, 
    real_dir,
    working_dir, 
    discard_dir = discard_dir)

  print("Evaluating Generated Data")
  syntdatae.evaluate_generated(input_dir,  1)
  print()

if __name__ == "__main__":
  main()
