from django.contrib import admin
from .models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')  
    search_fields = ('title', 'content') 
    list_filter = ('published_date',) 
    fields = ('title', 'content', 'author') 

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'text')
    search_fields = ('text',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
