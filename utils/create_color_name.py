def create_color_name(df):
    df = df.copy()
    COLORS = {
        "3F7E00": "darkgreen", "5BA829": "green", "9ACD32": "lightgreen",
        "CDD614": "orange", "FFBA00": "red", "CBCBC8": "darkred", "FF7800": "darkred"
    }
    df["color_name"] = df["rating_color"].map(COLORS)
    return df
