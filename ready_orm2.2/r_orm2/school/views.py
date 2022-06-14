from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    school_one = Student.objects.all()
    context = {'object_list': school_one}

    ordering = 'group'

    return render(request, template, context)
