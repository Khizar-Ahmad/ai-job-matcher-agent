from fastapi import FastAPI

from app.routes.auth_routes import router as auth_router
from app.routes.ai_routes import router as ai_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Job Application Agent"
)

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Next.js dev server
    "http://127.0.0.1:5173"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(ai_router)