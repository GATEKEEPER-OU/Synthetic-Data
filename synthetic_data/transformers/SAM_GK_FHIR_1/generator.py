import uuid
import os

# Prevent Tensorflow warning messages when no GPU is available
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Import Data Generation Class
#from synthetic_data.generator.datagen.model import DataGenModel
from synthetic_data.transformers.SAM_GK_FHIR_1.datagen.model import DataGenModel


class SyntheticDataGenerator:
  # Synthetic Data Generator Wrapper

  # Try various temperatures.
  # To date, there has not been enough experimentation to determine the best.
  # Will be done for the paper.
  temperatures = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

  def __init__(self, bundle_path):
    self.bundle_path = bundle_path

  def generate(self, output_dir: str, n_patients: int, n_days=1):
    for _ in range(n_patients):

      # Generate user ID
      user_id = str(uuid.uuid4())

      # The model is dumb. It does not understand days.
      # Well actually, it can only understand what it has been trained on.
      # We will assume 50 max_timings per day.
      max_timings = n_days * 50

      for i, temperature in enumerate(self.temperatures[:1], start=1):
        # A File could be evaluated as fake in relation to the data that the model is trained on.
        # Generate a number of files to be evaluated.
        userno = str(i)

        output_file = os.path.join(output_dir, user_id + "_" + userno + ".csv")

        print(f'Generating File {userno} for user id {user_id}' )
        try:
          # Instantiate Data Genearation Class
          data_generator = DataGenModel(self.bundle_path)

          # Run generate_single_user method of Data Generation Class
          results_df = data_generator.generate_single_user(temperature, max_timings)

          results_df.to_csv(output_file, index = False)
          print(f'{output_file} has been generated and is ready to be transferred for evaluation')
        except:
          print('Error generating file')
