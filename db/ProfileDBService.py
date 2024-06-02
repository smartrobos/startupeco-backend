from typing import Dict


class ProfileDBService:
    def add_profile(self, collection: str, profile: Dict) -> str:
        raise NotImplementedError

    def get_profile(self, collection: str, profile_id: str) -> Dict:
        raise NotImplementedError
