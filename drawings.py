import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import general

def drawRawData(data):
    st.write('## Scrapped Raw Data',data)

def drawWordsPerTweet(cleanData):
    word_count = cleanData['text'].str.split().apply(len).value_counts()
    word_dict = dict(word_count)
    word_dict = dict(sorted(word_dict.items(), key=lambda kv: kv[1]))

    sns.distplot(word_count.values)
    plt.title('WORDS PER TWEET')
    plt.xlabel('Words Per Tweet')
    st.pyplot(plt)

    ind = np.arange(len(word_dict))
    fig0,ax0 = plt.subplots()
    
    ax0.bar(ind, list(word_dict.values()))

    # plt.xticks(ind, list(word_dict.keys()))
    plt.ylabel('Number of Tweets')
    plt.xlabel('Number of words in each Tweet')
    plt.title('WORDS PER TWEET')
    st.pyplot(fig0)

def drawMostRetweeted(mst,data):
    general.mostRetweeted(mst,data)

def drawSentiments(sentiments):
    fig3, axes = plt.subplots()
    sizes = [sentiments['comp'][sentiments['comp']>0].count(),sentiments['comp'][sentiments['comp']==0].count(),sentiments['comp'][sentiments['comp']<0].count()]
    plt.pie(sizes,labels=['Positive','Neutral','Negative'],autopct='%1.1f%%', shadow=True)
    st.pyplot(fig3)           
    
    fig1,ax = plt.subplots()
    ax.bar(['Positive','Negative'],[sentiments['comp'][sentiments['comp']>0].shape[0],sentiments['comp'][sentiments['comp']<0].shape[0]],color=['#668cff','#ff5050'])
    plt.title("NEGATIVE vs POSITIVE")
    st.pyplot(fig1)

    fig2, axes = plt.subplots(1, 2, figsize=(18, 10))
    plt.suptitle('Distribution Of Index Scores',fontsize='xx-large')
    sns.distplot(ax=axes[0], a=sentiments['pos'],color='b',axlabel = 'Positive Index').set_title('Positive')
    sns.distplot(ax=axes[1], a=sentiments['neg'],color='r',axlabel = 'Negative Index').set_title('Negative')
    st.pyplot(fig2)

def drawWordCloud(cleanData):
    postves = general.getTop(30,'pos',cleanData)
    general.showWordCloud(postves,'POSITIVE')
    negtves = general.getTop(30,'neg',cleanData)
    general.showWordCloud(negtves,'NEGATIVE')

def drawMap(data):
    st.subheader('MapWise Tweets')
    lat_long = general.getLatLong(data['location'])
    st.map(lat_long)

def drawMostLocations(most,data):
        st.subheader('LocationWise Tweets')
        location_grp=data.groupby(by=['location'])
        lob = location_grp['text'].count()
        lob_sorted = lob.sort_values(ascending=False)
        plt.rcdefaults()
        plt.style.use('fivethirtyeight')
        fig1 = plt.figure(figsize=(20,15))
        plt.barh(lob_sorted.index[:most],lob_sorted.values[:most])
        plt.title("Locationwise Number of tweets")
        st.pyplot(fig1)

st.cache(suppress_st_warning=True)
def showUser(data):
    name = data['username'][0]
    acc_cre_date = data['acc_cre_date'][0]
    foll = data['followers'][0]
    id = data['user_id'][0]
    st.markdown(f'Information for **{name}** and UserId : **{id}**')
    st.text(f'Account created at: {acc_cre_date} with current followers {foll}')

    return data[['created_at','text','tweet_id']]

st.cache(suppress_st_warning=True)
def showUserData(data):
    st.write(data)

st.cache(suppress_st_warning=True)
def drawUserSentiments(sentiments): 
    fig3, axes = plt.subplots()
    sizes = [sentiments['comp'][sentiments['comp']>0].count(),sentiments['comp'][sentiments['comp']==0].count(),sentiments['comp'][sentiments['comp']<0].count()]
    plt.pie(sizes,labels=['Positive','Neutral','Negative'],autopct='%1.1f%%', shadow=True)
    plt.title('Sentiment Pie Chart')
    st.pyplot(fig3)           
    
    fig1,ax = plt.subplots()
    ax.bar(['Positive','Negative'],[sentiments['comp'][sentiments['comp']>0].shape[0],sentiments['comp'][sentiments['comp']<0].shape[0]],color=['#668cff','#ff5050'])
    plt.title("NEGATIVE vs POSITIVE")
    plt.ylabel('# of Tweets')
    st.pyplot(fig1)

    fig2, axes = plt.subplots(1, 2, figsize=(18, 10))
    plt.suptitle('Distribution Of Index Scores',fontsize='xx-large')
    sns.distplot(ax=axes[0], a=sentiments['pos'],color='b',axlabel = 'Positive Index').set_title('Positive')
    sns.distplot(ax=axes[1], a=sentiments['neg'],color='r',axlabel = 'Negative Index').set_title('Negative')
    st.pyplot(fig2)

st.cache(suppress_st_warning=True)
def drawUserWordCloud(cleanData,col):
    postves = general.getTop(min(len(cleanData),30),col,cleanData)
    general.showWordCloud(postves,col)


