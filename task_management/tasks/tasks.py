from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Configuration
mongo_client = MongoClient(
    "mongodb+srv://alimirsa123:a5VtspGwzNRv3m7b@cluster0.3wmvf.mongodb.net/",
    retryWrites=True,
    w="majority",
    appName="Cluster0"
)
mongo_db = mongo_client["Cluster0"]
users_collection = mongo_db["users"]
tasks_collection = mongo_db["tasks"]

@shared_task
def send_task_reminders():
    """
    Celery task to send reminders for tasks due tomorrow.
    """
    tomorrow = now() + timedelta(days=1)
    tomorrow_iso = tomorrow.isoformat()  # Convert to ISO format for MongoDB queries

    # Find tasks due tomorrow and still pending
    tasks = tasks_collection.find({
        "due_date": {"$lte": tomorrow_iso},
        "status": "pending"
    })

    for task in tasks:
        # Fetch user details from the users_collection
        user = users_collection.find_one({"_id": ObjectId(task["user_id"])})
        if user and "email" in user:
            send_mail(
                'Task Reminder',
                f'Reminder: Your task "{task["title"]}" is due tomorrow.',
                'from@example.com',
                [user["email"]],
                fail_silently=False,
            )
