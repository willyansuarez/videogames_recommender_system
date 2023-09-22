from fastapi import FastAPI
import uvicorn
import pandas as pd


df = pd.read_parquet('datasets/df_func_1.parquet')





app = FastAPI()

@app.get("/")
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


