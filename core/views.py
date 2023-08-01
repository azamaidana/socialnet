from django.shortcuts import render, HttpResponse


def homepage(request):
    return HttpResponse('Hello world!')


def contacts():
    return HttpResponse('Наши контакты!')

def about_us():
    return HttpResponse('Информацмя о нас!')




