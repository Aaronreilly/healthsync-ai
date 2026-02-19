"""
Main FastAPI application with Gemini and static frontend
File: backend/app/main.py
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

# Import our modules
from integrations.gemini_client import GeminiClient
from agents.nutrition_agent import NutritionAgent
from agents.exercise_agent import ExerciseAgent
from integrations.scaledown import ScaleDownEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize clients and agents
    print("🚀 Starting HealthSync AI with Gemini...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    
    app.state.gemini = GeminiClient(api_key=gemini_key)
    app.state.nutrition = NutritionAgent(app.state.gemini)
    app.state.exercise = ExerciseAgent(app.state.gemini)
    app.state.scaledown = ScaleDownEngine()
    
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(
    title="HealthSync AI with Gemini",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (our frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the main HTML page
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# API Endpoints
@app.get("/api/health")
async def health():
    return {
        "service": "HealthSync AI",
        "gemini": "connected" if hasattr(app.state, "gemini") else "not ready",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/nutrition/plan")
async def get_nutrition_plan(user_id: str = "user123", calorie_target: int = 2000):
    plan = await app.state.nutrition.generate_meal_plan(user_id, {"calorie_target": calorie_target})
    return plan

@app.post("/api/exercise/plan")
async def get_exercise_plan(user_id: str = "user123", fitness_level: str = "intermediate"):
    plan = await app.state.exercise.generate_workout_plan(user_id, fitness_level)
    return plan

@app.post("/api/sleep/advice")
async def get_sleep_advice(user_id: str = "user123", avg_hours: float = 7.0):
    sleep_data = {"avg_hours": avg_hours, "age": 30}
    advice = app.state.gemini.generate_sleep_advice(sleep_data)
    return {"user_id": user_id, "advice": advice}

@app.post("/api/compress")
async def compress_data(user_id: str = "user123"):
    # Create sample health data
    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    data = pd.DataFrame({
        "heart_rate": np.random.normal(70, 10, 365),
        "steps": np.random.randint(3000, 15000, 365),
        "sleep_hours": np.random.normal(7, 1.5, 365),
        "calories": np.random.randint(1800, 3000, 365)
    }, index=dates)
    result = app.state.scaledown.compress_health_history(user_id, data)
    return result

@app.post("/api/coach/message")
async def get_coach_message(context: str):
    message = app.state.gemini.generate_health_coach_message(context)
    return {"message": message}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)