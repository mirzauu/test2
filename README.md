
# Task Management

## Description

Task Management is a web application that helps users manage their tasks. The application allows users to create, update, retrieve, and delete tasks. Notifications about tasks can be sent via email.

### Features:
- User authentication via JWT
- Task management (create, update, delete)
- MongoDB integration for task and user storage
- Email notifications for tasks
- Hosted at: http://54.226.194.254/

## Technologies Used

- Django
- MongoDB
- Celery
- JWT (JSON Web Tokens)
- DRF (Django Rest Framework)
- drf_yasg (Swagger API Documentation)
- psycopg2 (for PostgreSQL compatibility)
- Django-Redis (for caching)
## Installation Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/mirzauu/test2.git
    cd test2/task_management
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your `.env` file with the following information:

    ```env
    SECRET_KEY=django-insecure-+o%jpdy5am_7yr(*_zt&w^yr%*=i^)g=w7+r87vw!9249xr75z
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    DATABASE_NAME=test2
    DATABASE_USER=postgres
    DATABASE_PASSWORD=alimirsa1
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    MONGO_DB_URI=mongodb+srv://alimirsa123:a5VtspGwzNRv3m7b@cluster0.3wmvf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
    MONGO_DB_NAME=Cluster0
    CELERY_BROKER_URL=redis://localhost:6379
    CELERY_RESULT_BACKEND=redis://localhost:6379
    ```
4. Run migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Documentation

The base URL for all API endpoints is:
```
http://54.226.194.254/
```

### Swagger UI
- The Swagger UI for API documentation is available at:
    ```url
    http://<your-server-ip>/swagger/
    ```

### API Endpoints
All API endpoints are accessible under the base URL `/api/`.

#### 1. User Signup
- **URL**: `/api/signup/`
- **Method**: POST
- **Description**: Create a new user with username and password.
- **Request Body**:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
- **Response**: 
    ```json
    {
        "message": "User created successfully!",
        "user_id": "string",
        "username": "string",
        "refresh": "string",
        "access": "string"
    }
    ```

#### 2. Task CRUD Operations

##### Create Task
- **URL**: `/api/tasks/`
- **Method**: POST
- **Description**: Create a new task for the authenticated user.
- **Request Body**:
    ```json
    {
        "task_name": "string",
        "task_description": "string"
    }
    ```
- **Response**:
    ```json
    {
        "_id": "string",
        "task_name": "string",
        "task_description": "string",
        "status": "string",
        "created_at": "string"
    }
    ```

##### List Tasks
- **URL**: `/api/tasks/`
- **Method**: GET
- **Description**: Retrieve all tasks for the authenticated user.
- **Response**:
    ```json
    [
        {
            "_id": "string",
            "task_name": "string",
            "task_description": "string",
            "status": "string",
            "created_at": "string"
        }
    ]
    ```

##### Retrieve Task by ID
- **URL**: `/api/tasks/{task_id}/`
- **Method**: GET
- **Description**: Retrieve a specific task by its ID.
- **Response**:
    ```json
    {
        "_id": "string",
        "task_name": "string",
        "task_description": "string",
        "status": "string",
        "created_at": "string"
    }
    ```

##### Update Task
- **URL**: `/api/tasks/{task_id}/`
- **Method**: PUT
- **Description**: Update an existing task.
- **Request Body**:
    ```json
    {
        "task_name": "string",
        "task_description": "string",
        "status": "string"
    }
    ```
- **Response**:
    ```json
    {
        "_id": "string",
        "task_name": "string",
        "task_description": "string",
        "status": "string",
        "updated_at": "string"
    }
    ```

##### Delete Task
- **URL**: `/api/tasks/{task_id}/`
- **Method**: DELETE
- **Description**: Delete a task by its ID.
- **Response**:
    ```json
    {
        "message": "Task deleted successfully."
    }
    ```

## Testing Instructions
To test the API:

1. Run the server locally.
2. Use the Swagger UI at `/swagger/` to test all API endpoints.
3. Use the following test cases for the task management:
    - **Create Task**: Send a POST request to `/api/tasks/` with valid data.
    - **List Tasks**: Send a GET request to `/api/tasks/` to retrieve all tasks.
    - **Retrieve Task**: Send a GET request to `/api/tasks/{task_id}/` to get a specific task.
    - **Update Task**: Send a PUT request to `/api/tasks/{task_id}/` with updated data.
    - **Delete Task**: Send a DELETE request to `/api/tasks/{task_id}/` to delete a task.

## Conclusion
This is the Task Management API for handling tasks with CRUD operations. It is fully integrated with MongoDB for task storage and PostgreSQL for user management.
