from typing import List
from fastapi import FastAPI, HTTPException

from data_model.profile_model import Entrepreneur, Mentor, Investor
from db.FireStoreProfileDB import FirestoreProfileDVService
from vectorDB.PineconeDBService import PineconeDBService
from embedding.SentenceTransformEmbedding import SentenceTransformEmbedding

app = FastAPI()

# Initialize services
profile_db_service = FirestoreProfileDVService(project_id='your-project-id')
vector_db_service = PineconeDBService(api_key="YOUR_PINECONE_API_KEY", environment="us-west1-gcp",
                                      index_name="startup-ecosystem")
embedding_service = SentenceTransformEmbedding(model_name="text-embedding-ada-002")


# Define data models


# Routes to create profiles
@app.post("/entrepreneurs/")
async def create_entrepreneur(entrepreneur: Entrepreneur):
    text = f"{entrepreneur.background} {entrepreneur.experience} {entrepreneur.skills} {entrepreneur.currentStartupFocus} {entrepreneur.interests} {entrepreneur.goals} {entrepreneur.availability} {entrepreneur.preferredCommunication}"
    entrepreneur.embedding = embedding_service.generate_embedding(text)
    profile_id = profile_db_service.add_profile('entrepreneurs', entrepreneur.dict())
    vector_db_service.upsert_embedding(profile_id, entrepreneur.embedding)
    return {"id": profile_id}


@app.post("/mentors/")
async def create_mentor(mentor: Mentor):
    text = f"{mentor.professionalBackground} {mentor.industryExperience} {mentor.expertiseAreas} {mentor.previousMentoringExperience} {mentor.interests} {mentor.mentoringGoals} {mentor.availability} {mentor.preferredMentoringMethods}"
    mentor.embedding = embedding_service.generate_embedding(text)
    profile_id = profile_db_service.add_profile('mentors', mentor.dict())
    vector_db_service.upsert_embedding(profile_id, mentor.embedding)
    return {"id": profile_id}


@app.post("/investors/")
async def create_investor(investor: Investor):
    text = f"{investor.investmentBackground} {investor.portfolio} {investor.industryFocus} {investor.investmentCriteria} {investor.fundingStages} {investor.interests} {investor.goals} {investor.availability}"
    investor.embedding = embedding_service.generate_embedding(text)
    profile_id = profile_db_service.add_profile('investors', investor.dict())
    vector_db_service.upsert_embedding(profile_id, investor.embedding)
    return {"id": profile_id}


# Route to search for similar profiles
@app.get("/search/{profile_type}/similarity/")
async def search_similarity(profile_type: str, embedding: List[float]):
    if profile_type not in ['entrepreneurs', 'mentors', 'investors']:
        raise HTTPException(status_code=400, detail="Invalid profile type")

    results = vector_db_service.query_embedding(embedding)
    matched_profiles = []

    for result in results['matches']:
        profile = profile_db_service.get_profile(profile_type, result['id'])
        matched_profiles.append(profile)

    return matched_profiles


# Route to retrieve a specific profile by ID
@app.get("/{profile_type}/{profile_id}")
async def get_profile(profile_type: str, profile_id: str):
    if profile_type not in ['entrepreneurs', 'mentors', 'investors']:
        raise HTTPException(status_code=400, detail="Invalid profile type")

    profile = profile_db_service.get_profile(profile_type, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
