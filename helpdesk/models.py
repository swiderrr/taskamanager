from django.db import models
from datetime import datetime


PRIORITY_CHOICES = (
    ('Niski','Niski'),
    ('Normalny', 'Normalny'),
    ('Wysoki','Wysoki'),
)

STATUS_CHOICES = (
    ('Stworzono','Stworzono'),
    ('W trakcie','W trakcie'),
    ('Częściowo rozwiązany', 'Częściowo rozwiązany'),
    ('Rozwiązany','Rozwiązany'),
    ('Zamknięty','Zamknięty'),
)




class Task(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    desc = models.TextField(max_length=1000, null=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Niski', null=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Stworzono', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def publish(self):
        self.save()

    def task_started(self):
        self.status = 'W trakcie'
        return self.save()


    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.save()

