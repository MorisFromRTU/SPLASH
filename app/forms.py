from django import forms
from .models import Article, CustomUser, Message

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description']
        
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите запрос'})
    )

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        label='Никнейм', 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль', 
        required=True)
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Подтвердите пароль', 
        required=True)
    

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        label='Никнейм', 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль', 
        required=True)
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите сообщение...', 'rows': 3, 'style': 'resize:none;'}),
        }
