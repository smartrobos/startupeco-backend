from typing import List
from pydantic import BaseModel


# Define data models
class Entrepreneur(BaseModel):
    user_id: str
    background: str
    experience: str
    skills: List[str]
    currentStartupFocus: str
    interests: List[str]
    goals: str
    availability: str
    preferredCommunication: str
    embedding: List[float] = None


class Mentor(BaseModel):
    user_id: str
    professionalBackground: str
    industryExperience: str
    expertiseAreas: List[str]
    previousMentoringExperience: str
    interests: List[str]
    mentoringGoals: str
    availability: str
    preferredMentoringMethods: str
    embedding: List[float] = None


class Investor(BaseModel):
    user_id: str
    investmentBackground: str
    portfolio: List[str]
    industryFocus: List[str]
    investmentCriteria: str
    fundingStages: List[str]
    interests: List[str]
    goals: str
    availability: str
    embedding: List[float] = None
