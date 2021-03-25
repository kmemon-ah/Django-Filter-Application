from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Keyword_Data(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    keyword = models.CharField(max_length=200)
    used = models.CharField(max_length=200)
    search_time = models.DateTimeField(default = timezone.now)
    searched_from = models.CharField(max_length=100)
    searched_via = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.user = self.user.lower()
        self.keyword = self.keyword.lower()
        self.used = self.used.lower()
        self.searched_from = self.searched_from.lower()
        self.searched_via = self.searched_via.lower()
        return super(Keyword_Data,self).save(*args, **kwargs)

    def __str__(self):
        return self.keyword
    




