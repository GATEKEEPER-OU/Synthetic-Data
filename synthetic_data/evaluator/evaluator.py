#from evaluate import evaluate
from synthetic_data.evaluator.evaluate import evaluate

class SyntheticDataEvaluator:
  import shutil
  import glob

  msg = ""

  # TODO
  #  the constructor wants static file paths
  def __init__(self, n_days=None):
    self.n_days = n_days
    self.msg = "SyntheticDataEvaluator"

  def evaluate_processed(self, dataset_dir: str , real_dir: str, fake_dir: str, report_dir: str):
    #print("%s" % self.msg)
    #print(" - dataset: %s" % dataset)
    evaluate(dataset_dir, real_dir, fake_dir, report_dir, self.n_days)


  def transfer(self, input_dir: str, output_dir: str):
    
    # Get the csv files from the input directory
    files = self.glob.glob(input_dir + "/*.csv")

    for filename in files:
      self.shutil.copy(filename, output_dir)
