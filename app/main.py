from fastapi import FastAPI
from api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:8080",  # frontend dev server
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not safe for production)
    allow_credentials=True,
    allow_methods=["*"],  # allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)
