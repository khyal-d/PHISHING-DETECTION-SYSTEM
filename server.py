from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from main import get_phishing_results 

app = FastAPI(title="Phishing Detection API")


# this is to Allow requests from anywhere (fine for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # i will restrict this  later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
