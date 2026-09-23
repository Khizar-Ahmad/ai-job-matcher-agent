from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.ai_routes import router as ai_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.agents.graph import buildAgenticWorkflow
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = await AsyncConnection.connect(
        os.environ["checkpointers_db"],
         autocommit=True
    )

    checkpointer = AsyncPostgresSaver(conn)
    await checkpointer.setup()

    app.state.job_graph = await buildAgenticWorkflow(
        checkpointer
    )
    
    app.state.conn = conn

    yield

    await app.state.conn.close()

# app = FastAPI(
#     title="AI Job Application Agent"
# )
app = FastAPI(title="AI Job Application Agent",lifespan=lifespan)

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    "https://ai-job-matcher-by-khizarahmad.netlify.app/",
    "http://ai-job-matcher-by-khizarahmad.netlify.app/",
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