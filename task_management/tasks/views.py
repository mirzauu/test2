import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from pymongo import MongoClient
from bson import ObjectId

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

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


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet to handle CRUD operations for tasks.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all tasks for the authenticated user.",
        responses={200: TaskSerializer(many=True)}
    )
    def list(self, request):
        """
        Retrieve all tasks for the authenticated user.
        """
        tasks = list(tasks_collection.find({"user_id": request.user.id}))
        for task in tasks:
            task['_id'] = str(task['_id'])
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new task for the authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_name': openapi.Schema(type=openapi.TYPE_STRING, description='Task name'),
                'task_description': openapi.Schema(type=openapi.TYPE_STRING, description='Task description'),
            },
            required=['task_name']
        ),
        responses={201: openapi.Response("Task created successfully")}
    )
    def create(self, request):
        """
        Create a new task for the authenticated user.
        """
        task_name = request.data.get("task_name")
        task_description = request.data.get("task_description", "")

        if not task_name:
            raise ValidationError({"error": "Task name is required."})

        task = {
            "task_name": task_name,
            "task_description": task_description,
            "user_id": request.user.id,
            "status": "pending",
            "created_at": datetime.utcnow()
        }
        result = tasks_collection.insert_one(task)
        task['_id'] = str(result.inserted_id)
        return Response(task, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Retrieve a specific task by its ID.",
        responses={
            200: openapi.Response("Task retrieved successfully", TaskSerializer),
            404: openapi.Response("Task not found or unauthorized")
        }
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific task by its ID.
        """
        try:
            task = tasks_collection.find_one({"_id": ObjectId(pk), "user_id": request.user.id})
            if not task:
                return Response({"error": "Task not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
            task['_id'] = str(task['_id'])
            return Response(task)
        except Exception:
            return Response({"error": "Invalid task ID."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing task.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_name': openapi.Schema(type=openapi.TYPE_STRING, description='Task name'),
                'task_description': openapi.Schema(type=openapi.TYPE_STRING, description='Task description'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Task status')
            }
        ),
        responses={200: openapi.Response("Task updated successfully")}
    )
    def update(self, request, pk=None):
        """
        Update an existing task.
        """
        task_name = request.data.get("task_name")
        task_description = request.data.get("task_description")
        task_status = request.data.get("status")

        try:
            task = tasks_collection.find_one({"_id": ObjectId(pk), "user_id": request.user.id})
            if not task:
                return Response({"error": "Task not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

            update_data = {"updated_at": datetime.utcnow()}
            if task_name:
                update_data["task_name"] = task_name
            if task_description:
                update_data["task_description"] = task_description
            if task_status:
                update_data["status"] = task_status

            tasks_collection.update_one({"_id": ObjectId(pk)}, {"$set": update_data})
            updated_task = tasks_collection.find_one({"_id": ObjectId(pk)})
            updated_task['_id'] = str(updated_task['_id'])
            return Response(updated_task)
        except Exception:
            return Response({"error": "Invalid task ID or update failed."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a task.",
        responses={204: openapi.Response("Task deleted successfully")}
    )
    def destroy(self, request, pk=None):
        """
        Delete a task.
        """
        try:
            result = tasks_collection.delete_one({"_id": ObjectId(pk), "user_id": request.user.id})
            if result.deleted_count == 0:
                return Response({"error": "Task not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"error": "Invalid task ID."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@swagger_auto_schema(
    operation_description="Create a new user with username and password.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
        },
        required=['username', 'password']
    ),
    responses={201: openapi.Response("User created successfully!")}
)
def signup(request):
    """
    Create a new user with username and password.
    Supports both PostgreSQL and MongoDB user creation.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if users_collection.find_one({"username": username}):
        return Response({"error": "Username already exists in MongoDB."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    new_mongo_user = {
        "username": username,
        "password": make_password(password),
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(new_mongo_user)

    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "User created successfully!",
        "user_id": str(user.id),
        "username": username,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)
