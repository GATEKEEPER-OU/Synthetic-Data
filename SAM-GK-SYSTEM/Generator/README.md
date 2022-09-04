## This Directory contains Python Data Generation scripts that can be run from the command line. The scripts have been tested with Python 3.10 and Tensoflow 2.9.

### You must have trained models in HDF5 format and the vocabulary files that were saved during training of the model. These scripts were created for testing of the models. For deployment, best practices should be considered.

The necessary directories are set in the config.py file, which should be updated if necessary.

### dataGenModel.py along with config.py and the files in the static directory represents the Data Generator. It requires access to a model. 

### test_app.py ((Run Data Generator from command line)

To run:

python test_app.py code maxEvents eventTemperature

where code is a code which must be included, maxEvents is the maximum nuber of events to be generated for a user, eventTemperature is a value between 0 and 1 and represents the diversity of the prediction probabilities.

### app.py (Run Data Generator from web frontend)
Simple Front-end. Use to test deployment.

To run:

python app.py

### test_app_batch.py (Run Data Generator with parameters set in script)

To run:

python app.py

### transferResultsToMiddleware.py
Transfer result files, which contain the generated data in text format to Middleware assuming the Middleware resides on the same system. The file should be adapted to suit. Middleware is responsible for reformatting the files and transferring the file to downstream systems.

To run:

python transferResultsToMiddleware.py
