import uuid
import os

# Prevent Tensorflow warning messages when no GPU is available
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Import Data Generation Class
#from synthetic_data.generator.datagen.model import DataGenModel
from synthetic_data.transformers.SAM_GK_FHIR_1.datagen.model import DataGenModel

class SyntheticDataGenerator:
  # Synthetic Data Generator Wrapper

  def __init__(self, bundle_path, transformer_version):
    self.bundle_path = bundle_path
    self.transformer_version = transformer_version

  def generate(self, output_dir: str, n_patients: int, n_days=1):
    for _ in range(n_patients):

      # Generate user ID
      user_id = str(uuid.uuid4())
      output_file = os.path.join(output_dir, user_id + ".csv")

      print(f'Generating File for user id {user_id}' )
      try:
          # Instantiate Data Genearation Class
          data_generator = DataGenModel(self.bundle_path, self.transformer_version)

          # Run generate_single_user method of Data Generation Class
          results_df = data_generator.generate_single_user(n_days)

          results_df.to_csv(output_file, index = False)
          print(f'{output_file} has been generated')
      except Exception as e:
          print(e)
          # print('Error generating file')
