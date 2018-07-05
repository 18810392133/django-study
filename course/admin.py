from django.contrib import admin
from .models import Course,Lesson
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_filter = ('user','created')
    list_display = ('user','title','created')
admin.site.register(Course,CourseAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title','video','attach')
    list_filter = ('title','video','attach')

admin.site.register(Lesson,LessonAdmin)