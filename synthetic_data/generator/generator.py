#from model import DataGenModel
from synthetic_data.generator.model import DataGenModel

class SyntheticDataGenerator:
  import uuid
  import shutil
  import glob

  # Consider random selection of codings
  start_coding = '41950-7'
  
  # Try various temperatures.
  # To date, there has not been enough experimentation to determine the best.
  # Will be done for the paper.
  temperatures = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
  
  def __init__(self, n_patients: int, n_days=1):
    self.n_patients = n_patients
    self.n_days = n_days


  def generate(self, output_dir: str):
    for _ in range(self.n_patients):

      # Generate user ID
      userId = str(self.uuid.uuid4())

      # The model is dumb. It does not understand days.
      # Well actually, it can only understand what it has been trained on.
      # We will assume 50 max_timings per day. 
      max_timings = self.n_days * 50 
      
      for i, event_temperature in enumerate(self.temperatures, start=1):
        # A File could be evaluated as fake in relation to the data that the model is trained on.
        # Generate a number of files to be evaluated.
        userno = str(i)
        output_file = output_dir + '/' + userId + "_" + userno + ".csv"
        
        print(f'Generating File {userno} for user id {userId}' )
        try:
          data_generator = DataGenModel(max_timings, self.start_coding, event_temperature = event_temperature)
          resultsDF = data_generator.generate_single_user()
  
          resultsDF.to_csv(output_file, index = False)
          print(f'{output_file} has been generated and is ready to be transferred for evaluation')
        except:
          print('Error generating file')


  def transfer(self, input_dir: str, output_dir: str):
    
    # Get the csv files from the input directory
    files = self.glob.glob(input_dir + "/*.csv")

    for filename in files:
      self.shutil.copy(filename, output_dir)

    #print("%s" % self.msg)
    #print(" - num of patients: %d" % n_patients)
    #if n_days is not None:
    #  print(" - num of patients: %d" % n_days)
