from fastapi import FastAPI
from routers import tasks, stats

app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact={
        "name": "Daniil Grinev"
    },
    root_path="/api/v1"
)

app.include_router(tasks.router)
app.include_router(stats.router)


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Welcome!",
        "api_title": app.title,
        "api_description": app.description,
        "api_version": app.version,
        "api_contact": app.contact
    }
