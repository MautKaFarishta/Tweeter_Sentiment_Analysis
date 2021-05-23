import numpy as np
import scrap,general
import streamlit as st
import pandas as pd
from geopy import geocoders
import matplotlib.pyplot as plt
import seaborn as sns
plt.xkcd()

debug_mode = False

st.title('Tweeter Sentiment Analysis')

dialogue = st.text("FOR EDUCATIONAL PURPOSE ONLY")


if debug_mode == True:
    st.text('App in DEBUG MODE.\nShowing Data for #DogeToTheMoon')
    tag = 'DogeToTheMoon'
    data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/doge_to_moon.csv')
else:
    n_twts = st.number_input("How many tweets to Scrap : ",10)
    tag = st.text_input("Enter Hashtag : ")
    if tag: 
        scrap.start(tag, general.getDate(1), n_twts)
        data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/temp.csv')

if not tag:
    pass
else:

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.dataframe(data)

    if st.checkbox('Sentiment Analysis'):
        data['text'] = general.cleaned(data['text'])
        data['text'] = data['text'].apply(lambda x : general.remove_stopwords(x))
        sentiments = pd.DataFrame(data = general.getSentiment(data['text']),columns = ['neg','neu','pos','comp'])
        fig,ax = plt.subplots()
        ax.bar(['Positive','Negative'],[sentiments['comp'][sentiments['comp']>0].shape[0],sentiments['comp'][sentiments['comp']<0].shape[0]],color=['#668cff','#ff5050'])
        plt.title("NEGATIVE vs POSITIVE")
        st.pyplot(fig)

        fig2, axes = plt.subplots(1, 2, figsize=(18, 10))
        plt.suptitle('Distribution Of Index Scores',fontsize='xx-large')
        sns.distplot(ax=axes[0], a=sentiments['pos'],color='b',axlabel = 'Positive Index').set_title('Positive')
        sns.distplot(ax=axes[1], a=sentiments['neg'],color='r',axlabel = 'Negative Index').set_title('Negative')
   
        # sns.distplot(ax=axes[1, 0], a=sentiments['neu'],color='g').set_title('Neutral')
        # sns.distplot(ax=axes[1, 1], a=sentiments['comp'],color='y').set_title('Compound')
        
        st.pyplot(fig2)

    if st.checkbox('Map'):
        st.subheader('MapWise Tweets')
        lat_long = general.getLatLong(data['location'])
        st.map(lat_long)



    # if st.checkbox('Location'):
    #     st.subheader('LocationWise Tweets')
    #     location_grp=data.groupby(by=['location'])
    #     lob = location_grp['text'].count()
    #     lob_sorted = lob.sort_values(ascending=False)
    #     plt.rcdefaults()
    #     plt.style.use('fivethirtyeight')
    #     fig1 = plt.figure(figsize=(20,15))
    #     plt.barh(lob_sorted.index[:40],lob_sorted.values[:40])
    #     plt.title("Locationwise Number of tweets")
    #     st.pyplot(fig1)