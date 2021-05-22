import datetime
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download()
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')

def getDate(d):
    curr = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
    return curr

def getLatLong(loc_series):
    latLong = pd.DataFrame(columns = ['lat','lon'])
    geolocator = Nominatim(user_agent="OmkarKhilari")
    for location in loc_series[:100]:
        city = geolocator.geocode(location)
        if city:
            latLong.loc[len(latLong)] = [city.latitude,city.longitude]
    
    return latLong

def cleaned(text):
    text = text.str.lower() # lowercase
    text = text.str.replace(r"\#","") # replaces hashtags
    text = text.str.replace(r"http\S+","URL")  # remove URL addresses
    text = text.str.replace(r"@","")
    text = text.str.replace(r"!","")
    text = text.str.replace(r"!","")
    text = text.str.replace(r"[^A-Za-z0-9()!?\'\`\"]", " ")
    text = text.str.replace("\s{2,}", " ")
    return text

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
def remove_stopwords(text):
  word_tokens = word_tokenize(text)
  filtered_sentence = [w for w in word_tokens if not w in stop_words]
  return " ".join(filtered_sentence)

def getSentiment(data):
  ob = SentimentIntensityAnalyzer()
  scores=np.zeros(shape=(len(data),4))

  for e,essay in enumerate(data):
    score = ob.polarity_scores(essay)
    scores[e][0]=score['neg']
    scores[e][1]=score['neu']
    scores[e][2]=score['pos']
    scores[e][3]=score['compound']

  return scores