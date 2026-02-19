"""
Gemini AI Client
File: backend/integrations/gemini_client.py
"""

import google.generativeai as genai
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    """Wrapper for Google's Gemini API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        logger.info("✅ Gemini client initialized")

    def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Send a prompt to Gemini and return the response text."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return f"Error: {e}"

    def generate_meal_plan(self, user_data: Dict[str, Any]) -> str:
        """Generate a personalized meal plan based on user data."""
        prompt = f"""
        Create a healthy one-day meal plan for a person with the following profile:
        - Age: {user_data.get('age', 'unknown')}
        - Weight: {user_data.get('weight', 'unknown')} kg
        - Height: {user_data.get('height', 'unknown')} cm
        - Activity level: {user_data.get('activity_level', 'moderate')}
        - Dietary preferences: {user_data.get('preferences', 'none')}
        - Daily calorie target: {user_data.get('calorie_target', 2000)} kcal

        Provide breakfast, lunch, dinner, and two snacks with approximate calories and macros.
        Keep the response friendly and encouraging.
        """
        return self.generate_response(prompt)

    def generate_workout_plan(self, user_data: Dict[str, Any]) -> str:
        """Generate a weekly workout plan."""
        prompt = f"""
        Create a weekly workout schedule for a person with:
        - Fitness level: {user_data.get('fitness_level', 'beginner')}
        - Available equipment: {user_data.get('equipment', 'none')}
        - Goals: {user_data.get('goals', 'general fitness')}
        - Time per session: {user_data.get('time_per_session', 30)} minutes

        Provide exercises for each day, include warm-up and cool-down tips.
        """
        return self.generate_response(prompt)

    def generate_sleep_advice(self, sleep_data: Dict[str, Any]) -> str:
        """Provide personalized sleep improvement tips."""
        prompt = f"""
        Based on the following sleep data, give 3-5 actionable tips to improve sleep quality:
        - Average sleep duration: {sleep_data.get('avg_hours', 7)} hours
        - Sleep latency: {sleep_data.get('latency', 15)} minutes
        - Wake ups: {sleep_data.get('wake_ups', 1)} per night
        - Sleep consistency: {sleep_data.get('consistency', 'moderate')}
        - User's age: {sleep_data.get('age', 30)}

        Keep advice practical and evidence-based.
        """
        return self.generate_response(prompt)

    def generate_health_coach_message(self, context: str) -> str:
        """Generate an encouraging AI coach message."""
        prompt = f"""
        You are a friendly and supportive health coach. The user has just completed the following:
        {context}
        Provide a short, motivating message (max 2 sentences) to encourage them to keep going.
        """
        return self.generate_response(prompt, temperature=0.9)