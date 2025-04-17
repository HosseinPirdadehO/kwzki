from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from datetime import datetime
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import WorkSession, BreakSession, WorkSession
from .serializers import WorkSessionSerializer, BreakSessionSerializer
from django.utils import timezone

# Create your views here.
User = get_user_model()


class StartWorkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if WorkSession.objects.filter(user=request.user, end_time__isnull=True).exists():
            return Response({'detail': 'شما در حال حاضر در یک جلسه کاری فعال هستید.'}, status=400)

        session = WorkSession.objects.create(user=request.user)
        return Response(WorkSessionSerializer(session).data, status=201)


class EndWorkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            session = WorkSession.objects.get(
                user=request.user, end_time__isnull=True)
            session.end_time = timezone.now()
            session.save()
            return Response(WorkSessionSerializer(session).data)
        except WorkSession.DoesNotExist:
            return Response({'detail': 'هیچ جلسه کاری فعالی برای پایان دادن وجود ندارد.'}, status=400)


class StartBreakView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            work_session = WorkSession.objects.get(
                user=request.user, end_time__isnull=True)

            if BreakSession.objects.filter(work_session=work_session, end_time__isnull=True).exists():
                return Response({'detail': 'شما هم‌اکنون در حال استراحت هستید.'}, status=400)

            break_session = BreakSession.objects.create(
                work_session=work_session)
            return Response(BreakSessionSerializer(break_session).data, status=201)
        except WorkSession.DoesNotExist:
            return Response({'detail': 'هیچ جلسه کاری فعالی برای شروع استراحت وجود ندارد.'}, status=400)


class EndBreakView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            work_session = WorkSession.objects.get(
                user=request.user, end_time__isnull=True)
            break_session = BreakSession.objects.get(
                work_session=work_session, end_time__isnull=True)
            break_session.end_time = timezone.now()
            break_session.save()
            return Response(BreakSessionSerializer(break_session).data)
        except (WorkSession.DoesNotExist, BreakSession.DoesNotExist):
            return Response({'detail': 'هیچ استراحت فعالی برای پایان دادن وجود ندارد.'}, status=400)


class WorkReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        period = request.query_params.get('period', 'daily')

        if period == 'weekly':
            start_date = now().date() - timedelta(days=7)
        else:
            start_date = now().date()

        sessions = WorkSession.objects.filter(
            user=user,
            start_time__date__gte=start_date
        ).order_by('-start_time')

        report = []
        for session in sessions:
            work_duration = session.duration()
            break_total = sum(
                [b.duration().total_seconds()
                 for b in session.breaks.all() if b.duration()],
                0
            )
            work_seconds = work_duration.total_seconds() if work_duration else 0
            net_seconds = work_seconds - break_total

            report.append({
                "date": session.start_time.date(),
                "start": session.start_time.time(),
                "end": session.end_time.time() if session.end_time else None,
                "total_work": round(work_seconds / 3600, 2),
                "total_break": round(break_total / 3600, 2),
                "net_hours": round(net_seconds / 3600, 2)
            })

        return Response({
            "user": f"{user.first_name} {user.last_name}",
            "report_type": period,
            "report": report
        })


class AdminUserWorkReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = request.query_params.get("period", "daily")
        if period == "weekly":
            start_date = now().date() - timedelta(days=7)
        else:
            start_date = now().date()

        users_data = []
        users = User.objects.all()

        for user in users:
            sessions = WorkSession.objects.filter(
                user=user,
                start_time__date__gte=start_date
            )
            total_work = 0
            total_break = 0

            for session in sessions:
                if session.end_time:
                    work_duration = (session.end_time -
                                     session.start_time).total_seconds()
                    total_work += work_duration
                    total_break += sum(
                        (b.end_time - b.start_time).total_seconds()
                        for b in session.breaks.all() if b.end_time
                    )

            users_data.append({
                "user": f"{user.first_name} {user.last_name}",
                "phone": user.phone_number,
                "position": user.position,
                "total_work_hours": round(total_work / 3600, 2),
                "total_break_hours": round(total_break / 3600, 2),
                "net_hours": round((total_work - total_break) / 3600, 2),
            })

        return Response({
            "period": period,
            "results": users_data
        })
