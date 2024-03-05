import firebase_admin
from firebase_admin import firestore

from Config import FirestoreConfig


class FireStore:
    def __init__(self, config: FirestoreConfig):
        cred = firebase_admin.credentials.Certificate(config.to_dict())
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.collection = self.db.collection("users")

    def get_user(self, user_id: str) -> dict | None:
        user = self.collection.document(user_id).get()
        return user.to_dict()

    def create_user(self, user_id: str, data: dict):
        self.collection.document(user_id).set(data)

    def update_user(self, user_id: str, data: dict):
        self.collection.document(user_id).update(data)
