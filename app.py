import streamlit as st
import preprosessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Ano')
st.sidebar.write('The Whatapp chat Analyzer!')


uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprosessor.preprocess(data)



    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)
    show_data = st.sidebar.button('Show Data')
    show_Analysis = st.sidebar.button('Show Analysis')
    if show_data:
        st.title('Data of Messages:')
        st.dataframe(df, use_container_width=True)

    if show_Analysis:
        # Finding stats.
        st.title('Top Statistics:')
        num_msg , num_words , num_media , num_link= helper.fetch_stats(selected_user,df)

        col1 ,col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total messages')
            st.title(num_msg)
        with col2:
            st.header('Total words')
            st.title(num_words)
        with col3:
            st.header('Media shared')
            st.title(num_media)
        with col4:
            st.header('Links shared')
            st.title(num_link)

        # Timeline
        # 1.monthly:
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='#A78295')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # 2. daily:
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#A78295')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#891652')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding busiest users in the group.
        if selected_user == 'Overall':
            st.title('Most busy users')
            x , new_df= helper.fetch_busy_users(df)
            fig, ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                plt.bar(x.index, x.values, color = '#891652')
                plt.xticks(rotation='vertical')  # or rotation=90
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


            # most common words
            most_common_df = helper.most_common_words(selected_user,df)
            st.title('Most Common Words')

            col1 , col2 = st.columns(2)
            with col1:
                st.dataframe(most_common_df)
            with col2:
                plt.figure(figsize=(14,7))
                fig , ax = plt.subplots()
                plt.barh(most_common_df[0],most_common_df[1], color = '#8EAC50')
                # plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # emoji analysis
            st.title('Emoji Analysis')
            emoji_df = helper.emoji_counter(selected_user,df)
            col1 , col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig , ax = plt.subplots()
                if emoji_df.shape[0] < 10:
                    plt.pie(emoji_df[1], labels=emoji_df[0], autopct='%0.2f')
                else:
                    plt.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct='%0.2f')
                st.pyplot(fig)



