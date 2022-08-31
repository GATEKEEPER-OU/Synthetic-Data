# Variables that do not change
import os
from datetime import datetime
import pandas as pd

# Working Directory = "."
WORKING_DIR = "."

# Directory holding the the generated data files 
GENERATOR_RESULT_DIR = os.path.join(WORKING_DIR, "generator_files")

# Directory that will hold the processed result files
GENERATOR_PROCESSED_DIR = os.path.join(WORKING_DIR, "generator_processed")

# Directory that will hold files we have processed
ARCHIVE_DIR = os.path.join(WORKING_DIR, "archive")

today = datetime.now()
ARCHIVE_DIR  = os.path.join(ARCHIVE_DIR, today.strftime('%Y%m%d'))

for d in [GENERATOR_PROCESSED_DIR,  GENERATOR_RESULT_DIR, ARCHIVE_DIR]:
    # Check whether the specified path exists or not
    isExist = os.path.exists(d)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(d)

def get_codings():
    # Directory containing the files with static data
    STATIC_DIR = os.path.join(WORKING_DIR, "static")
    
    # File holding codings mappings
    codingFile = os.path.join(STATIC_DIR, "codings.csv")

    codingDF = pd.read_csv(codingFile)
    coding = codingDF['coding'].values.tolist()
    display = codingDF['display'].values.tolist()
    guide_text = codingDF['guide_text'].values.tolist()
    return coding, display, guide_text