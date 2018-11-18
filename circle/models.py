from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    nick_name = models.ForeignKey(to='CircleUser', to_field='nick_name', on_delete=models.CASCADE)
    content = models.TextField()
    # picture = models.FileField(blank=True, null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=(('normal', '普通'), ('top', '置顶'), ('note', '通知')), default='normal', max_length=30)
    display = models.BooleanField(default=True)
    class Meta:
        pass


class CircleUser(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=120, unique=True)
    we_name = models.CharField(max_length=120)
    head_pic = models.FileField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True)
    display = models.BooleanField(default=True)
    type = models.CharField(default='normal',
                            choices=(('normal', '普通'),
                                     ('super', '超级用户'),
                                     ('admin', '管理员')), max_length=120)
    is_active = models.BooleanField(default=True)
    date_join = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    remark = models.CharField(null=True, blank=True, max_length=200)


class Comments(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    comment_user = models.OneToOneField('CircleUser', on_delete=models.CASCADE)
    # replay_user = models.OneToOneField()
    # view = models






