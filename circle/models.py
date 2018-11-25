from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):  # 发布圈子
    uid = models.ForeignKey('CircleUser', on_delete=models.CASCADE)  # 发布的用户昵称
    content = models.TextField()  # 内容
    # picture = models.FileField(blank=True, null=True) # 发布图片
    pub_time = models.DateTimeField(auto_now_add=True)  # 发布时间

    type = models.CharField(choices=
                            (('normal', '普通'), ('top', '置顶'), ('note', '通知')),
                            default='normal', max_length=30)   # 类型

    display = models.BooleanField(default=True)
    like_count = models.IntegerField(default=0)  # 点赞数
    dis_like_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)  # 评论数

    class Meta:
        ordering = ['-pub_time']

    def increase_comments(self):
        self.comments_count += 1
        self.save(update_fields=['comments_count'])

    def change_like(self, s):
        self.like_count += 1 if s else -1  # 根据s与否 三元运算
        self.save(update_fields=['like_count'])


class CircleUser(models.Model):  # 圈子用户表
    uid = models.CharField(max_length=100, primary_key=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=120)  # 昵称
    we_name = models.CharField(max_length=120)  # 微信用户名
    head_pic = models.CharField(max_length=500, null=True, blank=True)  # 头像
    description = models.CharField(max_length=500, null=True)  # 自我描述
    display = models.BooleanField(default=True)  # 展示状态
    type = models.CharField(default='normal',
                            choices=(('normal', '普通'),
                                     ('super', '超级用户'),
                                     ('admin', '管理员')), max_length=120)  # 用户类型
    is_active = models.BooleanField(default=True)  # 是否为活动用户
    date_join = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 注册时间
    last_login = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(null=True, blank=True, max_length=200)  # 后台备注
    gender = models.CharField(max_length=20, null=True, blank=True)


class Comments(models.Model):  # 评论表
    circle = models.ForeignKey('Post', on_delete=models.CASCADE)  # 被评论的内容
    comment_content = models.TextField()  # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    from_user = models.ForeignKey('CircleUser', on_delete=models.SET_NULL, null=True)  # 评论人
    is_view = models.BooleanField(default=False)  # 是否已经提醒




    # display = models.ForeignKey(to='Post', to_field='display')
    # replay_user = models.OneToOneField()
    # view = models



class Like(models.Model):  # 点赞表
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # 点赞对象的 ID
    type = models.IntegerField(choices=(('1', '圈子'), ('2', '评论')))  # 点赞对象类型
    uid = models.ForeignKey('CircleUser', on_delete=models.CASCADE)  # 点赞人
    status = models.BooleanField(default=True)  # 点赞状态，是否取消
    like_time = models.DateTimeField(auto_now_add=True)  # 点赞时间

    def __bool__(self):
        return self.status







