import re
import pandas as pd

import string



def remove_punctuation(text):
    return text.translate(
        str.maketrans('', '', string.punctuation)
    )

def clean_user(x):
    x = str(x).replace('~', '')
    x = x.replace(',', '')
    x = x.replace('.', '')
    x = x.strip()
    if x == '':
        return 'NoName'
    return x

def clean_umessage(x):
    x = x.replace('~', ' ')
    x = x.replace(',', ' ')
    x = x.replace('.', ' ')
    x = x.replace(':', ' ')
    x = x.replace('•', ' ')
    x = x.strip()
    return x


def preprocess(data):
    
    pattern = r'\u200e?\[\d{1,2}/\d{1,2}/\d{2},\s\d{2}:\d{2}:\d{2}\]\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(r'\d{1,2}/\d{1,2}/\d{2},\s\d{2}:\d{2}:\d{2}',data)

    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'],format='%d/%m/%y, %H:%M:%S')
    df.rename(columns={'message_date':'date'},inplace=True)

    users = []
    messages = []

    for message in df['user_message']:

        if ': ' in message:
            user, msg = message.split(': ', 1)

            users.append(user)
            messages.append(msg)

        else:
            users.append('group_notification')
            messages.append(message)

    df['user'] = users
    df['message'] = messages
    
    df.drop(columns=['user_message'],inplace = True)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['user'] = df['user'].apply(clean_user)
    df['message'] = df['message'].apply(remove_punctuation)
    df['message'] = df['message'].apply(clean_umessage)

    period = []

    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    
    df['period']=period
    return df