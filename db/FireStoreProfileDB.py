from typing import Dict, Optional
from google.cloud import firestore
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

from db.ProfileDBService import ProfileDBService


class FirestoreProfileDBService(ProfileDBService):
    def __init__(self, project_id: str = "startup-eco",
                 credentials_path: str = "startup-eco-firebase-adminsdk-7k3jj-14065c1b86.json"):

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.db = firestore.Client(project=project_id, credentials=credentials)

    def add_profile(self, user_id: str, role: str, profile: Dict) -> str:
        """Adds a profile to the specified collection and returns the document ID."""
        profile['user_id'] = user_id  # Include user_id in the profile
        # Check if a profile already exists for the given user_id and role
        existing_profiles = self.db.collection('users').document(user_id).collection(role).stream()
        for doc in existing_profiles:
            if doc.exists:
                # Profile already exists, update it
                print(f"Profile already exists for user {user_id} in role {role} with ID {doc.id}")
                doc.reference.update(profile)
                return doc.id  # Return the existing profile ID

        _, doc_ref  = self.db.collection('users').document(user_id).collection(role).add(
            profile)  # Use add() for auto-generated ID
        print(f"Profile added with ID: {doc_ref.id}")
        return doc_ref.id

    def get_profile(self, user_id: str, role: str, profile_id: str) -> Dict | None:
        """Retrieves a profile from the specified collection. Returns None if not found."""
        doc_ref = self.db.collection('users').document(user_id).collection(role).document(profile_id)
        try:
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except NotFound:
            raise ProfileNotFoundError(f"Profile with ID {profile_id} not found for user {user_id} in role {role}")


class ProfileNotFoundError(Exception):
    """Custom exception for profile not found errors."""
    pass


if __name__ == '__main__':
    service = FirestoreProfileDBService()

    user_id = 'user123'
    role = 'mentor'

    # Add a profile
    new_profile = {"name": "Alice", "skills": ["Python", "AI", "Data Science"]}
    try:
        profile_id = service.add_profile(user_id, role, new_profile)
    except Exception as e:
        print(f"Error adding profile: {e}")

    # Get a profile
    try:
        retrieved_profile = service.get_profile(user_id, role, profile_id)
        if retrieved_profile:
            print(retrieved_profile)
        else:
            print("Profile not found")
    except ProfileNotFoundError as e:
        print(f"Error retrieving profile: {e}")
    except Exception as e:
        print(f"Error retrieving profile: {e}")
