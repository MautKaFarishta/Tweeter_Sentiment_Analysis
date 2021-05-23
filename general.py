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
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
# nltk.download()
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')

@st.cache(suppress_st_warning=True)  
def getDate(d):
    curr = str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
    return curr

@st.cache(suppress_st_warning=True)  
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
      if idx == len(cityCount)*0.5:
        waitText.text('This May take a while...')
      prog.progress(((idx/maxIdx)/2)*1.5)

    idx = 0
    for loctn in cityLatLong:
          for k in range(cityCount[loctn]):
            latLong.loc[len(latLong)] = cityLatLong[loctn]
          prog.progress(0.75+(idx/len(cityLatLong))/4)

    prog.empty()
    waitText.empty()
    
    return latLong

@st.cache(suppress_st_warning=True)  
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

@st.cache(suppress_st_warning=True)  
def remove_stopwords(text):
  stop_words = stopwords.words('english')
  word_tokens = word_tokenize(text)
  filtered_sentence = [w for w in word_tokens if not w in stop_words]
  return " ".join(filtered_sentence)

@st.cache(suppress_st_warning=True)  
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

@st.cache(suppress_st_warning=True)  
def showImage(img):
  return st.pyplot(img)

@st.cache(suppress_st_warning=True)
def getTop(nTweets,sent,data):
  d = data.sort_values(by=sent,ascending=False)
  sent_score = []; twit = []
  for sent,tex in zip(d[sent].values,d['text'].values):
    if tex not in twit:
      sent_score.append(sent)
      twit.append(tex)
    if len(twit) > nTweets:
      break

  return twit

def showWordCloud(twit,sentiment):
  plt.style.use('ggplot')
  plt.rcdefaults()
  unique_string=(" ").join(twit)
  wordcloud = WordCloud(width = 1000, height = 500, colormap='tab20c').generate(unique_string)
  plt.figure(figsize=(15,8))
  plt.imshow(wordcloud)
  plt.title(f'TOP WORDS IN TOP {sentiment} TWEETS',fontsize='xx-large')
  st.pyplot(plt)

# @st.cache(suppress_st_warning=True)
def mostRetweeted(nTweets,data):
  d = data.sort_values(by='retweetcount',ascending=False)
  retw_c = []; retw = []
  for ret,tex in zip(d['retweetcount'].values,d['text'].values):
    if ret not in retw_c and tex not in retw:
      retw_c.append(ret)
      retw.append(tex)
    if len(retw) > nTweets:
      break
  st.write(f'## Most Retweeted {nTweets} Tweets :')
  for i in range(nTweets):
    st.text(str(i+1)+'-> '+retw[i])

