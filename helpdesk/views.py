from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from helpdesk.models import Task, Comment, Picture
from .forms import TaskForm, CommentForm, PictureForm
from datetime import datetime, timezone
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.template import RequestContext
import boto3
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

STATUSES_DICT = {'Stworzono': 'primary',
                    'W trakcie': 'secondary',
                    'Częściowo rozwiązany': 'warning',
                    'Rozwiązany': 'success',
                    'Zamknięty': 'danger', }

PRIORITY_DICT = {'Niski': 'success',
                 'Normalny': 'warning',
                 'Wysoki': 'danger'}

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        userAuth = authenticate(username=username, password=password)
        task_list = Task.objects.all()
        a_time = datetime.now()
        if userAuth is not None:
            login(request, userAuth)
            return redirect('/', {'task_list': task_list,
                                  'a_time': a_time})
        else:
            messages.warning(request, 'Logowanie nie powiodło się.')
            return redirect("login_page")
    return render(request, 'login_page.html')


def home_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            task_list = Task.objects.all().order_by('created_at')
        else:
            task_list = Task.objects.filter(author=request.user)
        a_time = datetime.now(timezone.utc)
        return render(request, 'home_page.html', {'task_list': task_list,
                                                  'a_time': a_time,
                                                  'statuses': STATUSES_DICT,
                                                  'priorities': PRIORITY_DICT})
    else:
        return redirect('login_page')


def logout_page(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany")
    return redirect('home_page')


def addtask_page(request):
    task_form = TaskForm()
    picture_form = PictureForm()
    return render(request, 'addtask_page.html', {'task_form': task_form,
                                                 'picture_form': picture_form})

def deletetask_page(pk):
    task = get_object_or_404(Task, pk=pk)
    task.task_delete()
    return redirect('home_page')

def deletecomment_page(request, comm_pk, pk):
    comment = get_object_or_404(Comment, pk=comm_pk)
    task = get_object_or_404(Task, pk=pk)
    comment.comment_delete()
    return redirect(request.META['HTTP_REFERER'])

def closetask_page(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status_closed()
    task.save()
    return redirect(request.META['HTTP_REFERER'])

def posttask_page(request):
    task_form = TaskForm()
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.author = request.user
            task.save()
        status = 'Created'
        return redirect('home_page')
    else:
        message = "Nie udało się dodać pliku"
        return render(request, "login_page.html", {'message': message})


def taskdetails_page(request, pk):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        picture_form = PictureForm(request.POST, request.FILES)
        task = Task.objects.get(pk=pk)
        if comment_form.is_valid():
            print('prawidłowe formy')
            comment = comment_form.save(commit=False)
            picture = picture_form.save(commit=False)
            comment.author = request.user
            comment.task = task
            comment.save()
            task.task_started()
            if picture_form['file'].value() is not None:
                picture.comment = comment
                picture_form.save()
                picture.convert_file_to_path(picture.file)
                picture.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.success(request, ("Wystąpił błąd podczas logowania, spróbuj ponownie."))
    else:
        task = get_object_or_404(Task, pk=pk)
        a_time = datetime.now(timezone.utc)
        comment_form = CommentForm()
        picture_form = PictureForm()
        comments_list = Comment.objects.filter(task_id=pk).order_by('created_at')
        return render(request, 'helpdesk/taskdetails_page.html', {'task': task,
                                                                  'a_time': a_time,
                                                                  'comment_form': comment_form,
                                                                  'picture_form': picture_form,
                                                                  'statuses': STATUSES_DICT,
                                                                  'comments_list': comments_list,})
