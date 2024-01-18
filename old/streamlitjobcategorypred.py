import joblib
import numpy as np
import keras.models

from old.preprocessing.strings import ultimate_text_preprocessing
import gensim.downloader as api


def vectorize_for_classification(sentences: list[str], wv):
    """
    Given a list of sentences, generates the vector embeddings of all the sentences, from the word2vec model keyed vectors
    :param sentences: list of sentences
    :param wv: word2vec model keyed vectors
    :return: numpy array of vector embeddings of all the sentences
    """
    return np.array(list(map(wv.get_mean_vector, sentences)))
    pass


CV = """
Class 1 HGV Driver 

Hampton-in-Arden, Solihull, B92 0LP 
Our client is looking for a Class 1 qualified driver to mainly shunt finished product/stock between its main production yard and local storage depot. 
Driver will be required to move stock between 2 local yards as well as helping out with mill collections from time to time. There is also occasional need for some loading/unloading of stock using a Moffett Mounty or C Balance FLT (Licenses provided) as well as some general yard shunting (Training provided). 
 Hours:   45 Hour per week minimum - Monday - Friday plus every other Saturday 
 Salary/Wage:  £11.90 per hour 
 To apply for this Class 1 HGV Driver role, please submit your current CV and contact details online or call 01675 443 888.  
Orange Recruitment is advertising this position on behalf of our client. By clicking apply you accept that your application will be forwarded to only this client in order for them to consider you for the role. 
 

Job Summary

                             
                     
                         Location 
                             Hampton in Arden, MID B920LP 
                     
                 
                             
                     
                         Job type 
                         Full Time, Permanent 
                     
                 
                 
                     
                         Posted 
                         Today 
                     
                 
                 
                     
                         Industries 
                         Transport and Storage - Materials  
                     
                 
                 
                     
                         Education level 
                         Unspecified 
                     
                 
                 
                     
                         Career level 
                         Entry Level 
                     
                 
                             
                     
                         Reference code 
                         OR/AWS/0619C1
"""

# %%

# 0. Prepare joblib
persistence = joblib.load("dumps/persistence.joblib")

# 1. Text preprocessing

# X_pred = ultimate_text_preprocessing([CV])
# %%

# 2. Load the pre-trained Gensim word2vec

glove_vector = api.load("glove-twitter-25")  # load glove vectors
# %%

# 3. Get the word vectors
# X_pred_vectors = vectorize_for_classification(X_pred, glove_vector)

# 4. Load the Keras model
loaded_model = keras.models.load_model(persistence["Job_Category_Classifier"])
# %%

# 5. Make predictions from the model
# y_pred = loaded_model.predict([X_pred_vectors])

# 6. Load the One Hot Encoder used in training, to get the class label (the job category)
loaded_enc = joblib.load(persistence["OneHotEncoder"])
# job_categories = loaded_enc.inverse_transform(y_pred)

# Return predicted job category
# job_category = job_categories[0][0]
# %%

# Return a list of jobs in the given job category
# job_df = pd.read_csv('job_descriptions.csv')


# BM = job_df["category"] == job_category
# l_jobs: pd.DataFrame = job_df[BM].head(20)


def pred_job_category(cv: str) -> str:
    X_pred = ultimate_text_preprocessing([cv])
    X_pred_vectors = vectorize_for_classification(X_pred, glove_vector)
    y_pred = loaded_model.predict([X_pred_vectors])
    job_categories = loaded_enc.inverse_transform(y_pred)
    job_category = job_categories[0][0]
    return job_category
    pass

# %%
