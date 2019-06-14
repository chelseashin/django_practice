from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
# 회원가입
def signup(request):
    # 나중에 구현
    if request.user.is_authenticated:
        return redirect('boards:index')
    
    # 먼저 구현하고
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            form.save()
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {'form': form,}
    return render(request, 'accounts/signup.html', context)
    
# 로그인
def login(request):
    # 나중에 구현
    if request.user.is_authenticated:
        return redirect('boards:index')
        
    # 먼저 구현하고
    if request.method == "POST":
       # Authentication은 DB가 아닌 Session으로 관리하기 때문에 request를 가장 먼저 인자로 받음
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # DB에 저장하는 것이 아니라 Session에 저장
            auth_login(request, form.get_user())
            return redirect('boards:list')
    else:
        form = AuthenticationForm()
    context = {'form' : form, }
    return render(request, 'accounts/login.html', context)
 
# 로그아웃   
def logout(request):
    auth_logout(request)
    return redirect('boards:list')
    
# 인스턴스 요소는 항상 마지막에 있음
# usercreationform의 아빠는 modelform이고, 인자 : request.POST, request.FILES ... instance
# 데이터 베이스에 저장
# authentication의 아빠는 django 인자 : request, request.POST, ... instance
# 세션에 저장