from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        # required = False, 
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목',
                'maxlength': 10,
                # 'required': False, # 안됨...
            }
        ),
         error_messages={
            'required': '제목이 유효하지 않습니다.',
        }
    )

    price = forms.IntegerField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '가격',
                # 'required': False,
            }
        ),
        error_messages={
            'required': '가격이 유효하지 않습니다.',
        }
    )

    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용',
                # 'required': False,
            }
        ),
        error_messages={
            'required': '내용이 유효하지 않습니다.',
        }
    )

    class Meta:
        model = Article
        fields = ('title', 'price', 'content', 'image',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'article',)