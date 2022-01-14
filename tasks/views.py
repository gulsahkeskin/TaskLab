from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

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
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'tasks/loginuser.html',
                          {'form': AuthenticationForm(), 'error': "username and password do not match!"})
        else:
            login(request, user)
            return redirect('current_tasks')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


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
    return render(request, 'tasks/current.html', {'tasks': tasks})


@login_required
def view_tasks(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'tasks/view_tasks.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('current_tasks')
        except ValueError:
            return render(request, 'tasks/view_tasks.html', {'form': TaskForm(), 'error': "something's wrong"})


@login_required
def complete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('completed')


@login_required
def list(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('completed-list')


@login_required
def completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks/completed.html', {'tasks': tasks})


@login_required
def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('current_tasks')
