# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.flights import router as flights_router

app = FastAPI(
    title="Flights by Country API",
    description="API to get number of flights arriving at a specific airport by country.",
    version="1.0.0"
)

# Allow CORS for Streamlit frontend (assuming it's running on localhost:8501)
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the listed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flights_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)