from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=40)
    roll_no = models.CharField(max_length=20, unique=True)
    # aur fields lagau toh

    def __str__(self):
        return self.name

class AttendanceSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} - {self.date}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='present')
