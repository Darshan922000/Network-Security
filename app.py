import pandas as pd
import sys
import os
import certifi
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from uvicorn import run as app_run
from starlette.responses import RedirectResponse

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


from dotenv import load_dotenv
load_dotenv()
ca = certifi.where()
mongodb_url = os.getenv("MONGODB_URL")
print(mongodb_url)




from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
client = pymongo.MongoClient(mongodb_url)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url = "/docs") 

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training Is Successful")
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("./final_model/preprocessor.pkl")
        final_model = load_object("./final_model/model.pkl")
        network_model = NetworkModel(preprocessor= preprocessor, model= final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df["predicted_column"] = y_pred
        print(df["predicted_column"])
        #df["predicted_column"].replace(-1, 0)
        #return df.to_json()
        df.to_csv("Prediction Output/output.csv")
        table_html =  df.to_html(classes="table table-striped")
        print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)

'''if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)'''

    

