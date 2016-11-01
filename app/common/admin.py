# coding:utf-8

from django.contrib import admin
from models import *

# Register your models here.

# 设置相关联的字段显示
class CourseInline(admin.TabularInline):
    model = Course
    extra = 3

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 3

class CourseAdmin(admin.ModelAdmin):

    list_display = ('name','index','date_publish','need_days','teacher','stages')
    list_display_links = ('name','stages')
    list_editable = ('index','teacher')

    inlines = [LessonInline]

class StageAdmin(admin.ModelAdmin):
    inlines = [CourseInline]


class LessonAdmin(admin.ModelAdmin):

    list_display = ('name','index')
    list_display_links = ('name',)
    list_editable = ('index',)


admin.site.register(UserProfile)
admin.site.register(Article)
admin.site.register(KeyWord)
admin.site.register(Ad)
admin.site.register(Links)
admin.site.register(CareerCourse)
admin.site.register(Stage,StageAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(RecommendKeyword)
