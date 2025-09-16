from django.contrib import admin
from .models import Student, AttendanceSession, AttendanceRecord

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name')
    search_fields = ('roll_no', 'name')

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'date')
    search_fields = ('session_id',)
    date_hierarchy = 'date'

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'timestamp', 'status')
    list_filter = ('session', 'timestamp', 'status')
    search_fields = ('student__roll_no', 'student__name', 'session__session_id')
    date_hierarchy = 'timestamp'
