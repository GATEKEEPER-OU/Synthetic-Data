class DataGenModel:
    '''
    This class should be used to generate FHIR observations for one individual.
    The ultimate goal is to provide a single Tensorflow Serving Model with a set of named signatures.


    Arguments:
        model_dir: str
            The directory that holds the models
        transformer_vers:
            The transformer version
    Output:
        generate_single_user method:
            If output file is None, a dataframe is returned to the calling program.
            Otherwise, the output file is created and None is returned to the calling progam.

    To run:
        Import the class
        Instantiate the class
        Run the generate_single_user method
    '''
    from synthetic_data.transformers.SAM_GK_FHIR_1.datagen.custom import PositionalEmbedding
    from gensim.models.doc2vec import Doc2Vec
        
    import os
    import tensorflow as tf
    import numpy as np
    import pandas as pd
    import json
    #np.random.seed(1)

    def __init__ (self,
      model_dir: str,
      transformer_vers: str
    ):
        self.transformer_vers = transformer_vers
        self.model_dir = model_dir

        self.OBSERVATION_SEQUENCE_LENGTH = 98
        self.OBSERVATION_START = "[START]"
        self.OBSERVATION_END = "[END]"

        # Load the embeddings
        doc2vec_fname = self.os.path.join(self.model_dir, 'embeddings', 'doc2vec_size512')
        self.doc2vec_model = self.Doc2Vec.load(doc2vec_fname)
       
        def load_model(model_name: str, custom_objects=None):
            import warnings
            warnings.filterwarnings("ignore", category=DeprecationWarning) 
            
            # Model Loader
            fname = self.os.path.join(self.model_dir, self.transformer_vers, model_name)

            if custom_objects == None:
                model = self.tf.keras.models.load_model(fname, compile=False)
            else:
                model = self.tf.keras.models.load_model(fname, custom_objects)
            return model
        
        # Load the transformer model
        self.transformer = load_model('SAM_FHIR', custom_objects={'PositionalEmbedding': self.PositionalEmbedding})
        
        # Load the input tokenizer
        source_tokens_model = load_model('sourceTokenLayer')
        self.sourceTextProcessor = source_tokens_model.layers[0]

        # Load the output tokenizer and create lookup for predictions
        target_tokens_model = load_model('targetTokenLayer')
        self.targetTextProcessor = target_tokens_model.layers[0]

        obs_vocab = self.targetTextProcessor.get_vocabulary()
        self.obs_index_lookup = dict(zip(range(len(obs_vocab)), obs_vocab))

        
    def _get_document_input(self):
        # We use a document tag as the input to the encoder
        tlist = self.doc2vec_model.dv.index_to_key

        random_doc_id = self.np.random.randint(len(self.doc2vec_model.dv))
        tag = tlist[random_doc_id-1]
        self.document = tag.split()[0]

        self.tag_list = [x for x in tlist if x.startswith(self.document)]


    def _check_doc(self, observationTimeDifference):
        time_secs = observationTimeDifference.split()
        
        if len(time_secs) != 2:
            return 0
        
        if (not time_secs[0].isdigit()) or (time_secs[1] != 'secs'):
            return 0
        return int(time_secs[0])
    

    def _check_document_similarity(self, input, observations):
        from sklearn.metrics.pairwise import cosine_similarity
        
        most_similar = -1
        similarity = -1.0

        document_tag_vector = self.doc2vec_model.dv[input]

        for num_obs, observation in enumerate(observations):
            query_tokens = observation.split()
            query_vector = self.doc2vec_model.infer_vector(query_tokens)

            sim = cosine_similarity(self.np.array([document_tag_vector]), self.np.array([query_vector]))

            if sim[0] > 0 and sim[0] > similarity:
                similarity = sim[0]
                most_similar = num_obs
                 
        return most_similar

    # Generate data for one user
    def generate_single_user(self, n_days=1, max_times=10):
        from datetime import timezone, datetime, timedelta
        timeNow = datetime.now(timezone.utc)

        columns = ['normTime', 'observation']
        resultsDF = self.pd.DataFrame(columns = columns)

        self._get_document_input()
        n_times = 0

        for input in self.tag_list:
            if n_times > max_times:
                break

            if int(input.split()[1]) > n_days:
                # Continue for now. We should probably sort and break
                continue

            tokenized_input= self.sourceTextProcessor([input])
            
            # TODO: Have one list of lists
            decoded_outputs = []
            json_outputs = []
            normTime_list = []

            for temp in range(1,11):
                decoded_output = self.OBSERVATION_START

                # Generate data for different temperatures
                temperature = 0.1 * temp

                for i in range(self.OBSERVATION_SEQUENCE_LENGTH):

                    tokenized_target = self.targetTextProcessor([decoded_output])[:, :-1]

                    predictions = self.transformer.predict([tokenized_input, tokenized_target], verbose=0)
                    preds = predictions[0, i, :]

                    preds = self.np.asarray(preds).astype("float64")
                    
                    self.np.seterr(divide='ignore')
                    preds = self.np.log(preds) / temperature
                    exp_preds = self.np.exp(preds)
                    preds = exp_preds / self.np.sum(exp_preds)
                    probas = self.np.random.multinomial(1, preds, 1)
 
                    sampled_token_index = self.np.argmax(probas)
                    sampled_token = self.obs_index_lookup[sampled_token_index]

                    if sampled_token == self.OBSERVATION_END:
                        break
                    decoded_output += " " + sampled_token

                decoded_output = decoded_output.replace(self.OBSERVATION_START, "").strip()
                decoded_output = input + " " + decoded_output

                observation = " ".join(decoded_output.split()[3:])

                # Verify JSON and update times
                observation = observation.replace("'", '"')
                normTime = 0

                try:
                    obsJSON = self.json.loads(observation)
                except:
                    continue

                if 'effectiveDateTime' in obsJSON:
                    observationTimeDifference = str(obsJSON['effectiveDateTime'])
                    normTime = self._check_doc(observationTimeDifference)
                    if normTime == 0:
                        continue
                    obsJSON['effectiveDateTime'] = (timeNow - timedelta(seconds=normTime)).strftime("%Y-%b-%d %X")
                elif 'valuePeriod' in obsJSON:
                    if 'end' in obsJSON['valuePeriod']:
                        end = str(obsJSON['valuePeriod']['end'])
                        endTime = self._check_doc(end)
                        if endTime == 0:
                            normTime = 0
                            continue
                        normTime = endTime
                        obsJSON['valuePeriod']['end'] = (timeNow - timedelta(seconds=endTime)).strftime("%Y-%b-%d %X")

                        if 'start' in obsJSON['valuePeriod']:
                            # "start" is the sleep duration
                            duration = str(obsJSON['valuePeriod']['start'])
                            startTime = self._check_doc(duration)
                            if startTime == 0:
                                normTime = 0
                                continue
                            
                            obsJSON['valuePeriod']['start'] = (timeNow - timedelta(seconds=endTime) - timedelta(seconds=startTime)).strftime("%Y-%b-%d %X")
                elif 'effectiveTiming' in obsJSON:
                    normTime = 0
                    if 'event' in obsJSON['effectiveTiming']:
                        for t, observationTimeDifference in enumerate(obsJSON['effectiveTiming']['event']):
                            eventTime = self._check_doc(str(observationTimeDifference))
                            if eventTime == 0:
                                normTime = 0
                                break
                            obsJSON['effectiveTiming']['event'][t] = (timeNow - timedelta(seconds=eventTime)).strftime("%Y-%b-%d %X")
                            
                            if eventTime > normTime:
                               normTime =  eventTime
                        if normTime == 0:
                            continue
                else:
                    normTime = 0
                    continue

                if normTime > 0:
                    decoded_outputs.append(decoded_output)
                    json_outputs.append(obsJSON)
                    normTime_list.append(normTime)

            if len(decoded_outputs) == 0:
                continue
            else:
                doc_index = self._check_document_similarity(input, decoded_outputs)
                if doc_index == -1:
                    continue
            
            resultsDF.loc[len(resultsDF.index)] = [normTime_list[doc_index], json_outputs[doc_index]]
            n_times = n_times + 1

        # There may be gaps in the results. We want to keep the best
        # We coulcd simply just output everything, but n_days will be redundant
        if len(resultsDF) > 0:
            minNT = min(resultsDF['normTime'])
            maxNT = max(resultsDF['normTime'])

            # Get minimum and maximum times generated
            n_keep_min = minNT
            n_keep_max = maxNT
          
            times = sorted(list(resultsDF['normTime'].unique()))
            n_between = 0

            # Total number of seconds we wish to output
            n_seconds = n_days * 86400

            for i, t1 in enumerate(times):
                # We only want to output up to n_days
                max_time = min(t1 + n_seconds, maxNT)

                # Check the future times
                j = i + 1
                for k, t2 in enumerate(times[j:]):
                    if t2 > max_time:
                        # We have all we need
                        break
                    if (k-i) > n_between:
                        n_between = k - i
                        n_keep_min = t1
                        n_keep_max = t2
                    if max_time == maxNT:
                        # We have the maximum number
                        break
            resultsDF = resultsDF.loc[(resultsDF['normTime'] >= n_keep_min) & (resultsDF['normTime'] <= n_keep_max)]
        resultsDF.drop(['normTime'], axis=1, inplace = True)

        return resultsDF
