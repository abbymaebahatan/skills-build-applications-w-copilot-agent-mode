from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.conf import settings

from pymongo import MongoClient

# Sample data
USERS = [
    {"name": "Tony Stark", "email": "tony@marvel.com", "team": "marvel"},
    {"name": "Steve Rogers", "email": "steve@marvel.com", "team": "marvel"},
    {"name": "Bruce Wayne", "email": "bruce@dc.com", "team": "dc"},
    {"name": "Clark Kent", "email": "clark@dc.com", "team": "dc"},
]

TEAMS = [
    {"name": "marvel", "members": ["tony@marvel.com", "steve@marvel.com"]},
    {"name": "dc", "members": ["bruce@dc.com", "clark@dc.com"]},
]

ACTIVITIES = [
    {"user_email": "tony@marvel.com", "activity": "Running", "duration": 30},
    {"user_email": "steve@marvel.com", "activity": "Cycling", "duration": 45},
    {"user_email": "bruce@dc.com", "activity": "Swimming", "duration": 60},
    {"user_email": "clark@dc.com", "activity": "Yoga", "duration": 20},
]

LEADERBOARD = [
    {"team": "marvel", "points": 75},
    {"team": "dc", "points": 80},
]

WORKOUTS = [
    {"name": "HIIT", "suggested_for": "marvel"},
    {"name": "Pilates", "suggested_for": "dc"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient("mongodb://localhost:27017")
        db = client["octofit_db"]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Create unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
