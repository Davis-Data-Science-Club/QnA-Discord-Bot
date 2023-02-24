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
pool3= ['get to know the officer team ', 'who are the officers and what do they do?', 'who is in the officer team']
pool4=['what has been accomplished so far?', 'greatest accomplishment?']
pool5= ['what do you do in the club?', 'what happens in the club?']
pool6=['club’s goal?', 'what is the purpose of this club?', 'future goals?']
pool7=['what type of events does your club offer?', 'what events does your club have?', 'any cool events?']
pools=[pool1, pool2, pool3, pool4, pool5, pool6, pool7]

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
reply= {"Our website can be found here: https://davisdsc.com/": pool1, "We accept all majors.": pool2, "Our current officer team can be found in this part of our website: https://davisdsc.com/about": pool3, "All our accomplishments can be found in our GitHub page: https://github.com/Davis-Data-Science-Club": pool4, "Each quarter we offer workshops about data science topics, talks with industry veterans, project involvement, and much more": pool5,
        "We are on a mission to foster a supportive community centered around developing technical skill sets, career building through industry guest speakers, and enhancing student body engagement." : pool6,
        "Each quarter we offer workshops about data science topics, talks with industry veterans, project involvement, and much more.": pool7}
keyl= list(reply.keys())
vall= list(reply.values())
answer= keyl[vall.index(question)]
print(answer)
