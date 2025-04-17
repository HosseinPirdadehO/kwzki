from rest_framework import serializers
from .models import WorkSession, BreakSession


class BreakSessionSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = BreakSession
        fields = ['id', 'start_time', 'end_time',
                  'duration', 'created_at', 'updated_at']

    def get_duration(self, obj):
        return obj.duration()


class WorkSessionSerializer(serializers.ModelSerializer):
    breaks = BreakSessionSerializer(many=True, read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = WorkSession
        fields = ['id', 'user', 'start_time', 'end_time',
                  'duration', 'created_at', 'updated_at', 'breaks']
        read_only_fields = ['user']

    def get_duration(self, obj):
        return obj.duration()
