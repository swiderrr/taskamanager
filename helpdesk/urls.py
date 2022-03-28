from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('addtask', views.addtask_page, name='addtask_page'),
    path('posttask', views.posttask_page, name='posttask_page'),
]