from django.contrib import admin
from .models import WorkSession, BreakSession
# Register your models here.


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time',
                    'get_duration', 'created_at')
    list_filter = ('start_time', 'end_time', 'user')
    search_fields = ('user__first_name', 'user__last_name',
                     'user__phone_number')
    date_hierarchy = 'start_time'

    def get_duration(self, obj):
        duration = obj.duration()
        if duration:
            return str(duration)
        return '-'
    get_duration.short_description = 'مدت زمان کار'


@admin.register(BreakSession)
class BreakSessionAdmin(admin.ModelAdmin):
    list_display = ('work_session', 'start_time', 'end_time', 'get_duration')
    list_filter = ('start_time', 'end_time')
    date_hierarchy = 'start_time'

    def get_duration(self, obj):
        duration = obj.duration()
        if duration:
            return str(duration)
        return '-'
    get_duration.short_description = 'مدت استراحت'
