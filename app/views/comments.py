from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Comment, Article
from app.models import Article, Comment, CommentLike

@login_required
def create_comment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(article=article, text=text, user=request.user)
        return redirect('article', id=id)
    
    return redirect('article', id=id)

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