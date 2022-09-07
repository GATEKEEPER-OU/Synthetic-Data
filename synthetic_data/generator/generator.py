from model import DataGenModel

class SyntheticDataGenerator:
  import uuid

  # Consider random selection of codings
  start_coding = '41950-7'
  
  temperatures = [0.3, 0.4, 0.8, 0.9, 1.0]
  
  def __init__(self,
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

      # The model is dumb. It does not understand days.
      # Well actually, it can only understand what it has been trained on.
      # We will assume 24 max_timings per day. 
      # Evaluation code will be updated to remove excess days, if necessary.
      # We either pass n_days to evaluator or add number of days required to filename
      max_timings = n_days * 24 
      
      for i, event_temperature in enumerate(self.temperatures, start=1):
        # A File could be evaluated as fake in relation to the data that the model is trained on.
        # Generate a number of files to be evaluated.
        userno = str(i)
        output_file = output_dir + '/' + userId + "_" + userno + ".csv"
        
        print(f'Generating File {userno} for user id {userId}' )
        try:
          data_generator = DataGenModel(max_timings, output_file, self.start_coding, 
                                    self.event_model, self.timing_model, 
                                    self.events_vocab, self.timings_vocab, self.codings_file,
                                    eventTemperature = event_temperature)
          data_generator.generate_single_user()
          print(f'{output_file} has been generated and is ready to be transferred for evaluation')
        except:
          print('Error generating file')
     
    
    #print("%s" % self.msg)
    #print(" - num of patients: %d" % n_patients)
    #if n_days is not None:
    #  print(" - num of patients: %d" % n_days)
