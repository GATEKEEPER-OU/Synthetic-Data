# Variables that do not change

import os
import tensorflow as tf

# Working Directory = "."
WORKING_DIR = "."

# Directory that will hold the results file
RESULT_DIR = os.path.join(WORKING_DIR, "results")

# Check whether the specified path exists or not
isExist = os.path.exists(RESULT_DIR)
if not isExist:
    # Create a new directory because it does not exist 
    os.makedirs(RESULT_DIR)

# Directory containing the files with static data
STATIC_DIR = os.path.join(WORKING_DIR, "static")

# Directory with the H5 formatted models
MODELS_DIR = os.path.join(WORKING_DIR, "models")
    
MAX_NUM_REAL_USERS = 86
TIMING_SEQ_LEN = 6
TIMING_MODEL = tf.keras.models.load_model(os.path.join(MODELS_DIR, "timing_model.h5"))
EVENT_MODEL = tf.keras.models.load_model(os.path.join(MODELS_DIR, "event_model.h5"))
EVENT_PADDING_END_TOKEN = ";"
EVENT_UNKNOWN_TOKEN = '[UNK]'

# The number of next characters we want to generate before giving up. 
# This is lower than the actual maximum sequence length to account for the starting characters 
EVENT_SEQ_LEN = 620

# Vocabularies
timings_vocab = os.path.join(STATIC_DIR, "timings_vocab.json")
events_vocab = os.path.join(STATIC_DIR, "events_vocab.json")

# File holding codings mappings
codingFile = os.path.join(STATIC_DIR, "codings.csv")