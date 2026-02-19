"""
Nutrition Agent – powered by Gemini
File: backend/agents/nutrition_agent.py
"""

from integrations.gemini_client import GeminiClient
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class NutritionAgent:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client
        logger.info("✅ Nutrition Agent initialized with Gemini")

    async def generate_meal_plan(self, user_id: str, goals: Dict[str, Any]) -> Dict:
        """Generate a meal plan using Gemini."""
        # In a real app, fetch user profile from database
        user_profile = {
            "age": 35,
            "weight": 70,
            "height": 170,
            "activity_level": "moderate",
            "preferences": "vegetarian",
            "calorie_target": goals.get("calorie_target", 2000)
        }
        meal_plan_text = self.gemini.generate_meal_plan(user_profile)
        return {
            "user_id": user_id,
            "date": "2025-02-13",
            "plan": meal_plan_text,
            "source": "Gemini AI"
        }

    async def track_meal(self, user_id: str, meal_data: Dict) -> Dict:
        """Log a meal and get feedback."""
        logger.info(f"User {user_id} tracked meal: {meal_data}")
        # Get quick AI feedback
        feedback = self.gemini.generate_health_coach_message(
            f"I just ate a {meal_data.get('name')} with {meal_data.get('calories')} calories."
        )
        return {
            "success": True,
            "message": "Meal logged",
            "feedback": feedback
        }

    async def get_daily_summary(self, user_id: str) -> Dict:
        """Return a summary (mock for now)."""
        return {
            "calories_consumed": 1650,
            "calories_remaining": 350,
            "protein": 95,
            "carbs": 180,
            "fats": 55
        }