from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from wordcloud import WordCloud, STOPWORDS
from .models import Article, Comment, Hashtag, HashtagCloud
from .forms import ArticleForm, CommentForm

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            # hashtag
            for word in article.content.split(): # content 를 공백기준으로 리스트로 변경
                if word[0] == '#': # '#'로 시작하는 요소 선택
                    hashtag, created = Hashtag.objects.get_or_create(content=word) # word(content안에 해시태그)랑 같은 기존 해시태그를 찾으면 기존 객체를, 없으면 새로운 객체를 return
                    article.hashtags.add(hashtag)
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        article.delete()
        return redirect('articles:index')
    return redirect('articles:detail', article_pk)
    

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                article.hashtags.clear() # 해당 article 의 hashtag 전체 삭제
                for word in article.content.split():
                    if word[0] == '#':
                        hashtag, created = Hashtag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:detail', article_pk)    
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article 
            comment.save()
            return redirect('articles:detail', article_pk)
        context = {
            'article': article,
            'comment_form': comment_form,
        }
        return render(request, 'articles/detail.html', context)
    return redirect('accounts:login')


def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', article_pk)


def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        # 하트 취소 
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:detail', article_pk)


def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    articles = hashtag.article_set.order_by('-pk')
    context = {
        'hashtag': hashtag, 
        'articles': articles,
    }
    return render(request, 'articles/hashtag.html', context)
	

def make_cloud(request):
    # 전체 해시태그 받아오기
    hashtags = Hashtag.objects.all()
    text = ''.join([str(i) for i in hashtags])
    # stopwords
    stopwords = set(STOPWORDS)
    stopwords.add('#')
    # 이미지 만들기
    wc = WordCloud(stopwords=stopwords).generate(text)
    image = wc.to_image()
    # PIL 파일을 jpeg 파일로 바꿔서 static 폴더에 저장하기
    image.save(str(settings.STATICFILES_DIRS[2]) + '/articles/cloud.jpeg')
    return render(request, 'articles/wordcloud.html')