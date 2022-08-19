import firebase_admin
from constants import DATABASE_URL, FIREBASE_CERTIFICATE


EXERCISES_NEXT_ID_KEY = "exercises_nextid"
EXERCISES_KEY = "exercises"
WORKOUT_ITEMS_NEXT_ID_KEY = "workoutitems_nextid"
WORKOUT_ITEMS_KEY = "workoutitems"

BASE_PATH = "/"
EXERCISES_NEXT_ID_PATH = f"/{EXERCISES_NEXT_ID_KEY}/"
EXERCISES_PATH = f"/{EXERCISES_KEY}/"
WORKOUT_ITEMS_NEXT_ID_PATH = f"/{WORKOUT_ITEMS_NEXT_ID_KEY}/"
WORKOUT_ITEMS_PATH = f"/{WORKOUT_ITEMS_KEY}/"
LANGUAGE_ITEMS_PATH = "/language/users/"


cred_obj = firebase_admin.credentials.Certificate(FIREBASE_CERTIFICATE)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': DATABASE_URL
})
