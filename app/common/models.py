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
from django.conf import settings

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

class RecommendKeyword(models.Model):

    name = models.CharField(u"推荐关键字",max_length=10,unique=True)

    class Meta:
        verbose_name = u"推荐关键字"
        verbose_name_plural = verbose_name
        db_table = 'recommend_keyword'

    def __unicode__(self):
        return self.name

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

#友情链接
class Links(models.Model):

    title = models.CharField(u"标题",max_length=50)
    discription = models.CharField(u"描述",max_length=200,null=True,blank=True)
    callback_url = models.URLField(u"链接")
    image = models.ImageField(u"图片路径",upload_to='link/%Y/%m',null=True,blank=True)

    class Meta:
        verbose_name = "友情链接"
        verbose_name_plural = verbose_name
        db_table = "links"

    def __unicode__(self):
        return self.title


#职业课程
class CareerCourse(models.Model):

    name = models.CharField(u"课程名称", max_length=50)
    short_name = models.CharField(u"英文简写", max_length=10,unique=True)
    image = models.ImageField(u"图片",upload_to='course/%Y/%m')
    discription = models.TextField(u"描述")
    student_count = models.IntegerField(u"学生数量",default=0)
    market_page_url = models.URLField(u"营销页面地址",null=True,blank=True)
    total_price = models.DecimalField(u"课程价格",max_digits=7,decimal_places=1,default=0)
    discount = models.DecimalField(u'折扣',default=1,max_digits=3,decimal_places=2)
    click_count = models.IntegerField(u"点击数量",default=0)
    index = models.IntegerField(u"排序",default=999)
    search_keywords = models.ManyToManyField(KeyWord,verbose_name=u"搜索关键字")

    class Meta:
        verbose_name = '职业课程'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        db_table = 'career_course'

    def __unicode__(self):
        return self.name

#课程阶段
class Stage(models.Model):

    name = models.CharField(u"阶段名称", max_length=50)
    discription = models.TextField(u"描述",null=True,blank=True)
    index = models.IntegerField(u"顺序",default=999)
    is_try = models.BooleanField(u"是否试学",default=False)
    career_course = models.ForeignKey(CareerCourse,verbose_name=u"职业课程")

    class Meta:
        verbose_name = u'阶段'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'stage'

    def __unicode__(self):
        return self.name



#课程
class Course(models.Model):

    name = models.CharField(u"课程名称", max_length=50)
    image = models.ImageField(u"课程图片",upload_to="course/%Y/%m")
    discription = models.TextField(u"描述", null=True, blank=True)
    index = models.IntegerField(u"顺序", default=999)
    is_active = models.BooleanField(u"是否激活",default=True)
    date_publish = models.DateTimeField(u"发布时间",auto_now_add=True)
    date_update = models.DateTimeField(u"更新时间",auto_now=True)
    need_days = models.IntegerField(u"学习时间/h",default=5)
    need_days_base = models.IntegerField(u"有基础的学习时间/h",default=3)
    student_count = models.IntegerField(u"学生人数",default=0)
    favorite_count = models.IntegerField(u"收藏数量",default=0)
    click_count = models.IntegerField(u"点击数量",default=0)
    is_voince = models.BooleanField(u"是否新手课程",default=False)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u"授课老师")
    stages = models.ForeignKey(Stage,verbose_name=u"课程阶段",blank=True,null=True)
    search_keywords = models.ManyToManyField(KeyWord,verbose_name=u"小课程搜索关键字")
    is_homeshow = models.BooleanField(u"是否显示首页",default=False)
    is_required = models.BooleanField(u"是否必修",default=True)

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'course'

    def __unicode__(self):
        return self.name

class StageCourse(models.Model):

        stages = models.ForeignKey(Stage)
        courses = models.ForeignKey(Course)

        class Meta:
            verbose_name = u'阶段-课程'
            verbose_name_plural = verbose_name
            ordering = ['id']
            db_table = 'stage_courses'


#视频章节
class Lesson(models.Model):

    name = models.CharField(u"名称", max_length=50)
    video_url = models.CharField(u"视频地址",max_length=200)
    video_length = models.IntegerField(u"视频长度")
    play_count = models.IntegerField(u"播放次数",default=0)
    share_count = models.IntegerField(u"分享次数",default=0)
    index = models.IntegerField(u"播放顺序",default=999)
    is_popup = models.BooleanField(u"是否弹出支付窗口",default=False)
    course = models.ForeignKey(Course,verbose_name=u'课程')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'lesson'

    def __unicode__(self):
        return self.name

#课程资源
class CourseResource(models.Model):

    name = models.CharField(u"名称", max_length=50)
    download_url = models.FileField(u"下载地址", upload_to="course/%Y/%m")
    course = models.ForeignKey(Course,verbose_name=u"课程")

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
        db_table = 'course_resourse'

    def __unicode__(self):
        return self.name

#章节资源
class LessonResource(models.Model):

    name = models.CharField(u"名称", max_length=50)
    download_url = models.FileField(u"下载地址", upload_to="lesson/%Y/%m")
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")

    class Meta:
        verbose_name = u'章节资源'
        verbose_name_plural = verbose_name
        db_table = 'lesson_resourse'

    def __unicode__(self):
        return self.name

#用户管理器
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
    first_name = models.CharField(u"姓",max_length=30,blank=True)
    last_name = models.CharField(u'名字',max_length=30,blank=True)
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
        full_name = '%s%s' % (self.first_name, self.last_name)
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
