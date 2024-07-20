from django.db import models
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    
    @property
    def rating(self):
        article_likes = ArticleLike.objects.filter(article__author=self, is_like=True).count()
        article_dislikes = ArticleLike.objects.filter(article__author=self, is_like=False).count()
        comment_likes = CommentLike.objects.filter(comment__user=self, is_like=True).count()
        comment_dislikes = CommentLike.objects.filter(comment__user=self, is_like=False).count()
        
        return (article_likes - article_dislikes) + (comment_likes - comment_dislikes)

class Article(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def likes_count(self):
        return ArticleLike.objects.filter(article=self, is_like=True).count()

    def dislikes_count(self):
        return ArticleLike.objects.filter(article=self, is_like=False).count()

class ArticleLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'article')

class Comment(models.Model):
    text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')

    class Meta:
        ordering = ['-timestamp'] 

    def __str__(self):
        return self.text[:50]

    def likes_count(self):
        return CommentLike.objects.filter(comment=self, is_like=True).count()

    def dislikes_count(self):
        return CommentLike.objects.filter(comment=self, is_like=False).count()

class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'comment')

class ReputationVote(models.Model):
    user_id = models.IntegerField(default=42)  
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='votes')
    vote = models.IntegerField(choices=[(-1, '-1'), (1, '1')])

