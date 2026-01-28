from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/") 
def index(): 
    return {"message": "Welcome to Sherlock API"}
