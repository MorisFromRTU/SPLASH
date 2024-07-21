from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.models import Article, Comment, ArticleLike
from app.forms import ArticleForm, SearchForm

def articles_page(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query', '')
    if query:
        articles = Article.objects.filter(title__icontains=query) | Article.objects.filter(description__icontains=query)
    else:
        articles = Article.objects.all()

    context = {
        'form': form, 
        'articles': articles
        }
    return render(request, 'articles/articles.html', context)

def article_page(request, id):
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=article)
    context = {
        'article' : article,
        'comments' : comments
    }
    return render(request, 'articles/article.html', context)

@login_required
def article_create_page(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user 
            article.save()
            return redirect(reverse('article_create') + '?success=True')
    else:
        form = ArticleForm()
    
    success = request.GET.get('success', False)
    context = {
        'form': form, 
        'success': success
    }
    return render(request, 'articles/article_create.html', context)

@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = ArticleLike.objects.get_or_create(user=request.user, article=article)
    like.is_like = True
    like.save()
    return redirect('article', id=article_id)

@login_required
def dislike_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = ArticleLike.objects.get_or_create(user=request.user, article=article)
    like.is_like = False
    like.save()
    return redirect('article', id=article_id)

