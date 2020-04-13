# Brexit Tweets Project
(ST20166622 CIS4015 WRIT1)

## Project description

This project aims to stream Tweets from [Twitter](https://twitter.com), save them to an SQLite database, and perform several analysis 
tasks on the Tweets:

- Sentiment analysis
- Visualisation of sentiment against time and as a histogram
- Investigating the relationship between Tweet length (word count) and sentiment
- Topic modelling using LDA (Latent Dirichlet Allocation)
 
The processes and results are stored in this folder (`brexittweetsproject') as the following scripts and notebooks:

This project forms the WRIT1 assessment of module 'CIS4015 Fundamentals of Data Science' at 
Cardiff Metropolitan University.  

### 00_data_collection_streaming.py

Creates SQlite database and collects Tweet data using [TweePy](https://www.tweepy.org/) via 
the [Twitter Streaming API](https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter)

Please note: API keys have been replaced with jumbled strings, so to run this script you will need to provide a key 
via `brexittweetsproject/brexittweets/config.py`

### 01_sentiment_analysis_custom.ipynb

A Naive-Bayes classifier is built to apply sentiment analysis to the Tweets in the SQLite database.

### 02_sentiment_analysis_textblob.ipynb

Sentiment analysis is repeated using TextBlob, because this API provides a continuous value for sentiment that can be 
used for data analysis and visualisation in following notebooks.

### 03_data_visualisation.ipynb

Sentiment data from [Textblob](https://textblob.readthedocs.io/) is visualised. Outputs are stored in the 
`plots` folder.

### 04_data_exploration.ipynb

The sentiment data is examined in preparation for analysis in notebook 5.

### 05_relationship_length_sentiment.ipynb

The relationship between length of Tweet (word count) and sentiment is examined using a linear regression model.

### 06_topic_modelling.ipynb

Latent Dirichlet Allocation (LDA) is applied to identify three topics within the data.

### data_anonymisation.py

In accordance with GDPR (ICO, 2017), usernames are replaced with numbers. Although Tweets on streaming are public, users may 
later delete their Tweets, which we can assume is a retraction. To protect the identities of users in these 
circumstances, all usernames (which can be used to personally identify subjects) are removed.

## Configuration

To run the scripts and notebooks, first check that the path saved in `brexittweetsproject.config` 
points to the `brexittweetsproject` directory.

To check, uncomment the line:  
`# print(path)`  
from the script `brexittweetsproject/brexittweets/config.py` and run the script.

You can add a custom path within `config.py` to override the given path.

To run `00_data_collection_streaming.py`, you must also add your own `api_key`, `api_secret`, `access_token` and 
`access_token_secret` to the `config.py` script.

### Dependencies

This project was developed in [PyCharm](https://www.jetbrains.com/pycharm/) using an Anaconda virtual environment.

As well as Python 3.7, the project utilises the following packages:

package | version
--- | ---
pandas | 1.0.1
sqlite3 | 3.31.1
tweePy | 3.8.0
numPy | 1.18.1
sklearn | 0.22.2
nltk | 3.4.5
gensim | 3.8.0
wordcloud | 1.0.0
textblob | 0.15.3
matplotlib | 3.1.3
jupyter | 1.0.0
jupyter client | 6.0.0
jupyter console | 6.1.0
jupyter core | 4.6.1

## Contents

In addition to the notebooks and scripts as described above, the project contains the following directories:

### brexittweets

Contains `config.py` script described above (see: Configuration), and [Google Font](https://fonts.google.com/), 
`Roboto-Medium.tff`, used to generate word clouds in Notebook 06.

Also contains `custom-funcs` subdirectory.

### brexittweets/custom-funcs

Holds functions organised into separate scripts to use throughout notebooks.

- `process_text_functions.py` - functions used in text pre-processing tasks
- `sqlite_functions.py` - functions used to interact with SQLite database
- `utils.py` - all other functions

### data

- `training-dataset.csv` - The Sentiment-140 dataset (Go, Bhayani, Huang, 2009) obtained from Kaggle, used to train 
Naive Bayes classifer in Notebook 01.
- `tweet_lengths_df.pkl` - A pickle object used to store data in Notebook 04 for use in Notebook 05.
- `tweets-for-lda.csv` - A CSV of tweet texts used for LDA in Notebook 06.
- Sqlite subdirectory containing `sqlite3.exe` and Tweet database.(`twitter-stream.db`)

### plots

Contains outputs from Notebooks 03 and 05, as well as subdirectory `word_clouds` containing outputs of Notebook 06.

## Bibliography

Information Commissioner’s Office (ICO) (2017) ’Guide To The General Data Protection Regulation (GDPR)’. [online] 
Ico.org.uk. Available at: 
[https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
[Accessed 21 March 2020].

Go, A., Bhayani, R. and Huang, L., 2009. 'Twitter sentiment classification using distant supervision'. 
*CS224N Project Report*, Stanford, 1(2009), p.12.

TextBlob, 2020 'Textblob: Simplified Text Processing' *Textblob 0.15.2 Documentation*, [online] 
available at [https://textblob.readthedocs.io/](https://textblob.readthedocs.io/). [Accessed 30 March 2020]

BBC News (2019a) 'General Election 2019: A really simple guide', available at
[https://www.bbc.co.uk/news/uk-politics-49826655](https://www.bbc.co.uk/news/uk-politics-49826655)
[accessed 16/03/20]

BBC News (2019b) 'General election 2019: Boris Johnson vows to 'forge a new Britain'', available at
[https://www.bbc.co.uk/news/election-2019-50532000](https://www.bbc.co.uk/news/election-2019-50532000)
[accessed 16/03/20]

BBC News (2020a) 'Brexit: NI deadline is 'almost impossible' to meet', available at 
[https://www.bbc.co.uk/news/uk-northern-ireland-51093782](https://www.bbc.co.uk/news/uk-northern-ireland-51093782)
[accessed 16/03/20]

BBC News (2020b) 'New blue British passport rollout to begin in March', 
available at [https://www.bbc.co.uk/news/uk-51585018](https://www.bbc.co.uk/news/uk-51585018) 
[accessed 16/03/20]

Prabhakaran, s. (2018) 'Topic Modeling with Gensim (Python)', *Machine Learning Plus* [online] available at
[https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/](https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/)
[accessed 09/03/2020]

The Guardian (2020) 'Brexit: EU and US trade deals 'at risk' if UK reneges on Northern Ireland pledges', available at
[https://www.theguardian.com/politics/2020/feb/23/brexit-uk-reneging-on-northern-ireland-pledges-risks-trade-deals-with-us-and-eu](https://www.theguardian.com/politics/2020/feb/23/brexit-uk-reneging-on-northern-ireland-pledges-risks-trade-deals-with-us-and-eu)
[accessed 16/03/20]

BrexitBot (2020) 'Hi, just a reminder that Brexit has not happened yet. It is due to occur on the 29th March 2019',
Twitter [online] available at 
[https://twitter.com/hasnthappened/with_replies](https://twitter.com/hasnthappened/with_replies) [accessed 10/04/2020] 
