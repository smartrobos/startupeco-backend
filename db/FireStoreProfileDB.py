from typing import Dict, Optional
from google.cloud import firestore
from google.api_core.exceptions import NotFound

from db.ProfileDBService import ProfileDBService


class FirestoreProfileDVService(ProfileDBService):
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)

    def add_profile(self, collection: str, profile: Dict) -> str:
        """Adds a profile to the specified collection and returns the document ID."""
        doc_ref = self.db.collection(collection).document()  # Generate ID automatically
        doc_ref.set(profile)  # Directly set the data
        return doc_ref.id

    def get_profile(self, collection: str, profile_id: str) -> Optional[Dict]:
        """Retrieves a profile from the specified collection. Returns None if not found."""
        doc_ref = self.db.collection(collection).document(profile_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None


if __name__ == '__main__':
    service = FirestoreProfileDVService("your-project-id")

    # Add a profile
    new_profile = {"name": "Alice", "skills": ["Python", "AI"]}
    profile_id = service.add_profile("entrepreneurs", new_profile)

    # Get a profile
    retrieved_profile = service.get_profile("entrepreneurs", profile_id)
    if retrieved_profile:
        print(retrieved_profile)
    else:
        print("Profile not found")
