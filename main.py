from fastapi import FastAPI, HTTPException, Query
from typing import Dict, List
from database import tasks_db

app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact={
        "name": "Daniil Grinev"
    }
)

quadrant_types = ["Q1", "Q2", "Q3", "Q4"]


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Welcome!",
        "api_title": app.title,
        "api_description": app.description,
        "api_version": app.version,
        "api_contact": app.contact
    }


@app.get("/tasks")
async def get_tasks() -> dict:
    return {
        "count": len(tasks_db),
        "items": tasks_db
    }


@app.get("/tasks/stats")
async def get_tasks_stats() -> dict:
    total = len(tasks_db)

    by_quadrant: Dict[str, int] = {q: 0 for q in quadrant_types}
    completed_count = 0

    for task in tasks_db:
        q = task.get("quadrant")
        if q in by_quadrant:
            by_quadrant[q] += 1
        if bool(task.get("is_completed")):
            completed_count += 1

    by_status = {
        "completed": completed_count,
        "pending": total - completed_count
    }

    return {
        "total_tasks": total,
        "by_quadrant": by_quadrant,
        "by_status": by_status
    }


@app.get("/tasks/search")
async def search_tasks(q: str = Query(..., min_length=2)) -> dict:
    query = q.strip()

    results: List[dict] = [
        t for t in tasks_db
        if query.lower() in str(t.get("title", "")).lower()
        or query.lower() in str(t.get("description", "")).lower()
    ]

    return {
        "count": len(results),
        "tasks": results
    }


@app.get("/tasks/by-status/{status}")
async def get_tasks_by_status(status: str) -> dict:
    status_map = {"completed": True, "pending": False}
    if status not in status_map:
        raise HTTPException(
            status_code=404,
            detail="Статус не найден. Используйте: completed | pending")

    filtered = [t for t in tasks_db if bool(t.get("is_completed")) == status_map[status]]
    return {
        "status": status,
        "count": len(filtered),
        "tasks": filtered
    }


@app.get("/tasks/by-quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: str) -> dict:
    if quadrant not in quadrant_types:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4")

    filtered_tasks = [
        task
        for task in tasks_db
        if task["quadrant"] == quadrant
        ]

    return {
        "count": len(filtered_tasks),
        "items": filtered_tasks
    }


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int) -> dict:
    task = next((t for t in tasks_db if t.get("id") == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task
