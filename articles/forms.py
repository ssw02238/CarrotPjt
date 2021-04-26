from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목',
                'maxlength': 10,
            }
        ),
    )

    price = forms.IntegerField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '가격',
            }
        ),
    )

    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용',
            }
        ),
    )

    class Meta:
        model = Article
        fields = ('title', 'price', 'content', 'image',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'article',)