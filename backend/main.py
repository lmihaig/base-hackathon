from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.dog import router as dog_router
import os
import uvicorn

os.environ["MONGODB_URL"] = "mongodb://localhost:27017"


origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dog_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
