import tweepy
import torch
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import time
import datetime as dt


df = pd.read_csv('sp500.csv') 
Security = df['Security']
sp500 = Security.tolist()




access_token = '1459884311570751489-Q1cd9lXgvjtN2lL0QGhIq5lnp4rpNs'
access_token_secret = 'r0kujVUVx2OMqTwHFkv8ffVg9Hh7Wu2hYV2XpkO7ZWIYu'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKLymwEAAAAAY23HfZVV9tjs0CpjusxN7nnBaMU%3DjDaMf4LXoOAxi6gBHHTw5UXtH8OnnJGQll5W0fKOixwukQtdYj'
api_key = 'LIuoEuH2BJzX9Tx5leBlbAfBG'
api_key_secret = 'qSlpS2lA71qxhsQZSLsdiQ0NyF5AZnovRj96aXTnMjXs2Z3zdX'


auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

#search_query = "(\$[A-Za-z]+|stocks|shares|finance|financial|opinion|analysis|earnings) (buy|sell|hold|long|short|bullish|bearish)"
keywords = ["finance", "stock market", "investing", "economy", "business", "earnings", "dividend", "losses", "profit", "financial results"]
query_template = "\"{} {}\" lang:en"  # Filter for English tweets only

# Define the list of tweet dictionaries
tweets = []

# Define the start and end times (in seconds since the epoch)
start_time = int(time.time())
end_time = start_time + 5 * 60 * 60  # 5 hours from start

# Define the batch size
batch_size = 10000

# Define the filename for the Parquet file
filename = 'tweets.parquet'

#time.sleep(600)
# Loop over companies
for company in sp500:
    # Define twitter search query items to 0
    counter = 0

    print(company)
    # Define the search query for this company
    #query = query_template.format(company, " OR ".join(keywords))
    query = company + ' AND finance'
    new_tweets = api.search_tweets( q=query, count=batch_size, tweet_mode='extended', lang="en")

    # Stop if there are no new tweets
    for tweet in new_tweets:
        counter += 1
    
    print(counter)
    if counter == 0:
            continue

    #Filter out non-finance related tweets
    new_tweets = [tweet._json for tweet in new_tweets if any(keyword in tweet.full_text.lower() for keyword in keywords)]
    # Add the new tweets to the list
    tweets.extend(new_tweets)

   
    # Convert the list of tweet dictionaries to a Pandas DataFrame
    df = pd.DataFrame(tweets)

    df = df[['created_at', 'full_text', 'retweet_count', 'favorite_count', 'user', 'entities', 'lang', 'id_str']]


        # Save the DataFrame to a Parquet file
    table = pa.Table.from_pandas(df)
    pq.write_table(table, filename)

    now = dt.datetime.now()
    print("Saved {} tweets to {} at {}".format(len(df), filename, now))

    time.sleep(40)