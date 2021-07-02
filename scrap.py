import pandas as pd 
import tweepy 
import streamlit as st
import path as p

@st.cache(suppress_st_warning=True)  
def scrape(words, date_since, numtweet,api):

    msg = st.text(f'Scraping Tweets for {words}')
    prog = st.progress(0)
      
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])
      
    tweets = tweepy.Cursor(api.search, q=words, lang="en",
                           since=date_since, tweet_mode='extended').items(numtweet)
     
    list_tweets = [tweet for tweet in tweets]
      
    i = 1  
      
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
          
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
          
        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet
          
        i = i+1
        prog.progress(i/(len(list_tweets)+2))
    filename = p.path3
      
    # db.to_csv(filename)
    print('Scraping has completed!')
    msg.empty()
    prog.empty()
    return db
  
  
def start(tag,date_since,numtweets):
    consumer_key = 'XBOMTUDVy5b0zOdWqRWYJuGkw'
    consumer_secret = 'oYK2W4jiARg3NQSFBklWwXgg9vhz1raviEd6OiFsZ7UsAAia17'
    access_key = '2572669031-n1HzM9bPb00wp4ZSuHWBsd7Wn9AEEShg2Z5z8eg'
    access_secret = 'J40ArmKsrPj4w5xgst4pq32ycOECM2cNy2OQ1Fd9I4zKI'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    # api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api = tweepy.API(auth)
      
    # print("Enter Twitter HashTag to search for")
    # tag = input()
    # print("Enter Date since The Tweets are required in yyyy-mm--dd")
    # date_since = input()
    # numtweet = 10

    return scrape(tag, date_since, numtweets,api)


if __name__ == '__main__':

    print("Enter Twitter HashTag to search for")
    tag = input()
    print("Enter Date since The Tweets are required in yyyy-mm--dd")
    date_since = input()
    numtweet = 10

    start(tag,date_since,numtweet)
    

