# faq_api
This project implements a FastAPI service to handle user queries, find the most similar question from a local FAQ database, and return an appropriate answer. If the similarity score between the user's query and the FAQ database is below a certain threshold, the service will fall back to OpenAI for an answer.
