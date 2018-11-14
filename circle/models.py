from django.db import models


class Post(models.Model):
    user_id = models.IntegerField()
    nick_name = models.CharField(max_length=20)
    content = models.TextField()
    picture = models.FileField()
    pub_time = models.DateTimeField()
    display = models.BooleanField()


class CircleUser(models.Model):
    pass


