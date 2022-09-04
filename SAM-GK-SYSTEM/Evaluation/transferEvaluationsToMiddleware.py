import os
import glob

# This stanalone script moves the processed files to Evaluation
# This does not need to be Python script. Evaluation could be on another system.
# This is just an idea.

# Directory that holds result files
EVALUATED_DIR = os.path.join(".", "evaluated")
FAKE_DIR  = os.path.join(EVALUATED_DIR, "fake")
REAL_DIR  = os.path.join(EVALUATED_DIR, "real")

# Directory that holds result files
MIDDLEWARE_DIR = os.path.join("..", "Middleware", "evaluated")
MWFAKE_DIR  = os.path.join(MIDDLEWARE_DIR, "fake")
MWREAL_DIR  = os.path.join(MIDDLEWARE_DIR, "real")

# Get the csv files from the real directory
files = glob.glob(REAL_DIR + "/*.csv")

for filename in files:
    head, tail = os.path.split(filename)
    middleware_file = os.path.join(MWREAL_DIR, tail)
    os.rename(filename, middleware_file)

# Get the csv files from the fake directory
files = glob.glob(FAKE_DIR + "/*.csv")

for filename in files:
    head, tail = os.path.split(filename)
    middleware_file = os.path.join(MWFAKE_DIR, tail)
    os.rename(filename, middleware_file)
