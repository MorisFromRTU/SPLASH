from django.urls import path
from app.views.comments import like_comment, dislike_comment, create_comment

urlpatterns = [
    path('<int:comment_id>/like/', like_comment, name='like_comment'),
    path('<int:comment_id>/dislike/', dislike_comment, name='dislike_comment'),
    path('article/<int:id>/create_comment/', create_comment, name='create_comment'),
]
