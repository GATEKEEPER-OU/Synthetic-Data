#from evaluate import evaluate
from synthetic_data.evaluator.processor.process import process
from synthetic_data.evaluator.processor.evaluate import evaluate
from synthetic_data.evaluator.processor.postprocess import postprocess

class SyntheticDataEvaluator:

  msg = ""

  # TODO
  #  the constructor wants static file paths
  def __init__(self, n_days=None):
    self.n_days = n_days
    self.msg = "SyntheticDataEvaluator"
    print("%s" % self.msg)
    #print(" - dataset: %s" % dataset)

  def process_generated(self, codings_dir: str, input_dir: str, output_dir: str):
        process(codings_dir, input_dir, output_dir) 


  def evaluate_processed(self, evaluate_dir: str, dataset_dir: str, real_dir: str, fake_dir: str, report_dir: str):
    evaluate(evaluate_dir, dataset_dir, real_dir, fake_dir, report_dir, self.n_days)


  def postprocess_evaluated(self, input_dir: str, output_dir: str):
      postprocess(input_dir, output_dir)