# Chatbot Project

This project is a modular, enterprise-level chatbot application that utilizes OpenAI's Chat Completion API for generating responses. It is designed to be reusable, scalable, and easy to extend with different components. This documentation explains each part of the project, its purpose, and how to run it effectively.

## Project Directory Structure

### chatbot_project/
- **services/**
  - `openai_service.py` - Implements the OpenAI API integration.
  - `abstract_ai_service.py` - Defines an abstract base class to provide a generic interface for any AI service.
- **utils/**
  - `logging_config.py` - Configures logging for both general logs and chat logs.
- **core/**
  - `chatbot.py` - The main chatbot class that integrates AI services, manages chat history, and communicates with the user.
  - `chat_logic_service.py` - Manages chat-related logic, including preparing the initial conversation history and appending messages.
- **config/**
  - `settings.py` - Handles application settings and loads environment variables.
- **persistence/**
  - `chat_repository.py` - Provides database operations to persist chat history.
- `main.py` - Command-line interface to interact with the chatbot.
- **api/**
  - `app.py` - REST API to interact with the chatbot using FastAPI.

## Components Explained

### 1. AI Service Abstraction (`services/abstract_ai_service.py`)
The `AbstractAIService` class defines an abstract base for any AI service. This allows the project to easily switch to a different AI service in the future, ensuring flexibility.

### 2. OpenAI Service (`services/openai_service.py`)
The `OpenAIService` class implements the `AbstractAIService` to connect with OpenAI's API. It handles the API key and performs the actual request to generate responses.

### 3. Logging Configuration (`utils/logging_config.py`)
The `logging_config.py` module sets up two types of logging:
- **General Log** (`chatbot_project.log`): Stores all activities and errors for monitoring the application.
- **Chat Log** (`chat.log`): Records each user-bot interaction, including user prompts and chatbot responses, providing a detailed record of conversations.

### 4. Chat Logic (`core/chat_logic_service.py`)
The `ChatLogicService` class manages chat-related logic such as preparing the initial system message and appending user/assistant messages. This keeps the chatbot’s logic modular and easy to maintain.

### 5. Chatbot (`core/chatbot.py`)
The `Chatbot` class is the core interface for user interaction. It:
- Integrates the AI service to generate responses.
- Manages conversation history.
- Logs both general information and chat interactions.

### 6. Settings Configuration (`config/settings.py`)
The `settings.py` module is responsible for loading environment variables, such as the OpenAI API key, using Pydantic's `BaseSettings` for easy configuration management.

### 7. Chat Persistence (`persistence/chat_repository.py`)
The `ChatRepository` class manages chat history persistence using SQLite. It allows saving and loading chat history from the database, supporting features such as resuming conversations.

### 8. Main Command-Line Interface (`main.py`)
The `main.py` file provides a command-line interface to interact with the chatbot. Users can start a conversation, clear the history, and exit the application using simple commands.

### 9. REST API Interface (`api/app.py`)
The `app.py` module provides a REST API to interact with the chatbot. This API, built using FastAPI, includes endpoints for chatting (`/chat`) and clearing history (`/clear_history`).

## Prerequisites
- Python 3.8 or later
- OpenAI API key
- Required Python packages:
  - `openai`
  - `fastapi`
  - `uvicorn`
  - `pydantic-settings`
  - `python-json-logger`
  - `tenacity`
  - `dotenv`
  - `sqlite3`

Install the required packages by running:

```sh
pip install -r requirements.txt
```

## Running the Project

### 1. Environment Setup
Create a `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Running the Command-Line Chatbot
To run the chatbot using the command line:

```sh
python main.py
```
- Type your message and the bot will respond.
- Type `clear` to reset the conversation history.
- Type `exit` or `quit` to end the session.

### 3. Running the API Server
To run the REST API server using FastAPI:

```sh
uvicorn api.app:app --reload
```
- **POST /chat**: Send a user prompt and receive the chatbot response.
  - Example request body: `{ "prompt": "Hello!" }`
- **POST /clear_history**: Clears the conversation history.

### 4. Logging
- **General Logs**: All logs during the lifetime of the program are saved in `chatbot_project.log`.
- **Chat Logs**: Chat-specific interactions are logged in `chat.log`.

## Project Highlights

### 1. Modular Design
- The project follows a modular architecture where components are separated into different modules. This makes the project easy to extend, maintain, and debug.

### 2. Abstraction and Flexibility
- Using the `AbstractAIService` allows for switching AI backends easily. If OpenAI is replaced or multiple AI services are required, they can be implemented with minimal changes.

### 3. Persistence Layer
- The `ChatRepository` ensures that chat history can be saved to and retrieved from a local SQLite database. This makes it possible to continue conversations between sessions.

### 4. Logging Capabilities
- Comprehensive logging provides insights into both general events and detailed conversation logs, which is useful for monitoring and debugging.

### 5. REST API Interface
- The REST API, built using FastAPI, allows for easy integration of the chatbot with other applications or frontend interfaces.

## Future Enhancements
- **User Authentication**: Add user authentication to the API to support multiple users and keep chat histories private.
- **Frontend Integration**: Create a frontend using React or Vue.js to offer a web interface for users to interact with the chatbot.
- **Advanced Error Handling**: Improve the error handling mechanism to provide more descriptive messages and retry strategies for API failures.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## License
This project is licensed under the MIT License.