from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title
