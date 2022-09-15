import os
from datetime import datetime
from synthetic_data.evaluator.evaluator import SyntheticDataEvaluator

def main():
  bundle_dir =  os.path.join('tests', 'bundles', 'evaluator', 'v0.1.0')

  timestamp = datetime.now()

  input_dir = os.path.join('out', '20220915154715') # The generated data
  
  # If rerunning delete "real" directory      
  output_dir = os.path.join('out', '20220915154715', 'real') # The evaluated data for transfer
  if not os.path.exists(output_dir):
      os.makedirs(output_dir) 
  
  dataset_dir = os.path.join('datasets', timestamp.strftime('%Y%m%d%H%M%S'))

  # This is the directory that holds the processed files
  processed_dir = os.path.join(dataset_dir, 'processed')
  if not os.path.exists(processed_dir):
      os.makedirs(processed_dir)

  # This is the directory that holds the files that are real
  real_dir = os.path.join(dataset_dir, 'real')
  if not os.path.exists(real_dir):
      os.makedirs(real_dir)

  # This is the directory that holds the files that are fake
  fake_dir = os.path.join(dataset_dir, 'fake')
  if not os.path.exists(fake_dir):
      os.makedirs(fake_dir)

  # This is the directory that holds reports. Should exist.
  report_file = os.path.join('tests', 'reports', timestamp.strftime('%Y%m%d%H%M%S') + ".csv")

  syntdatae = SyntheticDataEvaluator(bundle_dir)

  print("Processing Data")
  syntdatae.process_generated(input_dir, processed_dir)
  print()
  
  print("Evaluating Data")
  syntdatae.evaluate_processed(processed_dir, real_dir, fake_dir, report_file, 1)
  print()
  
  print("Post Processing Data")
  syntdatae.postprocess_evaluated(real_dir, output_dir)
  print()

if __name__ == "__main__":
    main()
