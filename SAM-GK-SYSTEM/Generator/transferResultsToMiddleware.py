import os
import glob

# This stanalone script moves the results files to Middleware
# This does not need to be Python script. Middleware could be on ather system.
# This is just an idea.

# Directory that holds result files
RESULT_DIR = os.path.join('.', "results")

MIDDLEWARE_DIR = os.path.join("..", "Middleware", "generator_files")

# Get the csv files from the results directory
files = glob.glob(RESULT_DIR + "/*.csv")

for filename in files:
    head, tail = os.path.split(filename)
    middleware_file = os.path.join(MIDDLEWARE_DIR, tail)
    os.rename(filename, middleware_file)