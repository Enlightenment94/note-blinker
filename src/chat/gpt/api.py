import os
from openai import OpenAI
from dotenv import load_dotenv

class GPTAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY nie jest ustawiony w pliku .env")
            
        self.client = OpenAI(api_key=self.api_key)
        
    def send_message(self, message):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Błąd podczas komunikacji z API: {str(e)}" 