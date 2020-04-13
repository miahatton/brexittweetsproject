from brexittweets.custom_funcs.sqlite_functions import size_of_database, get_data
from brexittweets.config import sqlite_db_path
import pandas as pd
import sqlite3

db = sqlite3.connect(sqlite_db_path)
cursor = db.cursor()

# Get length of the db
dbLength = size_of_database(cursor)
print('Updating usernames')
users = []

for index in range(1, dbLength + 1):
	# Overwrite username with number
	username = get_data('user', index, cursor)

	if username not in users:
		users.append(username)
	index_of_user = users.index(username)

	if index <10:
		print(f'Index: {index}; Username: {username}; Index of user: {index_of_user}')

	update_statement = f"UPDATE tweets SET user='twitter_user_{index_of_user}' WHERE id = {index};"
	cursor.execute(update_statement)
	db.commit()

# Check success

# Read back the first five rows of the database to test that the analysis worked.

test_ids = []
test_usernames = []

# Create a statement to run to test that the username values are now anonymised
test_statement = "SELECT id, user FROM tweets WHERE id<6;"
test_rows = cursor.execute(test_statement)

# Iterate through rows to save them to a dataframe
for row in test_rows:
	test_ids.append(row[0])
	test_usernames.append(row[1])

# Build and view dataframe.
df = pd.DataFrame(data={'id': test_ids, 'username': test_usernames})
print(df)

db.close()
