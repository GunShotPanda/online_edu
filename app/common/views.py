#!/usr/bin/env python
# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from models import *

# Create your views here.

def index(request):
    articles = Article.objects.all()[0:5]
    ads = Ad.objects.all()
    return render(request,'common/index.html',locals())

def article(request,id):
    try:
        article = Article.objects.get(pk=id)

    except Article.DoesNotExist:
        return render(request, "failure.html", {"reason": "此文章不存在"})


    return render(request,'common/article.html',locals())