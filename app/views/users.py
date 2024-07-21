from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import CustomUser
from app.forms import RegistrationForm, LoginForm, UserProfileForm, SearchForm

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
    return render(request, 'users/registration.html', context)

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
    return render(request, 'users/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
def personal_page(request):
    user = CustomUser.objects.get(id=request.user.id) 
    context = {
        'user': user
        }
    return render(request, 'users/personal_page.html', context)

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
    return render(request, 'users/personal_page.html', context)

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
    return render(request, 'users/users.html', context)

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
    return render(request, 'users/personal_page.html', context)