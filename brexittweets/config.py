# Set path of project
from pathlib import Path
import re

# gets current working directory replacing \ with / to avoid escapes - may need to change for other OS than windows.
path = re.sub(r'\\',r'/',str(Path(__file__).absolute()))
# Resets wd to top of directory tree
path = re.sub(r'/brexittweets/config.py',r'', path)

# Uncomment below and run script to check that 'path' points to the directory 'brexittweetsproject'
# print(path)

# Uncomment below and add your own path if needed
# path = 'C:/Users/UserName/PycharmProjects/brexittweetsproject'

# All other paths

sqlite_db_path = path + '/data/sqlite/twitter-stream.db'
tweets_csv_path = path + '/data/tweets-for-lda.csv'
training_data_path = path + '/data/training-dataset.csv'
plots_output_path = path + '/plots/'

# Other variables

# Insert your Twitter Developer credentials here
api_key = "xxxxxxxxxx"
api_secret = "xxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxx-xxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxx"

# Colour for plot outputs
twitter_blue = '#1DA1F2'
