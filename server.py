from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from main import get_phishing_results 

app = FastAPI(title="Phishing Detection API")

class URLRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}


@app.post("/predict")
def predict_url(data: URLRequest):
    try:
        # Call your ML logic from main.py
        result = get_phishing_results(data.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
