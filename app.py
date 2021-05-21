import scrap,general
import streamlit as st
import pandas as pd
from geopy import geocoders

st.title('Tweeter Sentiment Analysis')
data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/scraped_tweets.csv')

dialogue = st.text("We are keeping some limitation not to void to polycies of tweeter")
n_twts = st.number_input("How many tweets to Scrap : ")
tag = st.text_input("Enter Hashtag : ")

data = scrap.start(tag, general.getDate(1), n_twts)

st.dataframe(data)
# st.map(data['location'])