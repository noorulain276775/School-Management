from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'get_student_name', 'parent',
                    'get_parent_email', 'get_parent_phone')

    def get_student_name(self, obj):
        return obj.user.get_full_name() if obj.user else None
    get_student_name.short_description = 'Student Name'

    def get_parent_email(self, obj):
        return obj.parent.user.email if obj.parent.user else None
    get_parent_email.short_description = 'Parent Email'

    def get_parent_phone(self, obj):
        return obj.parent.user.phone if obj.parent.user else None
    get_parent_phone.short_description = 'Parent Phone'


class ParentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_email', 'get_phone', 'get_children_info')

    def get_email(self, obj):
        return obj.user.email if obj.user else None
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.user.phone if obj.user else None
    get_phone.short_description = 'Phone'

    def get_children_info(self, obj):
        kids = Student.objects.filter(parent=obj)
        kid_names = ", ".join([kid.user.get_full_name()
                              for kid in kids if kid.user])
        return f"{kids.count()} kids: {kid_names}"
    get_children_info.short_description = 'Children Info'


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'user_type', 'get_related_info')

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'

    def get_related_info(self, obj):
        if obj.user_type == 'student':
            return f"Roll Number: {obj.student.roll_number}"
        elif obj.user_type == 'parent':
            kids = Student.objects.filter(parent__user=obj)
            kid_names = ", ".join([kid.user.get_full_name()
                                  for kid in kids if kid.user])
            return f"{kids.count()} kids: {kid_names}"
    get_related_info.short_description = 'Related Info'


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'gender',
                    'get_subjects_taught', 'get_email', 'get_phone')

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else None
    get_full_name.short_description = 'Teacher Name'

    def get_subjects_taught(self, obj):
        return ", ".join([subject.subject_name for subject in obj.subjects_taught.all()])
    get_subjects_taught.short_description = 'Subjects Taught'

    def get_email(self, obj):
        return obj.user.email if obj.user else None
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.user.phone if obj.user else None
    get_phone.short_description = 'Phone'


class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'grade_level',
                    'homeroom_teacher', 'get_subjects')

    def get_subjects(self, obj):
        return ", ".join([subject.subject_name for subject in obj.subjects.all()])
    get_subjects.short_description = 'Subjects'


admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
