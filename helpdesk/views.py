from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from helpdesk.models import Task, Comment
from .forms import TaskForm, CommentForm
from datetime import datetime, timezone
from django.shortcuts import render, get_object_or_404


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
            task_list = Task.objects.all()
        else:
            task_list = Task.objects.filter(author=request.user)
        a_time = datetime.now(timezone.utc)
        statuses = {'Stworzono': 'primary',
                    'W trakcie': 'secondary',
                    'Częściowo rozwiązany': 'warning',
                    'Rozwiązany': 'success',
                    'Zamknięty': 'danger', }
        priority_dict = {'Niski': 'success',
                    'Normalny': 'warning',
                    'Wysoki': 'danger'}
        return render(request, 'home_page.html', {'task_list': task_list,
                                                  'a_time': a_time,
                                                  'statuses': statuses,
                                                  'priority_dict': priority_dict})
    else:
        return redirect('login_page')


def logout_page(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany")
    return redirect('home_page')


def addtask_page(request):
    task_form = TaskForm()
    return render(request, 'addtask_page.html', {'task_form': task_form})

def deletetask_page(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.task_delete()
    return redirect('home_page')

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
    task = get_object_or_404(Task, pk=pk)
    a_time = datetime.now(timezone.utc)
    comment_form = CommentForm()
    comments_list = Comment.objects.filter(task_id=pk)
    return render(request, 'helpdesk/taskdetails_page.html', {'task': task,
                                                              'a_time': a_time,
                                                              'comment_form': comment_form,
                                                              'comments_list': comments_list})

def postcomment_page(request, pk):
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        task = Task.objects.get(pk=pk)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = task
            comment.save()
            task.task_started()
        return redirect(request.META['HTTP_REFERER'])
    else:
        message = "Nie udało się dodać komentarza"
        return redirect("taskdetails_page.html", {'message': message})