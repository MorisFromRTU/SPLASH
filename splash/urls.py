from django.contrib import admin
from django.urls import path, include
from app.views.general import index_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_page, name='main'),
    path('admin/', admin.site.urls),
    path('articles/', include('app.urls.articles_urls'), name='articles'),
    path('comments/', include('app.urls.comments_urls'), name='comments'),
    path('users/', include('app.urls.users_urls'), name='users'),
    path('chats/', include('app.urls.chats_urls'), name='chats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)