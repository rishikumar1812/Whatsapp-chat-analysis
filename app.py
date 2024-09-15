import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt
from io import StringIO
import seaborn as sns
st.title("WhatsApp Chat Analyzer")
st.subheader("Discover Insights from Your WhatsApp Chats Effortlessly")

    # Introduction text
st.write("""
    Welcome to the **WhatsApp Chat Analyzer**! 🎉
    This tool allows you to uncover interesting patterns and insights from your WhatsApp chat history. Whether you're curious about your most active day, most used emojis, or simply want to visualize the flow of conversations, you're in the right place!

    **Features:**
    - 📊 Total messages, words, and media shared
    - 🗓️ Busiest days and hours
    - 👥 Identify the most active user in group chats
    - ☁️ Generate word clouds of most common words and emojis
    - 📅 Heatmap of your chat activity throughout the week

    Ready to explore? Just upload your chat file, and let's get started! 🚀
    """)


st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()  # here it is stream of byte data now we are gone it into string data
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
     
    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        #stats area
        st.title("Top Statistics")
        num_messages,words,num_media_messages,links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
            
        with col2:
            st.header("Total Words")
            st.title(words)
            
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)
            
        with col4:
            st.header('Total links shared')
            st.title(links)
        
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #activity map
        st.title("Activity Map")
        col1, col2= st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax =plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 
        
        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig, ax =plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 
        
        st.title('Weekly activity map')
        user_heat_map=helper.activity_heat_map(selected_user,df)
        fig=plt.figure(figsize=(18,10))
        fig,ax= plt.subplots()
        ax=sns.heatmap(user_heat_map)
        st.pyplot(fig)
          
        #Finding the busiest user in the group(Group level)
        if (selected_user=='Overall'):
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_user(df)
            fig, ax= plt.subplots()
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe()
            
        #World cloud
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.title('Word Cloud')
        st.pyplot(fig)
        
        #Most common word
        st.title('Most Common Words')
        most_common_df=helper.most_common_words(selected_user, df)
        fig, ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # emoji analysis
        st.title('Emoji Analysis')
        emoji_df=helper.emojihelper(selected_user,df)
        col1, col2= st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
            
    