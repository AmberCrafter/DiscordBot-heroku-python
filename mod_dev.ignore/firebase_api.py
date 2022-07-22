# import firebase
from firebase import firebase
import os
from dotenv import load_dotenv

# firebase structure
# firebase
#   + table
#       - key: value


load_dotenv()

TOKEN = os.getenv("FIREBASE_KEY")
EMAIL = os.getenv("FIREBASE_EMAIL")
URL = os.getenv("FIREBASE_URL")
authentication = firebase.FirebaseAuthentication(
    TOKEN,
    EMAIL
)

# firebase.authentication = authentication
user = authentication.get_user()
firebase = firebase.FirebaseApplication(
    URL,
    authentication
)

result = firebase.put("/test", "data1", 123)
