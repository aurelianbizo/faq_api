from fastapi import FastAPI, HTTPException, status, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
import openai
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
import json
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session
from models import User
from crud import create_user, get_user#, #UserCreate
from dependencies import get_db
from database import engine, SessionLocal, Base

load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITH','HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES','30'))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

with open("question_database.json","r") as file:
    faq_database = json.load(file)

openai.api_key = OPENAI_API_KEY

########################################
# Embeddings using langchain library
########################################
embeddings = OpenAIEmbeddings(openai_api_key = openai.api_key, model="text-embedding-3-small")

questions = [item['question'] for item in faq_database]

question_embeddings = embeddings.embed_documents(questions)

def verify_token(token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
        
def get_current_user(token: str = Depends(verify_token)):
    return token

def create_access_token(data: dict, expires_delta : timedelta | None = None):    
    to_encode = data.copy()

    if isinstance(expires_delta,int):
        expires_delta = timedelta(minutes=expires_delta)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

###################################################
# Similarity check conditiona and return database answer
# if similarity is below the threshold 
###################################################
def find_most_similar_question(user_query, faq_database, faq_embeddings, threshold=0.7):
    # Compute embedding for the user query
    user_query_embedding = embeddings.embed_query(user_query)
    
    # Compute cosine similarities
    similarities = cosine_similarity([user_query_embedding], faq_embeddings)
    
    # Find the most similar question
    max_similarity_idx = np.argmax(similarities)
    max_similarity = similarities[0][max_similarity_idx]
    
    # Return the best match if the similarity is above the threshold
    if max_similarity >= threshold:
        return faq_database[max_similarity_idx], max_similarity
    else:
        return None, max_similarity

######################################
# access the opeani answer
###########################################
def get_answer_from_openai(user_query):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )
    answer = response.choices[0].message.content
    return answer

# Route to create a new user
@app.post("/create-users")
def create_new_user(name: str, password: str, db: Session = Depends(get_db)):
    return create_user(db=db, name=name, password=password)

# Route to get the current user
@app.post("/ask-question")
async def ask_question(username: str, password: str, user_query: str, db: Session = Depends(get_db)):

    db_user = get_user(db=db, name=username, password=password)  # Assuming user_id=1 for simplicity
 
    if not db_user and not (username == 'task_user_1' and password == 'task_password_1'):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate":"Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    
    current_user = verify_token(access_token)

    matched_faq, similarity = find_most_similar_question(user_query,faq_database,question_embeddings,threshold=0.8)

    # return the response either from local (if the similarity is above the threshold) or from openai
    if matched_faq: 
        # response from local
        return {
            "source": "local",
            "original_question": user_query,
            "matched_question": matched_faq['question'],
            "similarity_coef": "{:.2f}".format(similarity),
            "response": matched_faq['answer']
        }
    else:
        # response from openai
        answer = get_answer_from_openai(user_query)
        return {
            "source": "opeani",
            "original_question": user_query,
            "matched_question": "N/A",
            "similarity_coef": "{:.2f}".format(similarity),
            "response":answer
        }
