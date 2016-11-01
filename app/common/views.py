#!/usr/bin/env python
# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.query_utils import Q
from models import *
import json

# Create your views here.

def index(request):

    try:

        #最新文章
        articles = Article.objects.all()[0:5]

        #首页广告
        ads = Ad.objects.all()

        #热门课程
        courses = Course.objects.all()[0:8]

        # 名师风采
        teachers = UserProfile.objects.all()
        good_teachers = []
        for teacher in teachers:
            if teacher.is_teacher():
                good_teachers.append(teacher)

        #推荐搜索词
        recommend_keywords = RecommendKeyword.objects.all()

    except Exception as e:
        return render(request,'common/failure.html',({"failure":"查询错误"}))

    return render(request,'common/index.html',locals())

def article(request,id):
    try:
        article = Article.objects.get(pk=id)

    except Article.DoesNotExist:
        return render(request, "failure.html", {"reason": "此文章不存在"})

    return render(request,'common/article.html',locals())

def search_keyword(request):
    try:
        # request.POST.get('')
        word = request.POST.get('word')
        courses = Course.objects.filter(Q(search_keywords__course__name__icontains=word) | Q(name__icontains=word)).distinct().values("id","name")
        # courses = Course.objects.all().values("id","name")
        # career_courses = CareerCourse.objects.filter(search_keywords__contains=word).values("id","name")
    except Exception:
        pass

    result_course = [x for x in courses]

    keywords = {"keywords":result_course,}

    return HttpResponse(json.dumps(keywords))