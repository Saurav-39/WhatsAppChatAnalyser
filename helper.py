
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
from matplotlib import font_manager
from urlextract import URLExtract
extractor = URLExtract()

def remove_ommitted(message):
    t1 = []

    for word in message.split():

        if word.lower() not in ['image omitted','video omitted', 'omitted']:
            t1.append(word)

    return " ".join(t1)



def fetch_stats(selected_user , df):
   
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    # 1. fetch number of messages
    num_messages =  df.shape[0]
    # 2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    # 3. Number of media message

    num_media_message = df[df['message'].str.contains('omitted')].shape[0]

    # 4. Fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return num_messages,len(words),num_media_message,len(links)
    

def most_busy_users(df):
    x = df[df['user'] != 'group_notification']['user'].value_counts().head()
    df2 = round((df[df['user'] != 'group_notification']['user'].value_counts()/df[df['user'] != 'group_notification'].shape[0])*100,2).reset_index().rename(columns={'count':'percent'})
    return x,df2;

def create_wordcloud(selected_user,df):

    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    df['message'] =  df['message'].apply(remove_ommitted)

    wc = WordCloud(width = 500 , height = 500 , min_font_size = 10 , background_color = 'white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp['message'] = temp['message'].apply(remove_ommitted)
    temp = temp[temp['message']!='']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_helper(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    user_activity_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_activity_heatmap