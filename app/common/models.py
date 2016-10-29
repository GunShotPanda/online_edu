#!/usr/bin/env python
# coding:utf-8

'''
created on 2016-10-28
@author:linguoyang
Model管理，各个模块和功能点所需要的数据模型,由项目组长统一管理
'''

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from datetime import datetime
from django.core.mail import send_mail

class Ad(models.Model):
    '''
    网站首页的广告
    '''

    title = models.CharField(u"网站广告",max_length=30)
    discription = models.CharField(u"广告描述",max_length=200)
    img = models.ImageField(u'广告图片地址',upload_to='ad/%Y/%m')
    callback_url = models.URLField(u'广告地址',null=True, blank=True)
    index = models.IntegerField(u"广告排序",default=999)

    class Meta:
        verbose_name = u"广告"
        verbose_name_plural = verbose_name
        db_table = 'ad'
        ordering = ['index','id']

    def __unicode__(self):
        return self.title

class UserProfileManager(BaseUserManager):

    '''
    自定义用户管理器
    '''

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        '''
        根据用户名和密码创建一个用户
        '''
        now = datetime.now()
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username,email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, email, password, True, True,
                                 **extra_fields)


# 用户模型
class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''
    继承AbstractBaseUser,扩展用户的功能
    '''

    username = models.CharField(u"昵称", max_length=30, unique=True)
    first_name = models.CharField(u"名字",max_length=30,blank=True)
    last_name = models.CharField(u'姓',max_length=30,blank=True)
    email = models.EmailField(u'邮箱', max_length=100,blank=True, unique=True)
    is_staff = models.BooleanField(u"是否职员", default=False,help_text=u"是否能够登录管理后台")
    is_active = models.BooleanField(u"是否激活",default=True)
    date_joined = models.DateTimeField(u"加入日期",auto_now_add=True)
    avatar_url = models.ImageField(upload_to='avatar/%Y/%m',default="avatar/default_avatar_big.png", max_length=200, null=True, blank=True, verbose_name=u'头像220*220')
    avatar_middle_thumbnall = models.ImageField(upload_to='avatar/%Y/%m',default="avatar/default_avatar_middle.png", max_length=200, null=True, blank=True, verbose_name=u'头像140*140')
    avatar_small_thumbnall = models.ImageField(upload_to='avatar/%Y/%m',default="avatar/default_avatar_small.png", max_length=200, null=True, blank=True, verbose_name=u'头像70*70')
    qq = models.CharField(u"QQ号码", max_length=15, null=True, blank=True, )
    mobile = models.CharField(u"手机号码", max_length=15, null=True, blank=True, )
    valid_email = models.SmallIntegerField(u"是否验证邮箱", default= 0, choices=((0,u"否"),(1,u"是"),))
    company_name = models.CharField(u"公司名",max_length=20, null=True,blank=True)
    position = models.CharField(u'职位名', max_length=15, null=True, blank=True)
    discription = models.TextField(u"个人介绍", null=True, blank=True)
    city = models.CharField(u'城市',max_length=8, null=True,blank=True)
    province = models.CharField(u'省份',max_length=8, null=True,blank=True)
    index = models.IntegerField(u"排列顺序(从小到大)", null=True, blank=True, default=999)
    # mylesson = models.ManyToManyField(Lesson, through="UserLearningLesson", verbose_name="我学习的章节")
    # mystage = models.ManyToManyField(Stage, through="UserUnlockStage", verbose_name=u"已解锁的阶段")
    # myfavorite = models.ManyToManyField(Course, through="UserFavoriteCourse",verbose_name=u"我收藏的课程")

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name
        db_table = 'user_profile'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        'Returns the short name for the user.'
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 是否是老师
    def is_teacher(self):
        if self.groups.filter(name='老师').count() > 0 :
            return True
        return False

    # 是否是学生
    def is_student(self):
        if self.groups.filter(name='学生').count() > 0 :
            return True
        return False

    def __unicode__(self):
        return self.username


class KeyWord(models.Model):
    '''
    关键字
    '''
    name = models.CharField(u"关键字",max_length=10,unique=True)

    class Meta:
        verbose_name = u"关键字"
        verbose_name_plural = verbose_name
        db_table = 'keywords'

    def __unicode__(self):
        return self.name

class Article(models.Model):
    '''
    文章
    '''

    ACTIVITY = 'ACTIVITY'
    NEWS = 'NEWS'
    DISCUSS = 'DISCUSS'

    TYPES = (
        (ACTIVITY,'官方活动'),
        (NEWS,'新闻咨询'),
        (DISCUSS,'技术交流'),
    )

    title = models.CharField(u"标题",max_length=30,)
    type = models.CharField(u"文章类型",max_length=8, choices=TYPES,default=ACTIVITY)
    data_publish = models.DateTimeField(u"发布时间",auto_now_add=True)
    is_active = models.BooleanField(u"是否发布",default=True)
    content = models.TextField(u"文章内容",null=True,blank=True)
    article_keywords = models.ManyToManyField(KeyWord)

    class Meta:
        verbose_name = u"文章"
        verbose_name_plural = verbose_name
        db_table = 'article'

    def __unicode__(self):
        return self.title
