# FAQ Querying API
This project implements a FastAPI service to handle user queries, find the most similar question from a local FAQ database, and return an appropriate answer. If the similarity score between the user's query and the FAQ database is below a certain threshold, the service will fall back to OpenAI for an answer.

Features
User Authentication: Users can create accounts and authenticate using JWT tokens.

FAQ Matching: Matches user queries with the most similar FAQ question based on embeddings.

OpenAI Fallback: If no suitable match is found in the local FAQ, OpenAI's GPT model is used to generate an answer.

JWT Authentication: Secure API access with JWT token-based authentication.

Setup and Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/faq-querying-api.git
cd faq-querying-api
```

2. Install the dependencies
Make sure you have Python 3.7+ installed. Then, create a virtual environment and install the necessary packages.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables
Create a .env file in the root directory and add the following environment variables:

```bash
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY: Secret key used for JWT token generation.
```

ALGORITHM: JWT algorithm used for encoding/decoding.

ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for JWT tokens.

OPENAI_API_KEY: Your OpenAI API key for generating answers when no FAQ match is found.

4. Database Setup
If you are using SQLAlchemy, make sure the database tables are set up. You can do this with the following command:

```bash
python -m models
```

5. Start the FastAPI server
Run the following command to start the server:

```bash
uvicorn app:app --reload
```
Your API should now be running at http://127.0.0.1:8000.

# API Endpoints
1. /create-users - Create a New User
This endpoint allows users to create a new account.

Method: POST

Parameters:

name: The username of the user.

password: The password for the user.

Example Request:
```bash
POST /create-users
{
  "name": "new_user",
  "password": "secure_password"
}
```
Example Response:
```bash
{
  "message": "User created successfully"
}
```
2. /ask-question - Ask a Question
This endpoint allows users to ask a question. It will match the question with the most similar FAQ question and return an answer. If no match is found, OpenAI will provide an answer.

Method: POST

Parameters:

username: The username of the user.

password: The password for the user.

user_query: The question the user is asking.

Example Request:
```bash
POST /ask-question
{
  "username": "task_user_1",
  "password": "task_password_1",
  "user_query": "How can I reset my password?"
}
```
Example Response (Local Match):
```bash
{
  "source": "local",
  "original_question": "How can I reset my password?",
  "matched_question": "What steps do I take to reset my password?",
  "similarity_coef": "0.92",
  "response": "Go to account settings, select 'Change Password', enter your current password and then the new one. Confirm the new password and save the changes."
}
```
Example Response (OpenAI Fallback):
```bash
{
  "source": "openai",
  "original_question": "How can I reset my password?",
  "matched_question": "N/A",
  "similarity_coef": "0.65",
  "response": "To reset your password, you need to go to the account settings and click on 'Forgot Password'. Then follow the instructions sent to your email."
}
```
Project Structure
```bash
.
├── app.py             # FastAPI application
├── models.py          # Database models and schema
├── crud.py            # CRUD operations for database interactions
├── dependencies.py    # Dependency injection functions
├── database.py        # Database connection setup
├── .env               # Environment variables (not to be committed)
├── requirements.txt   # Python dependencies
├── question_database.json  # JSON file containing FAQ questions and answers
└── README.md          # Project documentation
```

Requirements
Python 3.7+

FastAPI

SQLAlchemy

OpenAI Python client (openai)

langchain for embeddings

scikit-learn for cosine similarity

python-jose for JWT authentication

python-dotenv for managing environment variables

Install Requirements:
```bash
pip install -r requirements.txt
```
License
This project is licensed under the Apache 2.0 License.