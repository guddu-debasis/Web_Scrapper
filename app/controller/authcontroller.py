from fastapi import HTTPException, status
from app.config.db import db
from app.utils.auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from app.services.summarizer import generate_rag_summary
from app.config.db import db
import datetime

async def signup_user(user_data):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user_data.dict()
    user_dict["password"] = hash_password(user_data.password)
    await db.users.insert_one(user_dict)
    return {"message": "User created successfully"}

async def login_user(user_data):
    user = await db.users.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}



async def handle_summarization(url: str, user_id: str):
    """
    Coordinates the RAG summarization process and database persistence.
    """
    try:
        # 1. Trigger the RAG Agent Service
        # This calls the LangChain logic we built previously
        summary_text = await generate_rag_summary(url)
        
        # 2. Prepare the document for MongoDB
        summary_document = {
            "user_id": user_id,
            "url": url,
            "summary": summary_text,
            "created_at": datetime.datetime.utcnow()
        }
        
        # 3. Store the result in the 'summaries' collection
        await db.summaries.insert_one(summary_document)
        
        # 4. Return the result to the Route
        return {
            "status": "success",
            "url": url,
            "summary": summary_text
        }
        
    except Exception as e:
        # Log the error for debugging
        print(f"Summarization Error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="The AI Agent failed to process the URL. Please check if the link is accessible."
        )