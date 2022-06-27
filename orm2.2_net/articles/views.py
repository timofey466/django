from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    art = Article.objects.all()
    context = {'object_list': art}

    ordering = '-published_at'

    return render(request, template, context)