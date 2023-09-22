from fastapi import FastAPI
import uvicorn
import pandas as pd



app = FastAPI()

@app.get("/")
def root():
    data = {"word": "Hello Wolrd"}
    return data
