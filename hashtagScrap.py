import numpy as np
import scrap,general
import streamlit as st
import pandas as pd
from geopy import geocoders
import matplotlib.pyplot as plt
import seaborn as sns
plt.xkcd()

def runHashTagScrap(debug_mode):

    st.title('Tweeter Sentiment Analysis')

    dialogue = st.text("FOR EDUCATIONAL PURPOSE ONLY")


    if debug_mode == True:
        st.text('WebApp in DEMO MODE.\nShowing Data for #DogeToTheMoon')
        tag = 'DogeToTheMoon'
        data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/doge_to_moon.csv')
    else:
        st.text('WebApp in SCRAP MODE.\nEnter the tweet information you want to scrap.')
        st.text('Be patient with Twitter API\nYou can scrap max 500 Tweets')

        n_twts = st.number_input("How many tweets to Scrap : ",10)
        
        tag = st.text_input("Enter Hashtag : ")
        if tag: 
            scrap.start(tag, general.getDate(1), min(n_twts,500))
            data = pd.read_csv('/Users/macbookpro/Desktop/Tweeter_Sentiment_Analysis/temp.csv')

    cleanData = data
    cleanData['text'] = general.cleaned(cleanData['text'])
    cleanData['text'] = cleanData['text'].apply(lambda x : general.remove_stopwords(x))

    if not tag:
        pass
    else:

        if st.checkbox('Show raw data'):
            st.write('## Scrapped Raw Data',data)

        if st.checkbox('Words per Tweet'):
            word_count = cleanData['text'].str.split().apply(len).value_counts()
            word_dict = dict(word_count)
            word_dict = dict(sorted(word_dict.items(), key=lambda kv: kv[1]))

            ind = np.arange(len(word_dict))
            fig0,ax0 = plt.subplots()
            plt.figure(figsize=(20,5))
            
            ax0.bar(ind, list(word_dict.values()))

            plt.ylabel('Number of Tweets')
            plt.xlabel('Number of words in each Tweet')
            plt.title('WORDS PER TWEET')
            plt.xticks(ind, list(word_dict.keys()))
            st.pyplot(fig0)

        if st.checkbox('Most Retweeted Tweets'):
            general.mostRetweeted(10,data)

        sentiments = pd.DataFrame(data = general.getSentiment(cleanData['text']),columns = ['neg','neu','pos','comp'])
        cleanData = pd.concat([cleanData, sentiments], axis=1)

        if st.checkbox('Sentiment Analysis'):
            
            
            fig1,ax = plt.subplots()
            ax.bar(['Positive','Negative'],[sentiments['comp'][sentiments['comp']>0].shape[0],sentiments['comp'][sentiments['comp']<0].shape[0]],color=['#668cff','#ff5050'])
            plt.title("NEGATIVE vs POSITIVE")
            st.pyplot(fig1)

            fig2, axes = plt.subplots(1, 2, figsize=(18, 10))
            plt.suptitle('Distribution Of Index Scores',fontsize='xx-large')
            sns.distplot(ax=axes[0], a=sentiments['pos'],color='b',axlabel = 'Positive Index').set_title('Positive')
            sns.distplot(ax=axes[1], a=sentiments['neg'],color='r',axlabel = 'Negative Index').set_title('Negative')
    
            # sns.distplot(ax=axes[1, 0], a=sentiments['neu'],color='g').set_title('Neutral')
            # sns.distplot(ax=axes[1, 1], a=sentiments['comp'],color='y').set_title('Compound')
            
            st.pyplot(fig2)

        if st.checkbox('WordClouds'):
            postves = general.getTop(30,'pos',cleanData)
            general.showWordCloud(postves,'POSITIVE')
            negtves = general.getTop(30,'neg',cleanData)
            general.showWordCloud(negtves,'NEGATIVE')

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