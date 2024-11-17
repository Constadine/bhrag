from create_dataset import create_dataset
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import json
import requests
import numpy as np
from instructor_outfit_classifier import generate_concept_weights
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_top_n_similar(row, n=3) -> pd.DataFrame:
    sims = cosine_similarity([row], df.iloc[:, -98:]).flatten()
    idx = np.argsort(sims)[-n:]

    return pd.DataFrame({'similar_perfume': df.iloc[idx, 0], 'similarity': sims[idx]})

app = FastAPI()
df = create_dataset()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/similarity")
async def get_similarity(outfit_url: str):

    concept_weights = generate_concept_weights(outfit_url)

    top_three = get_top_n_similar(concept_weights, n=3)
    data = {
        "bestthree": list(top_three['similar_perfume'])
    }
    return JSONResponse(content=data, media_type="application/json")
