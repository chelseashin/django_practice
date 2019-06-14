from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
from .models import User


# 회원가입/로그인/Board ... Create
# 1. GET
#     - ModelForm context로 보내기
#     - 지정된 템플릿에 출력하기
#     + post요청이니까 csrf_token
    
# 2. POST
#     - 기존의 코드는 GET만 처리하니까 request.method를 통해 분기
#     - ModelForm으로 데이터 받기(request.POST)
#     - 데이터 검증하기
#         - 통과하면 저장, 
#             - 저장하기 전에 정보 더 추가하려면(user) commit=False
#             - Detail / List(index) 중 하나로 보내주기
#             - 통과하지 못하면

# Create your views here.
def signup(request):
    # if user.is_authenticated():
    #     if user == request.user:
    #         return redirect('posts:list')
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)    # 회원가입과 동시에 로그인 상태로 만들기
            return redirect('posts:list')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form, 
    }
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())    # 중요!
            return redirect('posts:list')
    else: 
        login_form = AuthenticationForm()
    context = {
        'login_form' : login_form
    }
    return render(request, 'accounts/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
#  팔로우
def follow(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if request.user != user:
        if request.user in user.followers.all():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
    return redirect('posts:list')