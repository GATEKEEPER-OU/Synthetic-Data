from synthetic_data.evaluator.processor.process import process
from synthetic_data.evaluator.processor.evaluate import evaluate
from synthetic_data.evaluator.processor.postprocess import postprocess

class SyntheticDataEvaluator:

  # the constructor wants static file paths
  def __init__(self, bundle_path: str):
    self.bundle_path = bundle_path

  # TODO: comment this
  def process_generated(self, dataset_dir: str):
    # process(codings_dir, input_dir, output_dir)
    pass

  # TODO: comment this
  # def evaluate_processed(self, evaluate_dir: str, dataset_dir: str, real_dir: str, fake_dir: str, report_dir: str):
  #   # evaluate(evaluate_dir, dataset_dir, real_dir, fake_dir, report_dir, self.n_days)
  #   pass

  # TODO: comment this
  def postprocess_evaluated(self, dataset_dir: str):
      # postprocess(input_dir, output_dir)
    pass