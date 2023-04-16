import re
import pandas as pd
from wordcloud import WordCloud ,STOPWORDS
from collections import Counter

f = open('stopwords.txt','r')
stop_words = f.read()
stop_words = [word for word in stop_words.split('\n')]


def remove_space(text):
    text = text.strip()
    return text

def remove_url(text):
    """
    remove urls from the tweets
    """
    return re.sub(r"https?://\S+|www\.\S+", " ", text)


def remove_html(text):
    """
    remove html tag from the tweets
    """
    html = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    return re.sub(html, "", text)

def remove_non_asci(text):
    """
    remove non asci chracters from the tweets
    """
    return re.sub(r'[^\x00-\x7f]',r' ', text)

def remove_special_characters(text):
    """
        Remove special special characters, including symbols, emojis, and other graphic characters
    """
    emoji_pattern = re.compile(
        '['
        u'\U0001F600-\U0001F64F'  # emoticons
        u'\U0001F300-\U0001F5FF'  # symbols & pictographs
        u'\U0001F680-\U0001F6FF'  # transport & map symbols
        u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
        u'\U00002702-\U000027B0'
        u'\U000024C2-\U0001F251'
        ']+',
        flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_pun(text):
    """
     Remove the punctuation
    """
    return re.sub(r'[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+', " ", text)

def fetch_stats(selected_location , df):

    if selected_location != 'Overall':
        df =  df[df['label'] == selected_location]
    #1. fetch num of messages
    num_tweets = df.shape[0]
    #2 num of words
    words = []
    for message in df['tweets']:
        words.extend(message.split())

    ##3 fetch number of users
    #num_of_users  = df['username'].unique().shape[0]
    #num_of_location = df['location'].unique().shape[0]
    try:
        num_of_negative = df['label'].value_counts().values[0]
        num_of_positive = df['label'].value_counts().values[1]

    except IndexError:
        num_of_negative = df[df['label']=='NEGATIVE'].shape[0]
        num_of_positive = df[df['label']=='POSITIVE'].shape[0]

    return num_tweets , len(words) , num_of_negative,num_of_positive

def most_tweets_location(df):
    x = df['location'].value_counts().head()
    df = round((df['location'].value_counts()/df.shape[0]) *100,2).reset_index().rename(columns={'index':'place','location':'percent'})
    return x , df

def create_wordcloud(selected_location , df):
    if selected_location != 'Overall':
        df =  df[df['label'] == selected_location]
    
    def remove_stop_words(tweet):
        
        y = []
        for word in tweet.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
    temp_df = df['tweets'].apply(remove_stop_words)
    wc = WordCloud(width=500,height=500,min_font_size=10 ,background_color='white')
    df_wc = wc.generate(temp_df.str.cat(sep=' '))
    return df_wc


def most_common_words(selected_location,df):
    
    if selected_location != 'Overall':
        df =  df[df['label'] == selected_location]

    removed = []
    for message in df['tweets']:
        for word in message.lower().split():
            if word not in stop_words:
                removed.append(word)
    
    common_words_df = pd.DataFrame(Counter(removed).most_common(20),columns=['words' , 'number of words'])
    return common_words_df

