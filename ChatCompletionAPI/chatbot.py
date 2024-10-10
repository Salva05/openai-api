import os
import openai
import logging
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initializes the Chatbot instance with the provided API key and model.
        """
        if not api_key:
            raise ValueError("API key must be provided to initialize the chatbot.")
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        self.chat_history = [{"role": "system", "content": "You are a helpful assistant responsible for fulfilling users' requests."}]
        logger.info("Chatbot initialized with model %s", model)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generates a response using OpenAI's Chat Completion API.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            logger.error("OpenAI API error: %s", e)
            return f"An error occurred: {e}"
        except KeyError:
            logger.error("Unexpected response format received from the API.")
            return "Unexpected response format received from the API."

    def get_response(self, prompt: str) -> str:
        """
        Adds the user's prompt to the chat history and generates a response.
        """
        self.chat_history.append({"role": "user", "content": prompt})
        response = self.generate_response(self.chat_history)
        self.chat_history.append({"role": "assistant", "content": response})
        return response

    def clear_history(self):
        """
        Clears the chat history, retaining only the system message.
        """
        self.chat_history = [{"role": "system", "content": "You are a helpful assistant responsible for fulfilling users' requests."}]
        logger.info("Chat history cleared.")

# Helper function to load API key from environment variables
def load_api_key() -> str:
    """
    Loads the API key from environment variables.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key. Please set the OPENAI_API_KEY environment variable.")
    return api_key

# Create an instance of Chatbot that can be imported and reused elsewhere
def create_chatbot(api_key: Optional[str] = None, model: str = "gpt-4") -> Chatbot:
    """
    Creates a Chatbot instance with the provided API key and model.
    """
    if not api_key:
        api_key = load_api_key()
    return Chatbot(api_key, model)

if __name__ == "__main__":
    # Example usage of chatbot in command-line interface
    chatbot = create_chatbot()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif user_input.lower() == "clear":
            chatbot.clear_history()
            print("Chat history cleared.")
            continue

        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}")