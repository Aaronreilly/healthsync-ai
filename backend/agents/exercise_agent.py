"""
Exercise Agent – powered by Gemini
File: backend/agents/exercise_agent.py
"""

from integrations.gemini_client import GeminiClient
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ExerciseAgent:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client
        logger.info("✅ Exercise Agent initialized with Gemini")

    async def generate_workout_plan(self, user_id: str, fitness_level: str = "intermediate") -> Dict:
        """Generate a weekly workout plan using Gemini."""
        user_profile = {
            "fitness_level": fitness_level,
            "equipment": "dumbbells, resistance bands",
            "goals": "build muscle and improve endurance",
            "time_per_session": 45
        }
        plan_text = self.gemini.generate_workout_plan(user_profile)
        return {
            "user_id": user_id,
            "week_start": "2025-02-13",
            "plan": plan_text,
            "source": "Gemini AI"
        }

    async def log_workout(self, user_id: str, workout_data: Dict) -> Dict:
        """Log a workout and get motivational feedback."""
        logger.info(f"User {user_id} logged workout: {workout_data}")
        feedback = self.gemini.generate_health_coach_message(
            f"I just completed a {workout_data.get('duration')} minute {workout_data.get('type')} workout."
        )
        return {
            "success": True,
            "message": "Workout logged",
            "feedback": feedback
        }

    async def get_weekly_summary(self, user_id: str) -> Dict:
        """Mock weekly summary."""
        return {
            "total_workouts": 4,
            "total_minutes": 180,
            "total_calories": 1500,
            "streak": 3
        }