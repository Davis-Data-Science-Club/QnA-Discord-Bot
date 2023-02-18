#importing libraries
import nltk
import sklearn
import numpy as np
from nltk.corpus.reader.tagged import sent_tokenize
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
stopwords= stopwords.words('english')

#user input question, tokenized
ques= "Where can I access the slides?" #will substitute with input() later
sToken= nltk.sent_tokenize(ques)

#question pools (only tried with 2 pools right now, will code it for all of them later
pool1= ['where is your website located', 'where is your website', 'where is your website link']
pool2=['can i join even though i am not in stats/data sciene/cs major', 'how inclusive is your club']
pools=[pool1, pool2]

#formatting function
def format_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    
    return text

#vectorizing and finding similarity of question with all pools
cv= CountVectorizer()
sim_list=[]
for i in pools:
    #formating user question and the question pools
    format_ques=list(map(format_string, sToken))
    format_pool=list(map(format_string, i))
    
    #vectorizing user question and the question pools
    pool_vectorizer= cv.fit_transform(format_pool)
    pool_vectors= pool_vectorizer.toarray()

    ques_vectorize= cv.transform(format_ques)
    ques_vector= ques_vectorize.toarray()

    #cosine similarity
    similarity= sklearn.metrics.pairwise.cosine_similarity(ques_vector, pool_vectors)
    max_sim= np.ndarray.max(similarity)
    sim_list.append(max_sim)

#displaying the answer based on the similarity scores
question= pools[sim_list.index(max(sim_list))] #matching user question to appropriate pool
#dictionary with answers as keys and question pools as values
reply= {"Our website can be found here: https://davisdsc.com/": pool1, "We accept all majors.": pool2}
keyl= list(reply.keys())
vall= list(reply.values())
answer= keyl[vall.index(question)]
print(answer)