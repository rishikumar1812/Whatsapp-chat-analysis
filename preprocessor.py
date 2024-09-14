import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    df = pd.DataFrame({'user-message': message, 'message_date': dates})
    
    # Function to parse date with multiple formats
    def parse_date(date_str):
        formats = ['%m/%d/%y, %H:%M', '%d/%m/%y, %H:%M']
        for fmt in formats:
            try:
                return pd.to_datetime(date_str.strip(' -'), format=fmt)
            except ValueError:
                continue
        return pd.NaT  # Return NaT if no format matches
    
    # Convert message_date using multiple formats
    df['message_date'] = df['message_date'].apply(parse_date)
    
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Separate users and messages
    users = []
    messages = []
    for message in df['user-message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user-message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1}")
        else:
            period.append(f"{hour}-{hour+1}")
    
    df['period'] = period
    
    return df
