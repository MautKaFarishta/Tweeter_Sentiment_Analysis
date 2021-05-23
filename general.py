import datetime
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit as st
from collections import Counter
# nltk.download()
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')

@st.cache
def getDate(d):
    curr = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
    return curr

# @st.cache
def getLatLong(loc_series):
    waitText = st.text('Plotting Map...')
    prog = st.progress(0)
    latLong = pd.DataFrame(columns = ['lat','lon'])
    geolocator = Nominatim(user_agent="OmkarKhilari")
    maxIdx = 1000
    cityCount = {}; cityLatLong = {};idx=0

    cityCount = Counter(loc_series)

    cityCount = Counter(dict((k, v) for k, v in cityCount.items() if type(k)!=float))

    for city in cityCount.most_common(min(maxIdx,len(cityCount))):
      idx+=1
      if city in cityLatLong:
        pass
      else:
        ct = geolocator.geocode(city,timeout=None)
        if ct:
            cityLatLong[city[0]] = [ct.latitude,ct.longitude]
      prog.progress((idx/maxIdx)/2)

    idx = 0
    for loctn in cityLatLong:
          for k in range(cityCount[loctn]):
            latLong.loc[len(latLong)] = cityLatLong[loctn]
          prog.progress(0.5+(idx/len(cityLatLong))/2)

    prog.empty()
    waitText.empty()
    
    return latLong

@st.cache
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

@st.cache
def remove_stopwords(text):
  stop_words = stopwords.words('english')
  word_tokens = word_tokenize(text)
  filtered_sentence = [w for w in word_tokens if not w in stop_words]
  return " ".join(filtered_sentence)

@st.cache
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