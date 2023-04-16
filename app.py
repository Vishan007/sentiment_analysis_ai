import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO
import preprocessing 
from utils import *

st.sidebar.title('Artifical Intelligence')
st.title('AI tweets analysis')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode()
    StringData = StringIO(data)    ##converting string data to dataframe
    df = preprocessing.preprocess(StringData)
    st.dataframe(df)

    ##fetch unique location
    unique_location = df['label'].unique().tolist()
    unique_location.sort()
    unique_location.insert(0,"Overall")
    selected_location = st.sidebar.selectbox('Show analysis wrt',unique_location)

    if st.sidebar.button('Show analysis'):

        num_of_tweets,num_of_words,num_of_negative,num_of_positive = fetch_stats(selected_location , df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header('Total tweets')
            st.title(num_of_tweets)

        with col2:
            st.header('Total words')
            st.title(num_of_words)

        with col3:
            st.header('Negative Sentiment')
            st.title(num_of_negative)

        with col4:
            st.header('Positive Sentiment')
            st.title(num_of_positive)

        ##finding the most tweets from location
        if selected_location == 'Overall':
            
            x , new_df = most_tweets_location(df)
            fig , ax = plt.subplots()
            col1 ,col2 = st.columns(2)

            with col1:
                st.title('Most tweets')
                ax.bar(x.index , x.values,color='green')
                st.pyplot(fig)

            with col2:
                st.title('Percent of tweets')
                st.dataframe(new_df[:6:])

        ## WordCloud
        st.title('Word Cloud')
        df_wc = create_wordcloud(selected_location,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        ##most common words
        common_words = most_common_words(selected_location,df)
        fig,ax = plt.subplots()
        ax.barh(common_words['words'],common_words['number of words'])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)
        


