from django.contrib import admin
from .models import Article, Comment, Hashtag
# Register your models here.


admin.site.register(Hashtag)
admin.site.register(Article)
admin.site.register(Comment)
