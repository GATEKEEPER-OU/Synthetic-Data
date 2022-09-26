class DataGenModel:
    '''
    This class should be used to generate FHIR observations for one individual.
    The ultimate goal is to provide a single Tensorflow Serving Model with a set of named signatures.


    Arguments:
        model_dir: str
            The directory that holds the models
        transformer_vers:
            The transformer version
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
    from synthetic_data.transformers.datagen.custom import PositionalEmbedding
    from gensim.models.doc2vec import Doc2Vec
        
    import os
    import tensorflow as tf
    import numpy as np
    import pandas as pd

    def __init__ (self,
      model_dir: str,
      transformer_vers: str,
      output_file = None,
    ):
        self.output_file = output_file
        self.transformer_vers = transformer_vers
        self.model_dir = model_dir

        self.OBSERVATION_SEQUENCE_LENGTH = 70
        self.OBSERVATION_START = "[START]"
        self.OBSERVATION_END = "[END]"

        # Load the embeddings
        doc2vec_fname = self.os.path.join(self.model_dir, 'embeddings', 'doc2vec_size256')
        self.doc2vec_model = self.Doc2Vec.load(doc2vec_fname)

        # codings file
        self.codings_file = self.os.path.join(self.model_dir, 'embeddings', 'codings', 'codings.csv')
       

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

        
    def _get_encoder_input(self):
        # We use a document tag as the input to the encoder

        if self.start_tag is None:
            
            # Get start of sequence
            for _ in range(50):
                random_doc_id = self.np.random.randint(len(self.doc2vec_model.dv))
                self.start_tag = self.doc2vec_model.dv.index_to_key[random_doc_id]


                if "_" not in self.start_tag:
                    # We want a line number, not the whole document
                    self.start_tag = None
                else:
                    break
            
            self.document_tag = self.start_tag
            if self.start_tag is not None:
                # Maybe someone has been naughty
                self.document = self.document_tag.split('_')[0]
                self.start_observation = int(self.document_tag.split('_')[1])
                self.direction = 'forward'
        else:
            
            # Get next in sequence
            if self.direction == 'forward':
                next_observation = int(self.document_tag.split('_')[1]) + 1
                current_document_tag = self.document + '_' + str(next_observation)
                if current_document_tag in self.doc2vec_model.dv:
                    self.document_tag = current_document_tag
                else:
                    # We have exhausted all the tags. Reverse.
                    self.direction = 'backward'
            
            if self.direction == 'backward':
                current_observation = int(self.document_tag.split('_')[1])
                if current_observation == 0:
                    self.document_tag = None
                else:
                    if current_observation < self.start_observation:
                        current_observation = self.start_observation

                    previous_observation =  current_observation - 1
                    self.document_tag = self.document + "_" + str(previous_observation)


    def _get_codings(self):
        # We need this for validation of generated data

        codingDF = self.pd.read_csv(self.codings_file)
        coding = codingDF['coding'].values.tolist()
        display = codingDF['display'].values.tolist()
        guide_text = codingDF['guide_text'].values.tolist()
        return coding, display, guide_text

    # Generate data for one user
    def generate_single_user(self, temperature, n_days=1):
        coding, display, guide_text = self._get_codings()
        n_secs = n_days * 86400
        
        self.start_tag = None

        if temperature < 0.2:
            temperature = 0.2

        columns = ['temperature', 'doc_tag', 'event']
        resultsDF = self.pd.DataFrame(columns = columns)

        min_secs  = None
        max_secs = None
        num_secs = 0
        while True:
            self._get_encoder_input()
            if self.start_tag is None or self.document_tag is None:
                break
            
            input = self.document_tag.replace("_", " ")

            tokenized_input= self.sourceTextProcessor([input])
            decoded_output = self.OBSERVATION_START

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

            if decoded_output.split()[0].isdigit() and (decoded_output.split()[1] in coding):
                coding_index = coding.index(decoded_output.split()[1])
                if display[coding_index] in decoded_output and guide_text[coding_index] in decoded_output:
                    if min_secs is None:
                        min_secs =  max_secs = int(decoded_output.split()[0])
                    elif min_secs > int(decoded_output.split()[0]):
                        min_secs = int(decoded_output.split()[0])
                    elif max_secs < int(decoded_output.split()[0]):
                        max_secs = int(decoded_output.split()[0])
                
                    num_secs = max_secs - min_secs
                    if num_secs < n_secs:
                        resultsDF.loc[len(resultsDF.index)] = [temperature, self.document_tag, decoded_output]
                    else:
                        break
            else:
                continue

            #normTime = decoded_output.split()[0]
            #code = decoded_output.split()[1]
            #observation = " ".join(decoded_output()[2:])
            #resultsDF.loc[len(resultsDF.index)] = [temperature, normTime, code, observation]

        return resultsDF