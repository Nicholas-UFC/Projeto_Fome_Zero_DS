import inflection

def rename_columns(dataframe):
    df = dataframe.copy()
    
    # Substituindo as lambdas por funções def conforme a recomendação
    def title(x): 
        return inflection.titleize(x)
    
    def snakecase(x): 
        return inflection.underscore(x)
    
    def spaces(x): 
        return x.replace(" ", "")
    
    # Aplicação das funções
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    
    df.columns = cols_new
    return df
