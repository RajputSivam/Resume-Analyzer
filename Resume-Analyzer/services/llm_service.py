from groq import Groq

from config import Config


class LLMService:

    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

    def chat(self, system_prompt: str, user_prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=Config.MODEL,
            temperature=Config.TEMPERATURE,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content
