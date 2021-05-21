import scrap,general
import streamlit as st
import pandas as pd
from geopy import geocoders
import matplotlib.pyplot as plt

debug_mode = False

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
        st.subheader('')

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