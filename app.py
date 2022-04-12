import streamlit as st
import pandas as pd
import numpy as np
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("ANALYSIS WITH RESPECT TO: ",user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3= st.columns(3)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
      
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
       

            
        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                sns.barplot(x.index, x.values,palette = 'gist_earth')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
         # WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        #  most common words
        
        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        sns.barplot(most_common_df[1],most_common_df[0])
        plt.xticks(rotation=45)

        st.title('Most commmon words')
        st.pyplot(fig)
        
        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct = '%.2f%%',shadow=True,startangle=90,colors = plt.cm.BuPu(np.linspace(0, 1, 7)))
            st.pyplot(fig)
            
        
        
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            sns.barplot(busy_day.index,busy_day.values,palette='rocket_r',)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            sns.barplot(busy_month.index, busy_month.values,palette = 'magma')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap="YlGnBu")
        st.pyplot(fig)
        
        
        
