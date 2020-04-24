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

# STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

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
