from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    details = models.TextField()
    # auto add now add the date a new instance is created
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
