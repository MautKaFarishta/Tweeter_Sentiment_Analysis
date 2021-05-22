import scrap,general
import streamlit as st
import pandas as pd
from geopy import geocoders
import matplotlib.pyplot as plt

debug_mode = True

st.title('Tweeter Sentiment Analysis')

dialogue = st.text("FOR EDUCATIONAL PURPOSE ONLY")
n_twts = st.number_input("How many tweets to Scrap : ",100)
tag = st.text_input("Enter Hashtag : ")

if debug_mode == True:
    data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/doge_to_moon.csv')
else:
    a = st.text(f'Scraping Tweets for {tag}')
    data = scrap.start(tag, general.getDate(1), n_twts)
    a.text('')

if data.empty:
    pass
else:
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    if st.checkbox('Sentiment Analysis'):
        st.subheader('Positive Vs Negative')
        data['text'] = general.cleaned(data['text'])
        data['text'] = data['text'].apply(lambda x : general.remove_stopwords(x))
        sentiments = pd.DataFrame(data = general.getSentiment(data['text']),columns = ['neg','neu','pos','comp'])
        fig,ax = plt.subplots()
        ax.bar(['+Ve','-Ve'],[sentiments['pos'][sentiments['pos']>0].shape[0],sentiments['neg'][sentiments['neg']>0].shape[0]],color=['#668cff','#ff5050'])
        plt.title("NEGATIVE vs POSITIVE")
        st.pyplot(fig)

    if st.checkbox('Location'):
        st.subheader('LocationWise Tweets')
        location_grp=data.groupby(by=['location'])
        lob = location_grp['text'].count()
        lob_sorted = lob.sort_values(ascending=False)
        plt.rcdefaults()
        plt.style.use('fivethirtyeight')
        fig1 = plt.figure(figsize=(20,15))
        plt.barh(lob_sorted.index[:40],lob_sorted.values[:40])
        plt.title("Locationwise Number of tweets")
        st.pyplot(fig1)

    if st.checkbox('Map'):
        st.subheader('MapWise Tweets')
        lat_long = general.getLatLong(data['location'])
        st.map(lat_long)