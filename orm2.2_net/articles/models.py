from django.db import models
from django.db.models import ManyToManyField


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = 'title'

    def __str__(self):
        return self.title


class Object(models.Model):
    objects = models.ManyToManyField(Article, related_name='objects', through='Relationship')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'обьект'
        verbose_name_plural = 'обьект'


class Relationship(models.Model):
    obj = models.ForeignKey(Object, on_delete=models.CASCADE)
    art = models.ForeignKey(Article, on_delete=models.CASCADE)
