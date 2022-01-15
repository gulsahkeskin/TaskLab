"""TaskLab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create', views.create_task, name='create'),
    path('current_tasks', views.current_tasks, name='current_tasks'),
    path('task/<int:task_pk>', views.view_tasks, name='view_tasks'),
    path('task/<int:task_pk>/complete_task', views.complete_task, name='complete_task'),
    path('completed/', views.completed, name='completed'),
    path('completed/', TemplateView.as_view(template_name='completed.html'), name='completed'),
    path('list/', views.yourlist, name='yourlist'),
    path('filter/', views.filter, name='filter'),
    path('list/', TemplateView.as_view(template_name='list.html'), name='yourlist'),
    path('task/<int:task_pk>/delete', views.delete_task, name='delete_task'),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
]
