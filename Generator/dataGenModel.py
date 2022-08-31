class DataGenModel:
    import uuid
    import os
    import numpy as np
    from random import randint
    import json
    import pandas as pd
   
    import tensorflow as tf
    
    # Imports config.py
    import config


    def __init__ (self, start_code, maxTimings=1, timingTemperature=0.1, eventTemperature=0.2):
        self.start_code = start_code
        self.max_timings = maxTimings
        self.timing_temperature = timingTemperature
        self.event_temperature = eventTemperature

        unique_filename = str(self.uuid.uuid4()) + ".csv"

        self.results_file = self.os.path.join(self.config.RESULT_DIR, unique_filename)
        
        # Load the vocabulary for timings
        tf = open(self.config.timings_vocab, "r")
        
        # Create timing mappings
        self.idx_to_word = self.json.load(tf)
        self.idx_to_word = dict((int(idx), word) for (idx, word) in self.idx_to_word.items())
        self.word_to_idx = dict((word, int(idx)) for (idx, word) in self.idx_to_word.items())
            
        # Length of the vocabulary   
        self.timings_vocab_size = len(self.idx_to_word) + 1

        # Load the vocabulary for events
        ef = open(self.config.events_vocab, "r")

        # Create event mapings
        self.idx_to_char = self.json.load(ef)
        self.idx_to_char = dict((int(idx), char) for (idx, char) in self.idx_to_char.items())
        self.char_to_idx = dict((char, int(idx)) for (idx, char) in self.idx_to_char.items())    
        
        # Length of the vocabulary
        self.events_vocab_size = len(self.idx_to_char)


    def _generate_seed_text(self):
        user = self.randint(1, self.config.MAX_NUM_REAL_USERS)
        if user == 82:
          # There was an issue with user 82, so this is rejected
          user = 83
        return self.start_code + " " + str(user)


    def _get_codings(self):
      codingDF = self.pd.read_csv(self.config.codingFile)
      coding = codingDF['coding'].values.tolist()
      display = codingDF['display'].values.tolist()
      guide_text = codingDF['guide_text'].values.tolist()
      return coding, display, guide_text


    def _generate_timings(self, seed_text, num_next_words):
        '''
        Generate timings from a seed text.
        
        Arguments:
          seed_text
            Either <coding>, <coding user>, <coding user time>
          num_next_words
            Number of "words" to generate.  
        '''
        seed_len = len(seed_text.split())
        total_len = seed_len + num_next_words
        
        if (seed_len > 3) or  (total_len > self.config.TIMING_SEQ_LEN):
            print("Error in input")
        else:
            for _ in range(num_next_words):
                # Preprocess data - Add Lambda Layer to model? Install Keraa rather than Tensorflow?
                #token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
                # Converting our start string to numbers (vectorizing)
                token_list = [self.word_to_idx[s] for s in seed_text.split()]
                #token_list = self.tf.expand_dims(token_list, 0)
                
                # Does not work in TensorFlow 2.9. Instead, try the line below.
                # token_list = self.tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=self.TIMING_SEQ_LEN-1, padding='pre')

                # Uncomment for Tensorflow 2.9
                token_list = self.tf.keras.utils.pad_sequences([token_list], maxlen=self.config.TIMING_SEQ_LEN-1, padding='pre')
                
                # Run model to infer next probabilities
                predicted = self.config.TIMING_MODEL.predict(token_list, verbose=0)
                
                if self.timing_temperature <= 0.0:
                    # Prediction is the ID associated with the highest logit.
                    predicted_id = self.np.argmax(predicted, axis=1)[-1]
                else:
                    # Get random next word
                    predicted_id = predicted / self.timing_temperature
                    
                    # Use numpy here, instead of Tensorflow?
                    predicted_id = self.tf.random.categorical(predicted_id, num_samples=1)[-1,0].numpy()

                output_word = self.idx_to_word[predicted_id]                  
                seed_text += " " + (output_word)
        return seed_text


    def _generate_events(self, start_string):
        '''
        Generate events from a start string.
              
        Arguments:
            start_string
        '''

        # Converting our start string to numbers (vectorizing)
        input_eval = [self.char_to_idx[s] for s in start_string]
        input_eval = self.tf.expand_dims(input_eval, 0)
            
        # Create a mask to prevent "[UNK]" from being generated.
        skipid = self.char_to_idx[self.config.EVENT_UNKNOWN_TOKEN]
        skip_id = self.tf.constant([[skipid]], dtype=self.np.int64)
            
        sparse_mask = self.tf.SparseTensor(
        # Put a -inf at each bad index.
        values=[-float('inf')]*len(skip_id), 
                indices=skip_id,
                # Match the shape to the vocabulary
                dense_shape=[self.events_vocab_size])
                    
        prediction_mask = self.tf.sparse.to_dense(sparse_mask)
            
        # Empty string to store our results
        text_generated = []
            
        self.config.EVENT_MODEL.reset_states()
        # num_samples = self.events_vocab_size + 1
            
        for i in range(self.config.EVENT_SEQ_LEN):
            # Run Model
            predictions = self.config.EVENT_MODEL.predict(input_eval, verbose=0)
                
            # remove the batch dimension
            predictions = self.tf.squeeze(predictions, 0)
                
            # Apply the prediction mask: prevent "[UNK]" from being generated.
            predictions = predictions + prediction_mask
                
            if self.event_temperature <= 0.0:
                # Prediction is the ID associated with the highest logit. 
                predicted_id = self.np.argmax(predictions, axis=1)[-1]
            else:
                # Low temperatures results in more predictable text
                # Higher temperatures results in more surprising text.
                # Experiment to find the best setting.
                predictions = predictions / self.event_temperature
                    
                # EXPERIMENTATION: Get a number of samples and select the ID that occurs the most
                predicted_id = self.tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
                # predicted_ids = self.tf.random.categorical(predictions, num_samples=num_samples)[-1,0].numpy()
                # predicted_id = predicted_ids.max()
                    
            next_char = self.idx_to_char[predicted_id]
            if next_char == self.config.EVENT_PADDING_END_TOKEN:
                break
            
            text_generated.append(next_char)
            
            # We pass the predicted token as the next input to the model
            # along with the previous hidden state
            input_eval = self.tf.expand_dims([predicted_id], 0)
        return (start_string + ''.join(text_generated))

    
    # Generate data for one user
    def generate_single_user(self):
        import pandas as pd
        from datetime import timezone, datetime, timedelta

        coding, display, guide_text = self._get_codings()
             
        # Generate Timings
        timing = []
        start_text = self._generate_seed_text()
        user = start_text.split()[1]
            
        for i in range(self.max_timings):
            if i == 0:
                # The first call will generate 2 timings
                result = self._generate_timings(start_text, 4)
                timings = " ".join(result.split()[0:3])
            elif i == 1:
                # We already have the timing
                timings = " ".join(result.split()[3:])
            else:
                # Now the 2nd timing of the previous is the 1st timing of the next 
                start_timing = timings
                timings = self._generate_timings(start_timing, 3)
                timings = " ".join(timings.split()[3:])

            # Enhancement: Implement Retries   
            if (timings.split()[1] != user) or not timings.split()[-1].isdigit() or (timings.split()[0] not in coding):
                print("Incorrect timing generated: ", timings)
                # Exit if returned user is differrent to input user or if time is not an integer or coding is not known
                break
        
            timing.append(timings)
        
        # Remove duplicates and sort by time. 
        # There were duplicates in the raw data, but we removed them, to avoid the risk of generating too many duplicates.
        timings = list(set(timing))

        # Sort timings by time
        def _by_time(ele):
            return int(ele.split()[2])
        
        timings = sorted(timings, key=_by_time)
        maxTime = timings[-1].split()[2]
        
        columns = ['Observation Time', 'Temperature', 'normTime', 'event']
        resultsDF = pd.DataFrame(columns = columns)

        # We want to generate past times
        timeNow = datetime.now(timezone.utc) - timedelta(seconds=int(maxTime))
        
        # Generate Events
        for j in timings:
            code = j.split()[0]
            coding_index = coding.index(code)
            
            start_string = j + " {'display': '" + display[coding_index] + "', " + guide_text[coding_index]
            event = self._generate_events(start_string)

            normTime = j.split()[2]
            generatedTime = timeNow + timedelta(seconds=int(normTime))
            obsTime = generatedTime.strftime("%Y-%b-%d %X")

            resultsDF.loc[len(resultsDF.index)] = [obsTime, self.event_temperature, normTime, event]

        resultsDF.to_csv(self.results_file, index=False)

        return self.results_file