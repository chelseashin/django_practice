from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

def signup(request):
    # 나중에 구현
    if request.user.is_authenticated:
        return redirect('posts:list')
    # 먼저 구현
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입 문제
            auth_login(request, user) # 회원가입과 동시에 로그인 상태로 만들기
            return redirect('posts:list')
    else: 
        form = UserCreationForm()
    context = {
        'form' : form, 
    }
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    # 나중에 구현
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user()) # 유저 정보로 로그인
            return redirect('posts:list')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }    
    return render(request, 'accounts/login.html', context)    
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
