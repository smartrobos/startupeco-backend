from typing import List
from pydantic import BaseModel

class Entrepreneur(BaseModel):
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
    investmentBackground: str
    portfolio: List[str]
    industryFocus: List[str]
    investmentCriteria: str
    fundingStages: List[str]
    interests: List[str]
    goals: str
    availability: str
    embedding: List[float] = None