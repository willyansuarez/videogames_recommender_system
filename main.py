from fastapi import FastAPI
import uvicorn
import pandas as pd


df = pd.read_parquet('datasets/df_func_1.parquet')



df7 = pd.read_parquet('datasets/df_games.parquet')

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



@app.get("/recommend_game/")
def recommend_game(game:str):
    res = df7[df7["game"] == game]
    games = res.recommended.item()
    return {games}
