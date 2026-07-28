def create_price_tye(df):
    df = df.copy()
    def get_price_cat(price_range):
        if price_range == 1: 
            return "cheap"
        elif price_range == 2: 
            return "normal"
        elif price_range == 3: 
            return "expensive"
        else: 
            return "gourmet"
    
    df["price_type"] = df["price_range"].apply(get_price_cat)
    return df
