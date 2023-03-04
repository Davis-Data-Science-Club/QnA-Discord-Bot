#importing libraries
import nltk
import sklearn
from nltk.corpus.reader.tagged import sent_tokenize
import string
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
stopwords= stopwords.words('english')
from nltk.translate.bleu_score import modified_precision
from nltk import ngrams

#user input question, tokenized
def bot_hi():
  print("hello! How can I help you today?")
bot_hi()
ques= input()
sToken= nltk.sent_tokenize(ques)

#question pools (will program for data from csv file later)
pool1= ['where is your website located where is your website. where is your website link']
pool2=['can i join even though i am not in stats/data sciene/cs major how inclusive is your club']
pool3= ['get to know the officer team. who are the officers and what do they do. who is in the officer team']
pool4=['what has been accomplished so far. greatest accomplishment?']
pool5= ['what do you do in the club? what happens in the club?']
pool6=['club’s goal? what is the purpose of this club? future goals?']
pool7=['what type of events does your club offer? what events does your club have? any cool events?']
pools=[pool1, pool2, pool3, pool4, pool5, pool6, pool7]

#formatting function
def format_string(text):
    text= ''.join([word for word in text])
    text = text.lower()
    text= nltk.word_tokenize(text)
    text = ' '.join([WordNetLemmatizer().lemmatize(word) for word in text])
    text = ''.join([word for word in text if word not in string.punctuation])
    text = ' '.join([word for word in text.split() if word not in stopwords]) 
    turnToString = ''.join([str(elem) for elem in text])
    return turnToString 

#constants for the for-loop
n_ques= format_string(sToken).split()
overlap=[]

#ngramming and finding overlap of question with all pools
for i in pools:
    #formating question pool
    format_pool=format_string(i)

    #ngramming question pool
    np= ngrams(format_pool.split(), 2)
    n_pool=[]
    for n in np:
      n_pool.append(n)

    #calculating overlap
    mp= modified_precision(n_pool, n_ques, 2)
    overlap.append(float(mp))

#variable for the maximum overlap found
max_ol= max(overlap)

#displaying the answer based on the overlap scores
reply= {"Our website can be found here: https://davisdsc.com/": pool1, "We accept all majors.": pool2, "Our current officer team can be found in this part of our website: https://davisdsc.com/about": pool3, "All our accomplishments can be found in our GitHub page: https://github.com/Davis-Data-Science-Club": pool4, "Each quarter we offer workshops about data science topics, talks with industry veterans, project involvement, and much more": pool5,
        "We are on a mission to foster a supportive community centered around developing technical skill sets, career building through industry guest speakers, and enhancing student body engagement." : pool6,
        "Each quarter we offer workshops about data science topics, talks with industry veterans, project involvement, and much more.": pool7}
keyl= list(reply.keys())
vall= list(reply.values())

#accuracy in reply
if max_ol==0: 
  print("I'm sorry, I'm afraid I do not know!")
  question= None

elif max_ol<0.8:
  probable_q= pools[overlap.index(max_ol)]
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
  question= pools[overlap.index(max_ol)] #matching user question to appropriate pool
  answer= keyl[vall.index(question)]
  print(answer)