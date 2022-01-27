
import res

from flask import Flask , render_template, request 
app = Flask(__name__,template_folder='template', static_folder='static')

from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet = True)




article = Article('https://minorprojectwork.blogspot.com/2021/12/data-of-earth-earth-is-fifth-largest.html')
article.download()
article.parse()
article.nlp()
corpus = article.text

text = corpus
sentence_list = nltk.sent_tokenize(text)

def greeting_response(text):
  text = text.lower()

  user_greetings = ['hello','hi','hey','whats up','hii','hiii','heyy','hola']

  bot_greetings = ['Hi, Thanks so much for reaching out! What brings you here today?','Hello,  how can we help you today?','Hey, thanks for your visit, how can i help you?','Hey there, how can i help you','Hi, how are you doing','hello, what are you looking for today?','Hey there, welcome to our store']

  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

def exit_response():
  bot_exit_responses = ['Bye, have a nice day','Bye, see you later', 'Bye, hope i answered your queries','Bye, see you soon']

  return random.choice(bot_exit_responses)


def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0,length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp

  return list_index  

def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response = ''
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1],cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index = index[1:]
  response_flag = 0

  k = 0

  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.25:
      bot_response = bot_response + ' '+ sentence_list[index[i]]
      response_flag = 1
      k= k+1
    
    if k >= 1:
      break
  
  if response_flag == 0:
    bot_response = bot_response+' '+ 'I dont understand'

  sentence_list.remove(user_input)

  return bot_response  

  

exit_list = ['exit','bye','see you later','quit','thanks','thankyou','thank you']

def response(user_input):
    if user_input.lower() in exit_list:
        r = exit_response()
        return r

    else:
        if greeting_response(user_input) != None:
            r =  greeting_response(user_input)
            return r
        if res.site_response(user_input) != None:
            r =  res.site_response(user_input)
            return r
        if res.site_response2(user_input) != None:
            r =  res.site_response2(user_input)
            return r
        if res.site_response3(user_input) != None:
            r =  res.site_response3(user_input)
            return r
        if res.site_response4(user_input) != None:
            r =  res.site_response4(user_input)
            return r
        else:
            r =  bot_response(user_input)
            return r

@app.route("/")
def main():
    return render_template("Main.html")

@app.route("/Home.html")
def home():
    return render_template("Home.html")

@app.route("/Store.html")
def store():
    return render_template("Store.html")

@app.route("/Contact-Us.html")
def contact():
    return render_template("Contact-Us.html")

@app.route("/Main.html")
def main2():
  return render_template("Main.html")

@app.route("/Register.html")
def register():
  return render_template("Register.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")
    return str(response(userText))

if __name__ == '__main__':
    app.run()
