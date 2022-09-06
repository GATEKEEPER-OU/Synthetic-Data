from model import DataGenModel

class SyntheticDataGenerator:
  import uuid

  start_coding = '41950-7'
  
  def _init__(self,
    event_model: str,
    timing_model: str,
    events_vocab: str,
    timings_vocab: str,
    codings_file: str
  ):
    self.event_model = event_model
    self.timing_model = timing_model
    self.events_vocab = events_vocab
    self.timings_vocab = timings_vocab
    self.codings_file = codings_file

  def generate(self, output_dir: str, n_patients: int, n_days = 1):
    for _ in range(n_patients):

      # Generate user ID
      userId = str(self.uuid.uuid4())
      
      # File that will hold the generated data for the user
      filename = output_dir + userId + ".csv"

      # We will attempt to generate observations for n_days. At least 1 observation for 1 day will be generated.
      # There is no gaurantee that n_days > 1 will be generated. 
      # This could be due to the randomly selected user not having the required number of days,
      # the start timing being too late in the sequence timings, or a prediction error prematurely 
      # halting the timing generation.
      data_generator = DataGenModel(n_days, self.start_coding, self.event_model, self.timing_model, self.events_vocab,
                                    self.timings_vocab, self.codings_file)
      userDF = data_generator.generate_single_user()
      userDF.to_csv(filename, index=False)
      
    
    #print("%s" % self.msg)
    #print(" - num of patients: %d" % n_patients)
    #if n_days is not None:
    #  print(" - num of patients: %d" % n_days)
