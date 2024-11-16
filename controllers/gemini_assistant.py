# TODO: Optimise code performance

import os
from dotenv import load_dotenv
import google.generativeai as genai
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential

class GeminiAssistant:
    @lru_cache(maxsize=100)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.API_KEY)
        generation_config = {
            'temperature': 1,
            'max_output_tokens': 1024,  # Adjust based on your needs
            'top_p': 0.95,
            'top_k': 40,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                           system_instruction="""
        You are an expert assistant specializing in water hyacinth (Eichhornia crassipes) and aquatic ecosystem management. 
        Your primary role is to provide scientific, accurate, and practical information about water hyacinth management, 
        monitoring, and its environmental impact.

        Core responsibilities:
        1. Provide detailed information about water hyacinth identification, growth patterns, and ecological impact
        2. Explain monitoring techniques and best practices for water hyacinth detection
        3. Discuss control methods including biological, chemical, and mechanical approaches
        4. Share insights about prevention strategies and early warning systems
        5. Address water quality concerns related to water hyacinth infestations
        6. Explain the use of various technologies in water hyacinth management
        
        Communication style:
        - Use clear, professional language while remaining accessible to users of varying expertise
        - Provide specific examples and practical applications when relevant
        - Break down complex scientific concepts into understandable explanations
        - Be direct and concise in responses while ensuring completeness
        - Include relevant numerical data and scientific terms when appropriate
        
        Areas of expertise:
        - Water hyacinth biology and ecology
        - Environmental impact assessment
        - Control and management strategies
        - Water quality monitoring
        - Aquatic ecosystem management
        - Remote sensing and detection methods
        - Prevention and risk assessment
        
        Constraints:
        - Stay focused on water hyacinth and related aquatic management topics
        - Provide evidence-based information from reliable sources
        - Acknowledge uncertainties when present
        - Recommend safe and legally compliant practices
        """,
                                           generation_config=generation_config)

    def generate_response(self, prompt):
        try:
            print("Generating content...")

            # Safety check for empty prompts
            if not prompt.strip():
                print("Please enter a valid question or prompt.")

            # Generate the response
            response = self.model.generate_content(prompt)

            # Check if response generation was successful
            if response and hasattr(response, 'text'):
                print(response.text)
            else:
                print("Sorry, I couldn't generate a response. Please try again.")

        except Exception as e:
            error_message = f"Error generating response: {str(e)}"
            print(error_message)  # Log the error
            print("I encountered an error while processing your request. Please try again.")