from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('addtask', views.addtask_page, name='addtask_page'),
    path('posttask', views.posttask_page, name='posttask_page'),
    path('taskdetails/<int:pk>/', views.taskdetails_page, name='taskdetails_page'),
    path('deletetask/<int:pk>/', views.deletetask_page, name='deletetask_page'),
    path('closetask/<int:pk>/', views.closetask_page, name='closetask_page'),
]
