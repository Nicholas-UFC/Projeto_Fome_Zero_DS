def clean_data(df):
    df = df.drop_duplicates(subset=['restaurant_id'], keep='first')
    df = df.dropna(subset=['restaurant_id'])
    
    return df
