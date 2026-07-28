# Valor de conversão tirado em 02/07/2026
EXCHANGE_RATES = {
    'Australia': 0.65,
    'Brazil': 0.18,
    'Canada': 0.73,
    'England': 1.27,
    'India': 0.012,
    'Indonesia': 0.000063,
    'New Zeland': 0.59,
    'Philippines': 0.017,
    'Qatar': 0.27,
    'Singapure': 0.74,
    'South Africa': 0.055,
    'Sri Lanka': 0.0033,
    'Turkey': 0.030,
    'United Arab Emirates': 0.27,
    'United States of America': 1.0
}

def convert_to_usd(df):
    
    df = df.copy()
    
    df['average_cost_for_two_cost_in_usd'] = df.apply(lambda row: row['average_cost_for_two'] * EXCHANGE_RATES.get(row['country'], 1), axis=1)
    
    return df
