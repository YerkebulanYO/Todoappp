from django.shortcuts import render, redirect
from .models import Task

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .forms import RegisterUserForm
from rest_framework import viewsets
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class TaskViewSet(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def list(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return Response({'tasks': tasks, 'template_name': 'tasklist.html'})



def profile(request):
    return render(request, 'base/profile.html')

class testing(ListView):
    template_name = 'base/tasklist.html'
    fields = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        print(**kwargs)
        pass


def completed_delete(request):
    completed_tasks = Task.objects.filter(completed=True)
    completed_tasks.delete()
    return redirect('home')


def task_complete(request, pk):
    task = Task.objects.filter(id=pk)[0]
    task.completed = True
    task.save()
    return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class Login(LoginView):
    template_name = 'base/login_page.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

# def login_user(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#
#         if request.method == 'POST':
#             form = LoginForm(request.POST)
#             if form.is_valid():
#                 username = request.POST.get('username')
#                 password = request.POST.get('password')
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     messages.success(request, 'Login or password is incorrect')
#                     return redirect('login')
#         else:
#             form = LoginForm
#         return render(request, 'base/login_page.html', {'form': form})

# class TaskList(ListView):
#     model = Task
#     context_object_name = 'tasks'
#     template_name = 'base/tasklist.html'
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context)
#         context['tasks'] = context['tasks'].filter(user=self.request.user)
#
#         return context

# @login_required(login_url='login')
# def home(request):
#     form = TaskForm()
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             todo = form.save(commit=False)
#             todo.user = request.user
#             form.save()
#     user = request.user
#     tasks = Task.objects.filter(user=user).order_by('completed')
#     context = {
#         'tasks': tasks,
#         'form': form
#     }
#     return render(request, 'base/tasklist.html', context)

class TaskCreateAndList(LoginRequiredMixin, CreateView, ListView):
    model = Task
    fields = ['title']
    template_name = 'base/tasklist.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateAndList, self).form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     context['tasks'] = context['tasks'].filter(user=self.request.user)
    #
    #     return context







# @login_required(login_url='login')
# def add(request):
#     error = ''
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             todo = form.save(commit=False)
#             todo.user = request.user
#             form.save()
#             return redirect('home')
#         else:
#             error = 'Error'
#
#     form = TaskForm()
#     context = {
#         'form': form,
#         'error': error
#     }
#     return render(request, 'base/tasklist.html', context)


@login_required(login_url='login')
def delete(request):
    task = Task.objects.all()
    task.delete()
    return redirect('home')


class Register(CreateView):
    template_name = 'base/register.html'
    form_class = RegisterUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(Register, self).get(*args, **kwargs)




# def register(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         form = RegisterUserForm()
#         if request.method == 'POST':
#             form = RegisterUserForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('home')
#             # else:
#             #     messages.error(request, form.errors)
#             #     print('akskadk')
#             #     print(form.errors)
#
#         context = {
#             'form': form
#         }
#         return render(request, 'base/register.html', context)
    # def get_success_url(self):
    #     return reverse('home')
    #
    # def get(self, *args, **kwargs):
    #     return self.delete(*args, **kwargs)
