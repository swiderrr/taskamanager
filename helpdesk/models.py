from django.db import models
from datetime import datetime
import boto3
from django.conf import settings
from django.contrib.auth.models import User
from dotenv import load_dotenv

load_dotenv()

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

    def task_delete(self):
        return self.delete()

    def status_closed(self):
        self.status = 'Zamknięty'
        return

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def publish(self):
        self.save()

    def comment_delete(self):
        return self.delete()


class Picture(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/', null=False)

    def convert_file_to_path(self, fileObj):
        media_root = 'https://helpdeskpvpl.s3.eu-central-1.amazonaws.com/media/'
        try:
            file_path = fileObj.url
            file_path = file_path.split('/')
            self.file = media_root + file_path[-1]
        except ValueError:
            print('Błąd')



    def picture_delete(self):
        client = boto3.client('s3')
        bucket = os.getenv("DB_NAME")
        path = self.file.url.split('/')[-2:]
        path = '/'.join(path)
        print(path)
        client.delete_object(Bucket=bucket, Key=path)


    def publish(self):
        self.save()

