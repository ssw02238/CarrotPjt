from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'price', 'content', 'image',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'article',)