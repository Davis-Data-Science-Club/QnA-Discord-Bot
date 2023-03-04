#importing libraries
import nltk
import sklearn
import numpy as np
from nltk.corpus.reader.tagged import sent_tokenize
from nltk.stem import WordNetLemmatizer   
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
stopwords= stopwords.words('english')

#user input question, tokenized
def bot_hi():
  print("hello! How can I help you today?")
bot_hi()
ques= input()
sToken= nltk.sent_tokenize(ques)

#question pools (will program for data from csv file later)
pool1= ['where is your website located. where is your website. where is your website link']
pool2=['can i join even though i am not in stats/data sciene/cs major. how inclusive is your club']
pool3= ['get to know the officer team. who are the officers and what do they do. who is in the officer team']
pool4=['what has been accomplished so far. greatest accomplishment?']
pool5= ['what do you do in the club? what happens in the club?']
pool6=['club\’s goal? what is the purpose of this club? future goals?']
pool7=['what type of events does your club offer? what events does your club have? any cool events?']
pools=[pool1, pool2, pool3, pool4, pool5, pool6, pool7]

#formatting
def format_string(text):
    text= ''.join([word for word in text])
    text = text.lower()
    text= nltk.word_tokenize(text)
    text = ' '.join([WordNetLemmatizer().lemmatize(word) for word in text])
    text = ''.join([word for word in text if word not in string.punctuation])
    text = ' '.join([word for word in text.split() if word not in stopwords]) 
    return text

#vectorizing and finding similarity of question with all pools
tv= TfidfVectorizer()
sim_list=[]
for i in pools:
    #formating user question and the question pools
    format_ques=list(map(format_string, sToken))
    format_pool=list(map(format_string, i))
    
    #vectorizing user question and the question pools
    pool_vectorizer= tv.fit_transform(format_pool)
    pool_vectors= pool_vectorizer.toarray()

    ques_vectorize= tv.transform(format_ques)
    ques_vector= ques_vectorize.toarray()

    #cosine similarity
    similarity= sklearn.metrics.pairwise.cosine_similarity(ques_vector, pool_vectors)
    max_sim= np.ndarray.max(similarity)
    sim_list.append(max_sim)

#variable for the maximum similarity found
maxSim= max(sim_list)

#displaying the answer based on the similarity scores
reply= {"Our website can be found here: https://davisdsc.com/": pool1, "We accept all majors.": pool2, "Our current officer team can be found in this part of our website: https://davisdsc.com/about": pool3, "All our accomplishments can be found in our GitHub page: https://github.com/Davis-Data-Science-Club": pool4, "Each quarter we offer workshops about data science topics, talks with industry veterans, project involvement, and much more": pool5,
        "We are on a mission to foster a supportive community centered around developing technical skill sets, career building through industry guest speakers, and enhancing student body engagement." : pool6,
        "Each quarter we offer workshops about data science topics, talks with industry veterans, project involvement, and much more.": pool7}
keyl= list(reply.keys())
vall= list(reply.values())

#tried something for edge cases and accuracy
if maxSim==0: #edge case: when question does not match any pool
  print("I'm sorry, I'm afraid I do not know!")
  question= None

elif maxSim<0.8: #tried a threshold of 0.8 in case there's not a close match of the question
  probable_q= pools[sim_list.index(max(sim_list))]
  print(probable_q)
  print("Was this your question?")
  confirmation= input("Type yes or no:")
  if confirmation=="yes":
    question = probable_q
    answer= keyl[vall.index(question)]
    print(answer)
  else:
      print("I'm sorry, I'm afraid I do not know!")
      question= None

else: #for question that match pools closely
  question= pools[sim_list.index(max(sim_list))] #matching user question to appropriate pool
  answer= keyl[vall.index(question)]
  print(answer)
