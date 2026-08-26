from fastapi import FastAPI
from Assign8.Ai_feature_specifications.models.ask import AskRequest

app=FastAPI()

@app.post("/ask")
def ask_question(req:AskRequest)
