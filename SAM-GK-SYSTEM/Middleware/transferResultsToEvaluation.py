import os
import glob

# This stanalone script moves the processed files to Evaluation
# This does not need to be Python script. Evaluation could be on another system.
# This is just an idea.

# Directory that holds result files
RESULT_DIR = os.path.join('.', "generator_processed")

EVALUATION_DIR = os.path.join("..", "Evaluation", "files_for_evaluation")

# Get the csv files from the results directory
files = glob.glob(RESULT_DIR + "/*.csv")

for filename in files:
    head, tail = os.path.split(filename)
    middleware_file = os.path.join(EVALUATION_DIR, tail)
    os.rename(filename, middleware_file)