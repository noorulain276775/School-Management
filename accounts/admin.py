from django.contrib import admin
from .models import CustomUser, Student, Parent
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Parent)