COUNTRIES = {
    1: "India", 14: "Australia", 30: "Brazil", 37: "Canada",
    94: "Indonesia", 148: "New Zeland", 162: "Philippines",
    166: "Qatar", 184: "Singapure", 189: "South Africa",
    191: "Sri Lanka", 208: "Turkey", 214: "United Arab Emirates",
    215: "England", 216: "United States of America"
}

def add_country_name(df):
    df = df.copy()
    df["country"] = df["country_code"].map(COUNTRIES)
    return df
