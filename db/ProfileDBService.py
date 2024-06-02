from typing import Dict


class ProfileDBService:
    def add_profile(self, user_id: str, role: str, profile: Dict) -> str:
        raise NotImplementedError

    def get_profile(self, user_id: str, role: str, profile_id: str) -> Dict | None:
        raise NotImplementedError
