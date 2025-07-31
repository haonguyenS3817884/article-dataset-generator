from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db_manager
from title_html_elements.router import router as title_html_elements_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup events
    print("Application startup: Initializing database connection...")
    try:
        await db_manager.client.admin.command("ping")
        print("Database is connected")
    except Exception as e:
        # If ping fails, bubble up so the server won’t start
        raise RuntimeError(f"MongoDB Exception: {e}") from e
    yield
    # Shutdown events
    print("Application shutdown: Closing database connection...")
    await db_manager.client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def index():
    return {"message": "Welcome to Article Dataset Generator"}

app.include_router(title_html_elements_router)