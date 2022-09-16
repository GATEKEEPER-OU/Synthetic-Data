from synthetic_data.evaluator.processor.process import process
from synthetic_data.evaluator.processor.evaluate import evaluate
from synthetic_data.evaluator.processor.postprocess import postprocess

class SyntheticDataEvaluator:

  # the constructor wants static file paths
  def __init__(self, bundle_path: str):
    self.bundle_path = bundle_path

  # Decompose the JSON formatted observations into tabular format for evaluation.
  def process_generated(self, input_dir: str, output_dir: str):
    '''
      input_dir:  Directory containing the generated data
      output_dir: Directory holding the procesed files
    '''
    process(self.bundle_path, input_dir, output_dir)

  # Evaluate the processed using statistcal analysis. Based on this analysis we decide
  # which files contain "fake" data and which files contain "real" data.
  # Initially, we evaluate using confidential data.
  # After a number of iterations we should decide which would be tha best temperature to use or
  # we can evaluate using the "real" data in the generator module.
  # We will therefore no longer require this.
  def evaluate_processed(self, dataset_dir: str, real_dir: str, fake_dir: str, report_dir: str, n_days):
    '''
      dataset_dir:  Directory containing the processed data files
      real_dir:     Files evaluated as real
      fake_dir:     Files evaluated as fake
      report_dir:   Evaluation results
      n_days:       Number of days in output
    '''
    evaluate(self.bundle_path, dataset_dir, real_dir, fake_dir, report_dir, n_days)

  # Add data to the "real" file so that the FHIR data can be constructed.
  # The construction to FHIR data  is done by a downstream system
  def postprocess_evaluated(self, input_dir: str, output_dir: str):
    '''
      input_dir:  Directory containing the evaluated real data files
      output_dir: Directory holding the post procesed files
    '''
    postprocess(input_dir, output_dir)
