from synthetic_data.evaluator.processor.process import process
from synthetic_data.evaluator.processor.evaluate import evaluate
from synthetic_data.evaluator.processor.postprocess import postprocess

import os

class SyntheticDataEvaluator:

  # the constructor wants static file paths
  def __init__(self, bundle_path: str, real_dir: str, working_dir: str, discard_dir: str):
    self.bundle_path = bundle_path
    self.real_dir = real_dir
    self.working_dir = working_dir
    self.discard_dir = discard_dir

  # Decompose the JSON formatted observations into tabular format for evaluation.
  def _process_generated(self, input_dir: str):
    '''
      input_dir:  Directory containing the generated data
    '''
    output_dir = os.path.join(self.working_dir, 'processed')
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    process(self.bundle_path, input_dir, output_dir)
    return output_dir

  # Evaluate the processed using statistcal analysis. Based on this analysis we decide
  # which files contain "fake" data and which files contain "real" data.
  # Initially, we evaluate using confidential data.
  # After a number of iterations we should decide which would be tha best temperature to use or
  # we can evaluate using the "real" data in the generator module.
  # We will therefore no longer require this.
  def _evaluate_processed(self, processed_dir: str, n_days):
    '''
      processed_dir:  Directory containing the processed data files
      n_days:    Number of days in output
    '''
    output_dir = os.path.join(self.working_dir, 'real')
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    evaluate(self.bundle_path, processed_dir, output_dir, self.discard_dir, n_days)
    return output_dir

  # Add data to the "real" file so that the FHIR data can be constructed.
  # The construction to FHIR data  is done by a downstream system
  def _postprocess_evaluated(self, working_real_dir):
    '''
      temp_dir:  Directory containing the evaluated real data files
    '''
    postprocess(working_real_dir, self.real_dir)

  def evaluate_generated(self, input_dir, n_days):
    processed_dir = self._process_generated(input_dir)
    working_real_dir = self._evaluate_processed(processed_dir, n_days)
    self._postprocess_evaluated(working_real_dir)
