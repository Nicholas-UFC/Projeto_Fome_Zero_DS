def create_unique_restaurant_name(df):
    df = df.copy()
    
    # 1. Identifica os registros que possuem nomes duplicados
    # keep=False marca todas as ocorrências de nomes repetidos como True
    mask_duplicados = df.duplicated(subset=['restaurant_name'], keep=False)
    
    # 2. Inicializa 'unique_name' com o nome original
    df['unique_name'] = df['restaurant_name']
    
    # 3. Aplica a lógica apenas para as linhas onde mask_duplicados é True
    # Usamos .loc para garantir que estamos alterando apenas os duplicados
    df.loc[mask_duplicados, 'unique_name'] = (
        df['restaurant_name'] + 
        '-' + df['city'] + 
        '-' + df['country']
    )
    
    return df
