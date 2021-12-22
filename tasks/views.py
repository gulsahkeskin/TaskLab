from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import TaskForm
from .models import Task


def home(request):
    return render(request, 'tasks/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'tasks/signupuser.html', {'form': UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'tasks/signupuser.html', {'form': UserCreationForm(), 'error': "This username "
                                                                                                      "has already "
                                                                                                      "taken. Please "
                                                                                                      "try another "
                                                                                                      "one!"})
        else:
            # Tell the user the passwords didn't match
            return render(request, 'tasks/signupuser.html',
                          {'form': UserCreationForm(), 'error': "Passwords do not match!"})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'tasks/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username= request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request, 'tasks/loginuser.html', {'form': AuthenticationForm(), 'error': "usename and password do not match!"})
        else:
            login(request, user)
            return redirect('current_tasks')


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create.html', {'form': TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
        except ValueError:
            return render(request, 'tasks/create.html', {'form': TaskForm(), 'error': "bad data passed in"})

    return redirect('current_tasks')


@login_required
def current_tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks/current_tasks.html', {'tasks': tasks})
