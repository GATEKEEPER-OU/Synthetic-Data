#from process import process
#from postprocess import postprocess
from synthetic_data.shared.process import process
from synthetic_data.shared.postprocess import postprocess

class SyntheticDataShared:
    ''' 
    This class should be used to process the generated FHIR observations.
    
    Arguments:
        codings_file: str
            The static file that was used in the predictions of the observations

    To run:
        Import the class
        Instantiate the class
        Run the process_generated method to process the generated files
    '''

    import shutil
    import  glob 

    def __init__ (self):
        pass

    
    def process_generated(self, input_dir: str, output_dir: str):
        process(input_dir, output_dir)
        
    
    # Here we could have a number of real files for a user. Select 1 and remove any excess days
    def postprocess_evaluated(self, input_dir: str, output_dir: str):
        postprocess(input_dir, output_dir)


    def transfer(self, input_dir: str, output_dir: str):
    
        # Get the csv files from the input directory
        files = self.glob.glob(input_dir + "/*.csv")

        for filename in files:
            self.shutil.copy(filename, output_dir)