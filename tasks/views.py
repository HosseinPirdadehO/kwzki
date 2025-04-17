# Create your views here.


from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        task = self.get_object()

        if task.assigned_to != request.user:
            return Response({'detail': 'شما اجازه ثبت این تسک را ندارید.'}, status=403)

        submitted_text = request.data.get('submitted_text')
        if not submitted_text:
            return Response({'detail': 'متن ثبت‌شده الزامی است.'}, status=400)

        task.submitted_text = submitted_text
        task.is_completed = True
        task.save()

        return Response({'detail': 'تسک با موفقیت ثبت شد.'})
