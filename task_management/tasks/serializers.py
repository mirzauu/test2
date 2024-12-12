from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    task_name = serializers.CharField()
    task_description = serializers.CharField(required=False)
    user_id = serializers.IntegerField()
    status = serializers.CharField(default='pending')
