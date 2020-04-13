import sqlite3
from math import floor
from datetime import datetime
import pandas as pd
from brexittweets.config import sqlite_db_path, tweets_csv_path
from brexittweets.custom_funcs.process_text_functions import lower_case_chars_only
from brexittweets.custom_funcs.utils import positive_negative


def get_cursor():
	"""
	Connect to the database and return a cursor to use for sqlite functions
	:return: db, cursor: a database and cursor for executing sqlite commands
	"""
	db = sqlite3.connect(sqlite_db_path)
	return db, db.cursor()


def create_table():
	"""
	Create a database table in sqlite where tweets will be stored.
	:return: None
	"""
	db = sqlite3.connect(sqlite_db_path)
	cursor = db.cursor()

	statement_create = """CREATE TABLE tweets (
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
		date DATE NOT NULL,
		user TEXT NOT NULL,
		text TEXT NOT NULL,
		sentiment FLOAT,
		sentiment_tb FLOAT,
		tweets_preprocessed TEXT
	);"""

	cursor.execute(statement_create)
	db.commit()
	db.close()


def size_of_database(cursor) -> int:
	"""
	Fetch the number of rows of the tweets table
	:param cursor: an sqlite cursor
	:return num_rows: the number of rows in the table
	"""
	statement = f"""SELECT COUNT(*) FROM tweets;"""
	num_rows = cursor.execute(statement).fetchone()[0]
	return num_rows


def get_data(colname: str, row_number: int, cursor):
	"""
	Fetch the contents of a given field at a given index from the database
	:param colname: (str) the name of the field
	:param row_number: (int) the row number
	:param cursor: an sqlite cursor connected to the database
	:return contents: the contents of the field at the given index number (could be float, int or string)
	"""
	get_statement = f"SELECT ({colname}) FROM tweets WHERE id = {row_number};"
	contents = cursor.execute(get_statement).fetchone()[0]
	return contents


def create_dataframe_timeseries(slot=5) -> pd.DataFrame:
	"""
	Fetch tweet text, sentiment and datetime from database,
	separate the datetime object into components to aggregate
	into time slots, and return as a pandas dataframe.
	:param slot: time slots for aggregating time series data. Default is 5.
	:return df: A pandas DataFrame
	"""

	# Connect to the database

	db = sqlite3.connect(sqlite_db_path)
	cursor = db.cursor()

	# Create empty lists in which to store information from database

	ids = []
	datetimes = []
	sentiments = []
	sentiments_tb = []

	# Get data

	for tweet in cursor.execute("SELECT id, date, sentiment, sentiment_tb FROM tweets;").fetchall():
		# Add data from database to lists

		ids.append(tweet[0])
		# Convert time to datetime object
		converted_datetime = datetime.strptime(tweet[1], '%Y-%m-%d %H:%M:%S')
		datetimes.append(converted_datetime)
		sentiments.append(tweet[2])
		sentiments_tb.append(tweet[3])

	# Close the database

	db.close()

	# Create DataFrame from lists
	df_data = {
			'id': ids,
			'datetime': datetimes,
			'polarity': sentiments_tb
	}

	df = pd.DataFrame(data=df_data, index=ids)

	# Separate datetime column into components

	df['sentiment'] = df['polarity'].apply(positive_negative)
	df['year'] = df['datetime'].apply(lambda x: x.date().year)
	df['month'] = df['datetime'].apply(lambda x: x.date().month)
	df['day'] = df['datetime'].apply(lambda x: x.date().day)
	df['hour'] = df['datetime'].apply(lambda x: x.time().hour)

	# Create 5 minute slots
	df['minute'] = df['datetime'].apply(lambda x: floor(x.minute / slot) * slot)

	# Remove unnecessary column
	df.drop(columns=['datetime'], inplace=True)

	# Put components back together as datetime
	df['datetime_slot'] = pd.to_datetime(df.iloc[:, 3:].copy())

	# Drop rows with missing data as they are clearly errors
	df = df.dropna(axis=0, how='any')
	return df


def create_dataframe_lengths() -> pd.DataFrame:
	"""
	Fetch id, tweet text and sentiment from the database.
	Preprocess tweet text and calculate number of words ('length')
	Return DataFrame of id, length, sentiment, and pre-processed tweet.
	:return:
	"""

	# Connect to the database
	db = sqlite3.connect(sqlite_db_path)
	cursor = db.cursor()

	# Create empty lists in which to store information from database
	ids = []
	sentiments = []
	tweets = []

	# Get data
	for tweet in cursor.execute("SELECT id, tweet_preprocessed, sentiment_tb FROM tweets;").fetchall():
		# Add data from database to lists
		ids.append(tweet[0])
		tweets.append(tweet[1])
		sentiments.append(tweet[2])

	# Close the database
	db.close()

	# Preprocess text to remove unnecessary symbols and whitespace
	tweets_preprocessed = [lower_case_chars_only(tweet) for tweet in tweets]

	# Counting the words in the tweets

	lengths = []

	for tweet in tweets_preprocessed:
		# Reset counter
		count = 0
		# Split tweet by space
		words = tweet.split(' ')
		# Iterate through words and count ONLY if word has length >0
		# (This is to account for double spaces)
		for i in range(len(words)):
			if len(words[i]) > 0:
				count += 1
		lengths.append(count)

	# Create DataFrame from lists
	df_data = {
			'id': ids,
			'length': lengths,
			'sentiment': sentiments,
			'tweet_preprocessed': tweets_preprocessed
	}

	df = pd.DataFrame(data=df_data, index=ids)

	return df


def save_to_csv():
	"""
	Save the contents of the database table to a csv file.
	:return: None
	"""

	# Connect to the database
	db = sqlite3.connect(sqlite_db_path)
	cursor = db.cursor()

	# Find the number of rows in the database.
	size = size_of_database(cursor)

	tweet_text = []
	tweet_ids = []

	# Fetch the data and populate the lists
	for index in range(1, size):
		tweet = get_data('text', index, cursor)
		tweet_id = get_data('id', index, cursor)
		tweet_ids.append(tweet_id)
		# Preprocess the tweet
		tweet = lower_case_chars_only(tweet)
		tweet_text.append(tweet)

	# Convert the lists into a DataFrame
	tweets_for_lda = pd.DataFrame(data={'tweet_id': tweet_ids, 'tweet_text': tweet_text})

	# Save the DataFrame to csv
	tweets_for_lda.to_csv(tweets_csv_path, index=False)

	# Close the database
	db.close()


def check_sentiment_analysis(cursor, sentiment_classifier: str) -> pd.DataFrame:
	"""
	Pull a few rows of the database to see how the first few Tweets were classified in sentiment analysis
	:param cursor: a database cursor
	:param sentiment_classifier: type of sentiment classifier used.
	:return df: A DataFrame
	"""
	test_ids = []
	test_tweets = []
	test_sentiments = []

	# Create a statement to run to test that the sentiment values have been saved to the database.
	if sentiment_classifier == 'tb':
		test_statement = 'SELECT id, text, sentiment_tb FROM tweets WHERE id<6;'
	elif sentiment_classifier == 'custom':
		test_statement = 'SELECT id, text, sentiment FROM tweets WHERE id<6;'
	else:
		print("Sentiment_classifier must be one of 'tb' or 'custom'")
		return None
	test_rows = cursor.execute(test_statement)

	# Iterate through rows to save them to a dataframe
	for row in test_rows:
		test_ids.append(row[0])
		test_tweets.append(row[1])
		test_sentiments.append(row[2])

	# Build and view dataframe.
	df = pd.DataFrame(data={'id'                : test_ids,
							'text'              : test_tweets,
							'sentiment_TextBlob': test_sentiments})
	return df