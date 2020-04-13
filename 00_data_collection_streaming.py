import tweepy
import sqlite3
from brexittweets.custom_funcs.process_text_functions import preprocess_stream
from brexittweets.custom_funcs.sqlite_functions import create_table
from brexittweets.config import sqlite_db_path, api_key, api_secret, access_token, access_token_secret

# Create sqlite table

create_table()

# Set up Twitter authentication
auth_token = tweepy.OAuthHandler(api_key, api_secret)
auth_token.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_token)

# Connect to the database and create sqlite cursor

db = sqlite3.connect(sqlite_db_path)
dbCursor = db.cursor()

# Create a class inheriting from StreamListener


class MyStreamListener(tweepy.StreamListener):
	def __init__(self):
		super().__init__()

		# Create counter of tweets saved
		self.tweets_saved = 0

	def on_status(self, status):
		"""
		Apply filters, extract relevant data and store to database
		:param status:
		:return:
		"""

		# Check whether or not the tweet has been truncated. If so, get the full text.
		if status.truncated:
			tweet_text = status._json['extended_tweet']['full_text']
		else:
			tweet_text = status.text

		# Check that the status is in English
		if status.lang is not None and status.lang == "en":
			try:
				# we don't want to store retweets because they will become very repetitive
				type(status.retweeted_status)
			except AttributeError:
				# If not a retweet,
				# pre-process text to remove usernames, single quotation marks (to avoid SQL errors) and urls.
				preprocessed_text = preprocess_stream(tweet_text)
				#print(preprocessed_text)
				statement = """INSERT INTO tweets (id, date, user, text) 
				VALUES ({},'{}', '{}', '{}');""".format(
						status.id,
						status.created_at,
						status.user.screen_name,
						preprocessed_text
				)
				dbCursor.execute(statement)
				db.commit()

				self.tweets_saved += 1
				if self.tweets_saved % 10 == 0:
					print(preprocessed_text)
				if self.tweets_saved % 100 == 0:
					print(f"Tweets saved: {self.tweets_saved}")

		if self.tweets_saved >= 10:
			return False

	def on_error(self, status_code: int) -> bool:
		"""
		Stop the stream if a 420 status code is returned
		"""
		if status_code == 420:
			return False


# Create instance of Stream Listener

myStreamListener = MyStreamListener()

# Create a Stream object

myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Connect to the Twitter API using the Stream.

print('Starting stream')
myStream.filter(track=['brexit'])

db.close()
