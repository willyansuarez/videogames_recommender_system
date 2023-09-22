from fastapi import FastAPI
import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException



app = FastAPI()
#--------------------------------------------
@app.get("/")
def index():
    return {"Mensaje" : "Hola Mundo"}
#--------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
@app.get("/userdata/")
async def userdata(user_id: str):
    
    df1 = pd.read_csv('df_func_1.parquet')
    user = df1[df1['user_id'] == user_id]

    cantidad_items = user.item_id.count()

    dinero_gastado = user.price.sum()

    porcentaje_recomendacion = user.recommend.mean() * 100

    res = {
        "cantidad items": cantidad_items,
        "dinero gastado": f"{dinero_gastado:.2f}$",
        "porcentaje de recomendación": f"{porcentaje_recomendacion:.2f}%",
    }

    return res

#-----------------------------------------------------------------------------------------------------------------

@app.get("/countreviews/")
async def countreviews(fecha_inicio: str, fecha_fin: str):
    
    df2 = pd.read_parquet('df_users_reviews_2.parquet')
    # Filtrar las reviews por las fechas dadas
    reviews_filtradas = df2[(df2['date_posted'] >= start_date) & (df2['date_posted'] <= end_date)]

    # Contar la cantidad de usuarios que realizaron reviews
    cantidad_usuarios = reviews_filtradas['user_id'].nunique()

    # Calcular el porcentaje de recomendación
    porcentaje_recomendacion = reviews_filtradas['recommend'].mean() * 100

    # Devolver la cantidad de usuarios y el porcentaje de recomendación

    info = {
        "cantidad de usuarios": cantidad_usuarios,
        "porcentaje de recomendación": porcentaje_recomendacion
    }

    return info
    

#-----------------------------------------------------------------------------------------------------------------

@app.get("/genre/")
async def genre(genero: str):
    
    df3 = pd.read_parquet('df_funcs_3_4.parquet')
    lista_gen = [
        'RPG', 'Sports', 'Simulation', 'Action', 'Strategy', 'Indie',
        'Casual', 'Utilities', 'Adventure', 'Racing', 'Education', 'Simulation',
    ]
    generos_suma = {}  # Diccionario para almacenar los géneros y sus sumas

    for g in lista_gen:
        x = df3[df3.genres.str.contains(g)]
        suma = x.playtime_forever.sum()
        generos_suma[g] = suma

    generos_ordenados = sorted(generos_suma.items(), key=lambda x: x[1], reverse=True)
    generos_ordenados_dict = dict(generos_ordenados)

    puesto = list(generos_ordenados_dict.keys()).index(genero) + 1

    return {"puesto": puesto}
    
#-----------------------------------------------------------------------------------------------------------------

@app.get("/userforgenre/")
async def userforgenre(genero: str):
    
    df4 = pd.read_parquet('df_funcs_3_4.parquet')
    # Filtrar el dataframe por el género especificado
    df_filtered = df4[df4['genres'].str.contains(genero, case=False, regex=False)]

    # Agrupar por usuario y calcular las horas totales de juego
    df_grouped = df_filtered.groupby(['user_id', 'user_url']).agg({'playtime_forever': 'sum'}).reset_index()

    # Ordenar por las horas totales de juego de forma descendente
    df_sorted = df_grouped.sort_values('playtime_forever', ascending=False)

    # Tomar los primeros 5 usuarios
    top_5_users = df_sorted.head(5)

    # Crear una lista de diccionarios con la información de cada usuario
    results = [{'user_id': row['user_id'], 'user_url': row['user_url'], 'playtime_forever': row['playtime_forever']} for _, row in top_5_users.iterrows()]

    # Retornar la lista de diccionarios resultante
    return results
    

#-----------------------------------------------------------------------------------------------------------------

@app.get("/developer/")
async def developer(developer: str):
    
    df5 = pd.read_parquet('df_steam_games_2.parquet')
    # Filtrar el dataframe por la empresa desarrolladora
    df_filtered = df5[df5['developer'] == desarrollador]

    # Calcular la cantidad de items gratuitos por año
    free_items_by_year = df_filtered[df_filtered['price'] == 0].groupby('year').size()

    # Calcular el total de items por año
    total_items_by_year = df_filtered.groupby('year').size()

    # Calcular el porcentaje de contenido gratuito por año
    free_percentage_by_year = (free_items_by_year / total_items_by_year) * 100

    # Reemplazar los valores NaN por 0
    free_percentage_by_year = free_percentage_by_year.fillna(0)

    # Crear el diccionario de resultados
    results = dict(zip(free_percentage_by_year.index, free_percentage_by_year.values))

    # Retornar el diccionario resultante
    return results
    

#-----------------------------------------------------------------------------------------------------------------

@app.get("/sentiment_analysis/")
async def sentiment_analysis(year: int):
    
    df6 = pd.read_parquet('df_func_6.parquet')
    # Filtrar el dataframe por el año de lanzamiento especificado
    df_filtered = df6[df6['year'] == anio]

    # Contar la cantidad de registros de reseñas por categoría de sentimiento
    sentiment_counts = df_filtered['sentiment'].value_counts().to_dict()

    # Retornar el diccionario con la cantidad de registros por categoría de sentimiento
    return sentiment_counts
    

#-----------------------------------------------------------------------------------------------------------------

@app.get('/recomendacion_juego/{id}')
def recomendacion_juego(game: str):
    df7 = pd.read_parquet('df_games.parquet')
    res = df7[df7["game"] == game]
    
    games = res.recommended.item()
    return {games}
    
    
