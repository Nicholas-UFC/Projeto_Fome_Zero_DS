def adjust_cuisines(df):
    df = df.copy()
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)
    return df
