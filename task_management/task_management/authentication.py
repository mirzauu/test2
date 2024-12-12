# task_management/authentication.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from bson import ObjectId
from django.conf import settings

User = get_user_model()

class MongoDBAuthBackend(ModelBackend):
    """
    Custom authentication backend that supports both PostgreSQL users and MongoDB users
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # First, try to authenticate with PostgreSQL users
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                # If PostgreSQL user not found, check MongoDB
                users_collection = settings.MONGO_COLLECTIONS['users']
                mongo_user = users_collection.find_one({"username": username})
                
                if mongo_user:
                    # Verify password for MongoDB user
                    if check_password(password, mongo_user['password']):
                        # Create or get a corresponding Django user
                        user, created = User.objects.get_or_create(
                            username=username,
                            defaults={
                                'is_active': True,
                                'is_staff': False,
                                'is_superuser': False
                            }
                        )
                        return user
            
            return None
        
        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    def get_user(self, user_id):
        """
        Retrieve user by ID from PostgreSQL or MongoDB
        """
        try:
            # Try to get user from PostgreSQL
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # If not found in PostgreSQL, check MongoDB
            users_collection = settings.MONGO_COLLECTIONS['users']
            try:
                mongo_user = users_collection.find_one({"_id": ObjectId(user_id)})
                if mongo_user:
                    # Create a temporary user object if needed
                    user, created = User.objects.get_or_create(
                        username=mongo_user['username'],
                        defaults={
                            'is_active': True,
                            'is_staff': False,
                            'is_superuser': False
                        }
                    )
                    return user
            except:
                return None