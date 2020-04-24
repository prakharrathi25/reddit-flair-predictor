import pickle
import praw
import re
import sklearn
import ast
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# To avoid redownloading or tedious searching for nltk corpus
# I have just stored them in a separte file as a list.

with open('stopwords.txt', 'r') as f:
    STOPWORDS = ast.literal_eval(f.read())

# Get reddit data
# Credentials generated from the reddit developers applications page
my_client_id = '8KS6G6Nt9BU9sg'
my_client_secret = 'CkeVFda-vf0DbseDb0eEr1YMpJo'
user = 'reddit_scrape'

reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=user)

# Data Cleaning tools
REPLACE_SPACES = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS = re.compile('[^0-9a-z #+_]')

def clean_text(text):

    text = text.lower() # lowercase text
    text = REPLACE_SPACES.sub(' ', text)
    text = BAD_SYMBOLS.sub('', text) # Replace Bad Symbols which
    text = text.replace('x', '')

    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwords from text
    return text

# Predict for a single entry ( This includes comments so far)
def get_flair(url, loaded_model):

    # Collect the data from that URL
    submission = reddit.submission(url=url)
    reddit_entry = {}

    reddit_entry['Title'] = submission.title
    reddit_entry['URl'] = submission.url

    submission.comments.replace_more(limit=0)
    comment = ''
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body

    reddit_entry["comment"] = comment
    reddit_entry['combine'] = reddit_entry['Title'] + reddit_entry['comment']
    reddit_entry['combine'] = clean_text(reddit_entry['combine'])

    # Need to convert it into a count Vectorizer object

    # # Creating an instance of the count vectorizer
    # count_vec = CountVectorizer()
    # data_counts = count_vec.transform([reddit_entry['Title']])

    return loaded_model.predict([reddit_entry['combine']])
