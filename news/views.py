from news.models import news
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    articles = news.objects.order_by('-date').values()
    context = {'articles': articles}
    return 'news/base.html', context
