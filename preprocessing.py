import pandas as pd
from utils import *

def preprocess(dataset):
    df = pd.read_csv(dataset , usecols = ['date','username','location','tweets','label','score'] ,sep=',')
    df['location'] = df['location'].fillna('missing')
    df['username']=df['username'].apply(lambda x : x.lower())
    df['location']=df['location'].apply(lambda x : x.lower())
    df['tweets']=df['tweets'].apply(lambda x : x.lower())
    df['tweets'] = df['tweets'].apply(lambda x : remove_space(x))
    df['tweets'] = df['tweets'].apply(lambda x : remove_url(x))
    df['tweets'] = df['tweets'].apply(lambda x : remove_html(x))
    df['tweets']=df['tweets'].apply(lambda x : remove_non_asci(x))
    df['tweets'] = df['tweets'].apply(lambda x : remove_special_characters(x))
    df['tweets'] = df['tweets'].apply(lambda x : remove_pun(x))
    df['tweets'] = df['tweets'].fillna('Neutral')
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['min'] = df['date'].dt.minute
    df['month'] = df['date'].dt.month_name()

    return df