from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index_page, name='main'),
    path('admin/', admin.site.urls),
    path('article/<int:article_id>/like/', views.like_article, name='like_article'),
    path('article/<int:article_id>/dislike/', views.dislike_article, name='dislike_article'),
    path('article/<int:id>', views.article_page, name='article'),
    path('article/<int:id>/create_comment/', views.create_comment, name='create_comment'),
    path('article/create/', views.article_create_page, name='article_create'),
    path('articles/', views.articles_page, name='articles'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),
    path('delete/', views.delete_articles),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('random_article/', views.create_random_article),
    path('personal/', views.personal_page, name='personal'),
    path('upload/', views.upload_profile_picture, name='upload'),
    path('reg/', views.register_page, name='registration'),
    path('shop/', views.shop_page, name='shop'),
    path('time/', views.time_page),
    path('users/', views.get_all_users, name='users'),
    path('users/<int:id>', views.get_user, name='user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)