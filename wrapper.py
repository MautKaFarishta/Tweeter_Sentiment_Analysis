import numpy as np
import scrap,general
import streamlit as st
import pandas as pd
from geopy import geocoders
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import drawings
import scrapUser
import path as p
plt.xkcd()

def runHashTagScrap(debug_mode):

    st.title('Tweeter Sentiment Analysis')

    dialogue = st.text("FOR EDUCATIONAL PURPOSE ONLY")


    if debug_mode == True:
        st.text('WebApp in DEMO MODE.\nShowing Data for #DogeToTheMoon')
        tag = 'DogeToTheMoon'
        data = pd.read_csv(p.path1)
    else:
        st.text('WebApp in SCRAP MODE.\nEnter the tweet information you want to scrap.')
        st.text('Be patient with Twitter API\nYou can scrap max 500 Tweets')

        n_twts = st.number_input("How many tweets to Scrap : ",10)
        
        tag = st.text_input("Enter Hashtag : ")
        if tag: 
            scrap.start(tag, general.getDate(1), min(n_twts,500))
            data = pd.read_csv(p.path3)


    if not tag:
        pass
    else:
        cleanData = data.copy()
        cleanData['text'] = general.cleaned(cleanData['text'])
        cleanData['text'] = cleanData['text'].apply(lambda x : general.remove_stopwords(x))

        st.markdown('## **View Analysis**')
        Analysis = st.selectbox('Select Analysis',
            ['Show Raw Data','Tweet Text Analysis','Sentiment Analysis','Location Analysis'])

        sentiments = pd.DataFrame(data = general.getSentiment(cleanData['text']),columns = ['neg','neu','pos','comp'])
        cleanData = pd.concat([cleanData, sentiments], axis=1)
        
        if Analysis == 'Show Raw Data':
            drawings.drawRawData(data)
            
        elif Analysis == 'Tweet Text Analysis':
            drawings.drawWordsPerTweet(cleanData)
            drawings.drawWordCloud(cleanData)
            drawings.drawMostRetweeted(10,data)
            
        elif Analysis == 'Sentiment Analysis':
            drawings.drawSentiments(sentiments)

        elif Analysis == 'Location Analysis':
            drawings.drawMostLocations(15,data)
            drawings.drawMap(data)

def getUserInfo():

    user = st.text_input("Enter Username: ")

    n_twts = st.number_input("How many tweets to Scrap : ",2)

    if user:
        userData = pd.read_csv(p.path2)
        
        if (userData.empty) or (userData['chk'][0]!=str(user)+str(n_twts)):
        
            userData = scrapUser.start(user, n_twts)
            userData = pd.read_csv(p.path2)

        usrAnalysis = st.selectbox('Select Analytics',
            ['Show Raw Data','Overall Sentiment of user'])  

        try:
            usrSentiments = pd.DataFrame(data = general.getSentiment(userData['text']),columns = ['neg','neu','pos','comp'])
        except:
            st.write('Unexpected Error Try Again...')
        uData = drawings.showUser(userData)

        if usrAnalysis == 'Show Raw Data':
            drawings.showUserData(uData)

        elif usrAnalysis == 'Overall Sentiment of user':
            drawings.drawUserSentiments(usrSentiments)
            drawings.drawUserWordCloud(uData)
    else:pass
        
    