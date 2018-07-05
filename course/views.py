import json

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, CreateView,DeleteView
from django.views.generic.base import TemplateResponseMixin

from course.forms import CreateCourseForm, CreateLessonForm
from .models import Course, Lesson

class AboutView(TemplateView):
    template_name = "course/about.html"


class CourseListView(ListView):
    model = Course#取得数据表中的所有数据
    context_object_name = 'courses'
    template_name = 'course/course_list.html'

class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)

class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"



class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'



class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})

class DeleteCourseView(DeleteView):
    template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")
    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login/"

    def get(self, request , *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request, "course/manage/create_lesson.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        students = course.student.all()
        return self.render_to_response({'course':course,'students':students})


class DetailLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return self.render_to_response({"lesson":lesson})

class StudentListLessonView(ListLessonsView):
    template_name = "course/slist_lessons.html"

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.student.add(self.request.user)
        # course.student.remove(self.request.user)
        return HttpResponse("ok")

@login_required(login_url="/account/login")
def enrolled_courses_manage(request,user_id):
    # print(user_id)
    enrolled_courses = Course.objects.filter(student=user_id)
    return render(request,"course/manage/manager_enrolled_courses_list.html",{'enrolled_courses':enrolled_courses})

@csrf_exempt
@require_POST
def drop_out_of_course(request,course_id):
        course = Course.objects.get(id = course_id)
        course.student.remove(request.user)
        return HttpResponse("1")