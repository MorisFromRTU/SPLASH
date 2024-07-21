from django.urls import path
from app.views.users import (
    login_page, logout_page, register_page, personal_page, 
    upload_profile_picture, get_all_users, get_user
)

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='registration'),
    path('personal/', personal_page, name='personal'),
    path('upload/', upload_profile_picture, name='upload'),
    path('', get_all_users, name='users'),
    path('<int:id>/', get_user, name='user'),
]
