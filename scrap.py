import pandas as pd 
import tweepy 

def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Username:{ith_tweet[0]}")
    print(f"Description:{ith_tweet[1]}")
    print(f"Location:{ith_tweet[2]}")
    print(f"Following Count:{ith_tweet[3]}")
    print(f"Follower Count:{ith_tweet[4]}")
    print(f"Total Tweets:{ith_tweet[5]}")
    print(f"Retweet Count:{ith_tweet[6]}")
    print(f"Tweet Text:{ith_tweet[7]}")
    print(f"Hashtags Used:{ith_tweet[8]}")
  
  
def scrape(words, date_since, numtweet,api):
      
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
          
        printtweetdata(i, ith_tweet)
        i = i+1
    filename = 'scraped_tweets.csv'
      
    # db.to_csv(filename)
    print('Scraping has completed!')
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
    
