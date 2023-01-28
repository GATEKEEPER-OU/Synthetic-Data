import uuid
import os

# Prevent Tensorflow warning messages when no GPU is available
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from synthetic_data.generator2.datagen.model import DataGenModel

class SyntheticDataGenerator:

  # Try various temperatures.
  # 0.9 and 1.0 have been shown to generate reasonable results
  # temperatures = [0.9, 1.0]

  def __init__(self, bundle_path):
    self.bundle_path = bundle_path

  def generate(self, output_dir: str, n_patients: int, n_days=1):

    data_generator = DataGenModel(n_days, self.bundle_path)

    for _ in range(n_patients):

        # Generate user ID
        user_id = str(uuid.uuid4())

        # userno = str(i)

        # output_file = os.path.join(output_dir, user_id + "_" + userno + ".csv")
        output_file = os.path.join(output_dir, user_id + ".csv")

        try:
          # print(f'Generating File {userno} for user id {user_id}' )
          print(f'Generating File for user id {user_id}' )
          results_df = data_generator.generate_single_user()

          results_df.to_csv(output_file, index = False)
          print(f'{output_file} has been generated and is ready to be transferred for evaluation')
        except Exception as e:
          print(e)
          # print('Error generating file')
