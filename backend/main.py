from fastapi import FastAPI
from api.dog import router as dog_router
import os
import uvicorn

os.environ["MONGODB_URL"] = "mongodb://localhost:27017"


app = FastAPI()

app.include_router(dog_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
