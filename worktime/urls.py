from django.urls import path
from .views import (
    StartWorkView,
    EndWorkView,
    StartBreakView,
    EndBreakView,
    WorkReportView,
    AdminUserWorkReport,
)

urlpatterns = [
    path('work/start/', StartWorkView.as_view(), name='start-work'),
    path('work/end/', EndWorkView.as_view(), name='end-work'),
    path('break/start/', StartBreakView.as_view(), name='start-break'),
    path('break/end/', EndBreakView.as_view(), name='end-break'),
    path('report/', WorkReportView.as_view(), name='work_report'),
    path('admin-report/', AdminUserWorkReport.as_view(), name='admin_report'),
]
