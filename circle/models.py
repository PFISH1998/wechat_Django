# -*- coding: utf-8 -*-

from django.db import models


# 圈子 model
class Post(models.Model):
    # 发布的用户昵称
    uid = models.ForeignKey('CircleUser', on_delete=models.DO_NOTHING)
    # 内容
    content = models.TextField()
    # 发布图片
    picture = models.TextField(null=True, blank=True)
    # 发布时间
    pub_time = models.DateTimeField(auto_now_add=True)
    # 类型
    type = models.CharField(choices=(
        ('normal', '普通'),
        ('top', '置顶'),
        ('note', '通知')), default='normal', max_length=30)

    display = models.BooleanField(default=True)
    # 点赞数
    like_count = models.IntegerField(default=0)

    dis_like_count = models.IntegerField(default=0)
    # 评论数
    comments_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-pub_time']

    def increase_comments(self):
        self.comments_count += 1
        self.save(update_fields=['comments_count'])

    def change_like(self, s):
        self.like_count += 1 if s else -1  # 根据s与否 三元运算
        self.save(update_fields=['like_count'])


# 圈子用户表
class CircleUser(models.Model):
    uid = models.CharField(max_length=100, primary_key=True)
    # 昵称
    nick_name = models.CharField(max_length=120, null=True, blank=True)
    # 微信用户名
    we_name = models.CharField(max_length=120, null=True, blank=True)
    # 头像
    head_pic = models.CharField(max_length=500, null=True, blank=True)
    # 自我描述
    description = models.CharField(max_length=500, null=True)
    # 展示状态
    display = models.BooleanField(default=True)
    # 用户类型
    type = models.CharField(default='normal',
                            choices=(('normal', '普通'),
                                     ('super', '超级用户'),
                                     ('admin', '管理员')), max_length=120)
    # 是否为活动用户
    is_active = models.BooleanField(default=True)
    # 注册时间
    date_join = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    # 后台备注
    remark = models.CharField(null=True, blank=True, max_length=200)
    gender = models.CharField(max_length=20, null=True, blank=True)


# 评论表
class Comments(models.Model):
    # 被评论的内容
    circle = models.ForeignKey('Post', on_delete=models.DO_NOTHING)
    # 评论内容
    comment_content = models.TextField()
    # 评论时间
    pub_time = models.DateTimeField(auto_now_add=True)
    # 评论人
    from_user = models.ForeignKey('CircleUser', on_delete=models.DO_NOTHING, null=True)
    # 是否已经提醒
    is_view = models.BooleanField(default=False)
    display = models.BooleanField(default=True)
    # display = models.ForeignKey(to='Post', to_field='display')
    # replay_user = models.OneToOneField()
    # view = models


# 点赞表
class Like(models.Model):
    # 点赞对象的 ID
    post = models.ForeignKey('Post', on_delete=models.DO_NOTHING)
    # 点赞对象类型
    type = models.IntegerField(choices=((1, '圈子'), (2, '评论')))
    # 点赞人
    uid = models.ForeignKey('CircleUser', on_delete=models.DO_NOTHING)
    # 点赞状态，是否取消
    status = models.BooleanField()
    # 点赞时间
    like_time = models.DateTimeField(auto_now_add=True)

    def __bool__(self):
        return self.status







