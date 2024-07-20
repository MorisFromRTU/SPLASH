from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from app.models import Article, Comment, ArticleLike, CommentLike, CustomUser, Chat, Message
from .forms import ArticleForm, SearchForm, RegistrationForm, LoginForm, UserProfileForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.serializers import serialize
import random


def index_page(request):
    context = {

    }
    return render(request, 'index.html', context)


def time_page(request):
    date, time = str(datetime.now()).split()
    time = str(time).split('.')[0]
    context = {
        'date' : date,
        'time' : time
    }
    return render(request, 'time.html', context)

def shop_page(request):
    products = ['помидоры', 'огурцы','перец','яблоки','виноград']
    context = {
        'products' : products
    }
    return render(request,'shop.html' ,context)

adjectives = ["Удивительный", "Инновационный", "Превосходный", "Интригующий", "Загадочный", "Невероятный"]
nouns = ["Метод", "Подход", "Анализ", "Обзор", "Тренд", "Проект"]
topics = ["Искусственного Интеллекта", "Машинного Обучения", "Больших Данных", "Кибербезопасности", "Веб Разработки", "Анализа Данных"]

first_names = ["Алексей", "Мария", "Иван", "Екатерина", "Дмитрий", "Анна", "Сергей", "Наталья"]
last_names = ["Иванов", "Петрова", "Сидоров", "Смирнова", "Кузнецов", "Попова", "Васильев", "Михайлова"]

def generate_article_title():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    topic = random.choice(topics)
    return f"{adjective} {noun} в области {topic}"

def generate_author_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def create_random_article(request):
    title = generate_article_title()
    description = random.randint(0, 100)
    author = generate_author_name()
    new_article = Article(title = title, description = description, author = author)
    new_article.save()

    context = {
        'article' : new_article
    }
    return render(request, 'new_article.html', context)
    

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
    return render(request, 'articles.html', context)

def article_page(request, id):
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=article)
    context = {
        'article' : article,
        'comments' : comments
    }
    return render(request, 'article.html', context)

def delete_articles(request):
    Article.objects.all().delete()
    articles = Article.objects.all()
    context = {
        'articles' : articles
    }
    return render(request, 'articles.html', context)

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
    return render(request, 'article_create.html', context)

@login_required
def create_comment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(article=article, text=text, user=request.user)
        return redirect('article', id=id)
    
    return redirect('article', id=id)

def register_page(request):
    unavailable = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user, created = CustomUser.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                return redirect('login') 
            else:
                unavailable = True    
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'unavailable' : unavailable
    }
    return render(request, 'registration.html', context)

def login_page(request):
    context = {
        'form' : LoginForm()
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
        else:
            context = {
                'form' : form
            }
    return render(request, 'login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')


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

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    like.is_like = True
    like.save()
    return redirect('article', id=comment.article.id)

@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    like.is_like = False
    like.save()
    return redirect('article', id=comment.article.id)

@login_required
def personal_page(request):
    user = CustomUser.objects.get(id=request.user.id) 
    context = {
        'user': user
        }
    return render(request, 'personal_page.html', context)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            user.profile_picture = form.cleaned_data['profile_picture']
            user.save()
            return redirect(f'/users/{user.id}')
    else:
        form = UserProfileForm()
    user = CustomUser.objects.get(id=request.user.id)
    is_own = user == request.user    
    context = {
        'form': form,
        'is_own_profile': is_own,
    }
    return render(request, 'personal_page.html', context)

@login_required
def get_all_users(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query', '')
    if query:
        users = CustomUser.objects.filter(username__icontains=query)
    else:
        users = CustomUser.objects.all()
    context = {
        'users': users,
        'form' : form
        }
    return render(request, 'users.html', context)

@login_required
def get_user(request, id):
    user_page = CustomUser.objects.get(id=id)
    user = request.user
    is_own = user_page == user
    context = {
        'user_page': user_page,
        'is_own_profile': is_own,
        'user' : user,
    }
    return render(request, 'personal_page.html', context)

@login_required
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
    return render(request, 'articles.html', context)

@login_required
def get_or_create_chat(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    
    return redirect('chat_detail', chat_id=chat.id)

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('main')
    
    messages = chat.messages.all().order_by('timestamp') 
    receiver = chat.participants.exclude(id=request.user.id).first()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()
    
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages, 'form': form, 'receiver' : receiver})
