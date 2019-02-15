from django.db import models


class IndexPictures(models.Model):
    pic_url = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    date = models.DateTimeField()
    mark = models.CharField(max_length=50)






