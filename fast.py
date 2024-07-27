from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from speech21 import speech
from genai2 import *
from fastapi.middleware.cors import CORSMiddleware

import os


class Input(BaseModel):
    input: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allows requests from your Angular app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
@app.post("/")
async def get_customer(input_data: Input):
    try:
        result = speech(input_data.input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


