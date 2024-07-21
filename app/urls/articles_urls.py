from django.urls import path
from app.views.articles import (
    article_page, article_create_page, articles_page, 
    like_article, dislike_article
)

urlpatterns = [
    path('', articles_page, name='articles'),
    path('create/', article_create_page, name='article_create'),
    path('<int:id>/', article_page, name='article'),
    path('<int:article_id>/like/', like_article, name='like_article'),
    path('<int:article_id>/dislike/', dislike_article, name='dislike_article'),
]
