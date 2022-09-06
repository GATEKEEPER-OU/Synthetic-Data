
class SyntheticDataGenerator:

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

  def generate(self, n_patients: int, n_days: int=None):
    print("%s" % self.msg)
    print(" - num of patients: %d" % n_patients)
    if n_days is not None:
      print(" - num of patients: %d" % n_days)
