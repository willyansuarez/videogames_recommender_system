from fastapi import FastAPI
import uvicorn
import pandas as pd


# df = pd.read_csv("/home/willian/modelo_recomendacion_peliculas/movies_recommendation/datasets/movies_processed.csv")
# df_2 = pd.read_parquet("/home/willian/modelo_recomendacion_peliculas/movies_recommendation/datasets/movies_with_recommendations.parquet")

df_func_1 = pd.read_parquet("datasets/df_func_1.parquet")
# df_2 = pd.read_parquet("./datasets/movies_with_recommendations.parquet")

app = FastAPI()

# @app.get("/")
# def root():
#     data = {"word": "Hello Wolrd"}
#     return data

@app.get('/userdata/{user_id}')
def userdata(user_id: str ):
    user = df_func_1[df_func_1['user_id'] == user_id]
    
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