import uuid
import os
import json

# Prevent Tensorflow warning messages when no GPU is available
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from synthetic_data.generator.datagen.model import DataGenModel

class SyntheticDataGenerator:

  # Try various temperatures.
  # 0.9 and 1.0 have been shown to generate reasonable results
  # temperatures = [0.9, 1.0]

  def __init__(self, bundle_path):
    self.bundle_path = bundle_path

  def generate(self, output_dir: str, rejects_dir:str, n_patients: int, n_days=1, early_stop=0):

    data_generator = DataGenModel(n_days, self.bundle_path, early_stop=early_stop)

    for _ in range(n_patients):

        # Generate user ID
        user_id = str(uuid.uuid4())
        output_file = os.path.join(output_dir, user_id + ".json")
        rejects_file = os.path.join(rejects_dir, user_id + ".csv")

        try:
          print(f'Generating File for user id {user_id}' )

          for _ in range(2):
            # Try 2 times, just in case all the data is rejected the first time
            outputJSON, rejectDF = data_generator.generate_single_user(user_id)

            if outputJSON is None:
              continue

            with open(output_file, 'w') as json_file:
              json.dump(outputJSON, json_file, indent=2)
          
          if rejectDF is not None: 
            rejectDF.to_csv(rejects_file, index=False)

        except Exception as e:
          print(e)
          # print('Error generating file')
