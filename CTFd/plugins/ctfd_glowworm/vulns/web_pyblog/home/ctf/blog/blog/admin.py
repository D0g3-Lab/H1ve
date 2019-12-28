from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from blog.models import UserProfile

from blog.models import Tag, Article, Category

admin.site.register(UserProfile)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_time'
    list_display = ('title', 'category', 'author', 'date_time', 'view')
    list_filter = ('category', 'author')
    filter_horizontal = ('tag',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
