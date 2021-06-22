from fastapi import FastAPI, File, UploadFile, HTTPException
from aiofiles import open
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import util,models


app = FastAPI(title=" API Vine fungal disease",
    description="Data Pipeline using jenkins + mlflow + Google cloud build + kubernetes + fastapi + github + python + linux \o/ :)",
    version="1.0.1",
)

model = load_model('model')

labels = ['negativo', 'positivo']

@app.post("/uploadfile/", tags=["model"])
async def create_upload_file(new_file: UploadFile = File(...)):
    file_name = "images/" + new_file.filename
    up_file = await new_file.read()
    
    if new_file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Please upload only .jpeg and .png files")
    async with open(f"{file_name}", "wb") as f:
        await f.write(up_file)
    img =util.preprocess_image(file_name,32)
    predict =model.predict(img)
    new_pred=models.Prediction(class_name=labels[int(np.round(predict))],class_prob=str(predict))
    return new_pred 