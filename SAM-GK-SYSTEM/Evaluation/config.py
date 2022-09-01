# Variables that do not change
import os
from datetime import datetime
import pandas as pd

today = datetime.now()

# Working Directory = "."
WORKING_DIR = "."

# Directory holding the processed result files to be evaluated
RESULT_DIR = os.path.join(WORKING_DIR, "files_for_evaluation")

# Directory that will hold the evaluated result files
EVALUATION_REPORT_DIR = os.path.join(WORKING_DIR, "reports")
report_file = os.path.join(EVALUATION_REPORT_DIR, today.strftime('%Y%m%d%H%M') + ".csv")

# Directory that will hold files we have processed
EVALUATED_DIR = os.path.join(WORKING_DIR, "evaluated")
FAKE_DIR  = os.path.join(EVALUATED_DIR, "fake")
REAL_DIR  = os.path.join(EVALUATED_DIR, "real")

for d in [RESULT_DIR,  EVALUATION_REPORT_DIR, FAKE_DIR, REAL_DIR]:
    # Check whether the specified path exists or not
    isExist = os.path.exists(d)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(d)

STATIC_DIR = os.path.join(WORKING_DIR, "static")
evaluation_file = os.path.join(STATIC_DIR, "evaluation.csv")