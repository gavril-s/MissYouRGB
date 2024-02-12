from fastapi import FastAPI
import dotenv
import os
import uvicorn
import common

dotenv.load_dotenv()

host = os.environ.get("SERVER_HOST")
port = os.environ.get("SERVER_PORT")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Miss you"}


uvicorn.run(app, host=host, port=port, log_level="debug")
