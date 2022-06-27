from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Object, Relationship, Article


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            var = form.cleaned_data
            if var != Relationship.objects.all():
                raise ValidationError('Тут всегда ошибка')
        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Relationship
    formset = RelationshipInlineFormset


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
