from fastapi import FastAPI
import uvicorn
import pandas as pd


df = pd.read_parquet('datasets/df_func_1.parquet')
df2 = pd.read_parquet('datasets/df_users_reviews_2.parquet')


app = FastAPI()

# @app.get("/")
# def root():
#     data = {"word": "Hello Wolrd"}
#     return data


@app.get("/userdata/")
def userdata(user_id:str):

    user = df[df['user_id'] == user_id]
    cantidad_items = user.item_id.count()
    # 
    dinero_gastado = user.price.sum()
    # 
    porcentaje_recomendacion = user.recommend.mean() * 100
    #
    res = {
        "cantidad items": cantidad_items.item(),
        "dinero gastado": f"{dinero_gastado:.2f}$",
        "porcentaje de recomendación": f"{porcentaje_recomendacion:.2f}%",
    }

    return res

# Función 2
@app.get('/countreviews/{start_date, end_date}')
def countreviews(start_date: str, end_date: str):
    # Filtrar las reviews por las fechas dadas
    reviews_filtradas = df2[(df2['date_posted'] >= start_date) & (df2['date_posted'] <= end_date)]

    # Contar la cantidad de usuarios que realizaron reviews
    cantidad_usuarios = reviews_filtradas['user_id'].nunique()

    # Calcular el porcentaje de recomendación
    porcentaje_recomendacion = reviews_filtradas['recommend'].mean() * 100

    # Devolver la cantidad de usuarios y el porcentaje de recomendación

    info = {
        "cantidad de usuarios": cantidad_usuarios,
        "porcentaje de recomendación": f"{porcentaje_recomendacion:.2f}%"
    }

    # return cantidad_usuarios, porcentaje_recomendacion
    return info


