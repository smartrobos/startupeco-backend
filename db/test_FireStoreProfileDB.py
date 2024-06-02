import unittest
from unittest.mock import patch, MagicMock
from google.api_core.exceptions import NotFound  # Import NotFound exception
from google.api_core.exceptions import NotFound
from db.FireStoreProfileDB import FirestoreProfileDBService, ProfileNotFoundError


class TestFirestoreProfileDBService(unittest.TestCase):

    @patch('db.FireStoreProfileDB.firestore')
    @patch('db.FireStoreProfileDB.service_account')
    def setUp(self, mock_service_account, mock_firestore):
        self.mock_db = MagicMock()
        mock_firestore.Client.return_value = self.mock_db
        self.service = FirestoreProfileDBService()

    def test_add_profile(self):
        self.mock_db.collection.return_value.document.return_value.collection.return_value.add.return_value = (
        None, MagicMock(id='123'))

        user_id = 'user123'
        role = 'entrepreneur'
        profile = {"name": "Alice", "skills": ["Python", "AI"]}

        profile_id = self.service.add_profile(user_id, role, profile)
        self.assertEqual(profile_id, '123')
        self.mock_db.collection.assert_called_with('users')
        self.mock_db.collection().document.assert_called_with(user_id)
        self.mock_db.collection().document().collection.assert_called_with(role)
        self.mock_db.collection().document().collection().add.assert_called_with(
            {'name': 'Alice', 'skills': ['Python', 'AI'], 'user_id': user_id})

    def test_get_profile(self):
        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"name": "Alice", "skills": ["Python", "AI"], 'user_id': 'user123'}
        self.mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = mock_doc

        user_id = 'user123'
        role = 'entrepreneur'
        profile_id = 'profile123'

        profile = self.service.get_profile(user_id, role, profile_id)
        self.assertEqual(profile, {"name": "Alice", "skills": ["Python", "AI"], 'user_id': 'user123'})
        self.mock_db.collection.assert_called_with('users')
        self.mock_db.collection().document.assert_called_with(user_id)
        self.mock_db.collection().document().collection.assert_called_with(role)
        self.mock_db.collection().document().collection().document.assert_called_with(profile_id)

    def test_get_profile_not_found(self):
        self.mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.side_effect = NotFound(
            'Profile not found')

        user_id = 'user123'
        role = 'entrepreneur'
        profile_id = 'profile123'

        with self.assertRaises(ProfileNotFoundError):
            self.service.get_profile(user_id, role, profile_id)


if __name__ == '__main__':
    unittest.main()
