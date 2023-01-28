class DataGenModel:
    '''
    This class should be used to generate FHIR observations for one individual.
    The observations are produced by a combination of 2 trained Deep Learning Models.
    They should exsit in the models directory in Keras H5 format.
    The vocabulary files should exist in the vocabulary directory.
    The codings file should exist in the codings directory.

    Arguments:
        max_timings : int
            The maximum number of timings, or observation times, to generate.
            At least 1 will be generated. The actual number generated could be less due to:
                the randomly selected user not having enough timings,
                the start timing being too late in the sequence timings, or
                a prediction error prematurely halting the timing generation.
        model_dir: str
            The directory that holds models th
        output_file (Default is None):
            The filename of a csv file that will hold the generated data.
            If None, a dataframe is returned, Otherwise the data is written to the output file.

    Output:
        generate_single_user method:
            If output file is None, a dataframe is returned to the calling program.
            Otherwise, the output file is created and None is returned to the calling progam.

    To run:
        Import the class
        Instantiate the class
        Run the generate_single_user method
    '''
    import numpy as np
    from random import randint, shuffle
    import pandas as pd
    import os
    import warnings

    import tensorflow as tf

    def __init__ (self, max_days: int, model_dir: str, temperature=1.0):
        
        self.temperature = temperature
        self.EVENT_START_TOKEN = "%"
        self.EVENT_END_TOKEN = ";"

        emodel = self.os.path.join(model_dir, 'models', 'event_model.h5')

        # Load Model
        self.warnings.filterwarnings("ignore", category=DeprecationWarning) 
        self.model = self.tf.keras.models.load_model(emodel)

        # Load 
        tokeniser_dir = self.os.path.join(model_dir, 'vocabulary', 'sourceTokenLayer')
        source_tokens_model = self.tf.keras.models.load_model(tokeniser_dir, compile=False)
        self.sourceTextProcessor = source_tokens_model.layers[0]

        # Get vocab
        obs_vocab = self.sourceTextProcessor.get_vocabulary()
        self.obs_index_lookup = dict(zip(range(len(obs_vocab)), obs_vocab))

        # Load Prompts
        codings_file = self.os.path.join(model_dir, 'codings', 'codings.csv')
        codingsDF = self.pd.read_csv(codings_file)

        # Add columns for easier manipulation
        codingsDF['patients'] = codingsDF['prompts'].str.split().str[0]
        codingsDF['timestep'] = codingsDF['prompts'].str.split().str[1]
        codingsDF['normTime'] = codingsDF['prompts'].str.split().str[2]
        codingsDF['normTime'] = codingsDF['normTime'].astype(str).astype(int)
        codingsDF['dayNum'] = codingsDF['normTime'].floordiv(86400).add(1)
        
        # Get Patient Template, start day and end day
        patients_list = list(codingsDF['patients'].unique())
        self.shuffle(patients_list)

        # Default if something goes wrong
        patient_template = patients_list[0]
        start_day = 1
        end_day = max_days

        for patient in patients_list:
            num_daysDF = codingsDF[(codingsDF['patients'] == patient) & (codingsDF['dayNum'] >= max_days)]
            num_days = len(num_daysDF)
            if num_days > 0:
                num_days = num_daysDF['dayNum'].max()
                patient_template = patient
                days_delta = num_days - max_days
                if days_delta == 0:
                    start_day = 1
                    end_day = max_days
                else:
                    days_delta = days_delta + 1
                    start_day = self.randint(1, days_delta)
                    if len(num_daysDF.loc[num_daysDF['dayNum'] == start_day]) == 0:
                        start_day = 1
                    end_day = start_day + max_days - 1
                break
        
        self.templateDF = codingsDF[codingsDF['patients'] == patient_template]
        self.templateDF = self.templateDF.loc[(self.templateDF['dayNum'] >= start_day) & (self.templateDF['dayNum'] <= end_day)]


    def _softmax(self, x):
      max_x = self.np.max(x)
      exp_x = self.np.exp(x - max_x)
      sum_exp_x = self.np.sum(exp_x)
      sm_x = exp_x/sum_exp_x
      return sm_x


    # The prediction loop
    def _generate_events(self, start_string, max_sequence_len):
        input_eval = start_string
 
        # Empty string to store our results
        text_generated = []
 
        self.model.reset_states()
        #num_samples = vocab_size + 1
    
        for i in range(max_sequence_len):
            
            # Run Model
            tokenized_input= self.sourceTextProcessor([input_eval])
            
            predictions = self.model.predict(tokenized_input, verbose=0)
            predictions = self.tf.squeeze(predictions, 0)
                    
            preds = self.np.asarray(predictions)[-1].astype("float64")
            preds = preds / self.temperature
            preds = self._softmax(preds)

            preds = self.np.random.multinomial(1, preds, 1)
            sampled_token_index = self.np.argmax(preds)

            sampled_token = self.obs_index_lookup[sampled_token_index]

            text_generated.append(sampled_token)

            if sampled_token == self.EVENT_END_TOKEN:
                break

            # We pass the predicted token as the next input to the model
            # along with the previous hidden state
            input_eval = sampled_token

        self.text = start_string + ''.join(text_generated)
        
    # Generate data for one user
    def generate_single_user(self):
        from datetime import timezone, datetime, timedelta
        
        maxTime = self.templateDF['normTime'].max()
        
        # We want to generate past times
        timeNow = datetime.now(timezone.utc) - timedelta(seconds=int(maxTime))

        columns =  ['obsTime', 'temperatue', 'observation']
        resultsDF = self.pd.DataFrame(columns = columns)

        for ind in self.templateDF.index:
            prompt = self.templateDF['prompts'][ind]
            start_text = self.EVENT_START_TOKEN + prompt + " "
            
            self._generate_events(start_text, 880)
            if self.text[-1] != ';':
                continue

            generatedTime = timeNow + timedelta(seconds=int(self.templateDF['normTime'][ind]))
            obsTime = generatedTime.strftime("%Y-%b-%d %X")
            self.text = self.text[1:-1]
            self.text = " ".join(self.text.split()[3:])
            resultsDF.loc[len(resultsDF.index)] = [obsTime, self.temperature, self.text]

        return resultsDF