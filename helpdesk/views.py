from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from helpdesk.models import Task
from .forms import TaskForm
from datetime import datetime, timezone
from django.contrib.auth.models import User


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
        task_list = Task.objects.all()
        a_time = datetime.now(timezone.utc)
        print(a_time)
        return render(request, 'home_page.html', {'task_list': task_list,
                                                  'a_time': a_time,})
    else:
        return redirect('login_page')

def logout_page(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany")
    return redirect('home_page')

def addtask_page(request):
    form = TaskForm()
    return render(request, 'addtask_page.html', {'form':form})

def posttask_page(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
        # author = request.user
        # title = request.POST.get('title')
        # desc = request.POST.get("desc")
        status = 'Created'
        # priority = request.POST.getlist('priority')
        # new_task = Task.objects.create(author=author, title=title, desc=desc, priority=priority)
        return render(request, 'home_page.html')
    else:
        message = "Nie udało się dodać pliku"
        return render(request, "login_page.html", {'message': message})