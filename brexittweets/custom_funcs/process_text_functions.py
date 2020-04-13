import re
from gensim.utils import simple_preprocess
from gensim.parsing import preprocessing
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from typing import List, Tuple


def preprocess_stream(text: str) -> str:
	"""
	Remove usernames, links and punctuation that does not indicate sentiment from tweets
	"""
	# remove links
	text = re.sub("https?://\w+\.\w+(/\w*)*", '', text)
	# remove tagged usernames
	text = re.sub("[RT ]?@\w+:?", '', text)
	# remove single quotation marks, asterisks, fullstops and hashtags
	# Keeping !, ?, : etc because they can be associated with emotion.
	text = " ".join([re.sub("[#\.\*\']", "", word) for word in text.split(" ")])
	return text


def lower_case_chars_only(text: str) -> str:
	"""
	Remove punctuation, upper case letters, special characters,
	and any non-space whitespace character from Tweets.
	"""

	# replace all whitespace characters with a single space (ready for tokenization)
	# and lower case the whole text
	text = re.sub('\s', ' ', text).lower()

	# Remove '&amp;' which keeps cropping up
	text = re.sub('&amp;', '', text)

	# remove any character that is not a letter or space
	text = re.sub('[^a-z ]', '', text)

	return text


def preprocess_training_data(text: str) -> str:
	"""
	Perform the same preprocessing on training data as was performed on stream.
	Also remove punctuation and digits and convert to lower case for classification.
	"""
	return lower_case_chars_only(preprocess_stream(text))


def find_tag(tag: str):
	"""
	Converts string 'tag' to wordnet part-of-speech object (e.g. wordnet.ADJ for adjective)
	If the tag does not match any of j, n, v or r, function returns False and stem/lemmatize function skips
	lemmatization for this word
	:param tag: str (part-of-speech tag)
	:return: either wordnet pos object or 'False'
	"""
	if tag.startswith('J'):
		return wordnet.ADJ
	elif tag.startswith('N'):
		return wordnet.NOUN
	elif tag.startswith('V'):
		return wordnet.VERB
	elif tag.startswith('R'):
		return wordnet.ADV
	else:
		return False


def stem_lemmatize(tokens: List[Tuple[str]]) -> List[str]:
	"""
	Apply stemming and lemmatization to each text in a list of tuples where each tuple is (word, tag)
	return a list of lemmatized & stemmed words
	"""
	# Create empty list
	stemmed_lemmatized = []
	# Initialise SnowballStemmer and WordNetLemmatizer
	stemmer = SnowballStemmer('english')
	wnl = WordNetLemmatizer()
	
	for word, tag in tokens:
		# Identify the tag on the word
		word_tag = find_tag(tag)
		# If the function returns a POS, lemmatise AND stem
		if word_tag:
			stemmed_lemmatized.append(stemmer.stem(wnl.lemmatize(word, word_tag)))
		# If the function does not return a POS ('False'), stem
		else:
			stemmed_lemmatized.append(stemmer.stem(word))

	return stemmed_lemmatized


def tokenize_tag(text: str) -> List[Tuple[str]]:
	"""
	Accepts string, separates words from string and tags each word,
	returning a list of tuples where each tuple is (word, tag)
	"""
	tokenized_text = []
	tokens = simple_preprocess(text)
	for token in tokens:
		if token not in preprocessing.STOPWORDS and len(token) > 3:
			tokenized_text.append(token)
	tagged_tokens = pos_tag(tokenized_text)
	return tagged_tokens
