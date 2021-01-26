from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from django.views import View

class Todo_board(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'todo_main/index.html'
        return render(request, template_name)
