import pandas as pd
import os
import json

def check_embeddings(models_dir, dataframe):
    from gensim.models.doc2vec import Doc2Vec
    import os

     # Load the embeddings
    doc2vec_fname = os.path.join(models_dir, 'embeddings', 'doc2vec_size256')
    doc2vec_model = Doc2Vec.load(doc2vec_fname)

    def _by_integer(ele):
        # Sort by line number within document
        return int(ele.split('_')[1])

    dataframe.sort_values(by=['document_tag'], axis=1, key=_by_integer)
    
        