from django.shortcuts import render, redirect
from .models import Friend

# Create your views here.
def index(request):
    friends = Friend.objects.all()
    return render(request, 'friends/index.html', {'friends':friends})
    
def create(request):
    name= request.GET.get('name')
    email=request.GET.get('email')
    birthday=request.GET.get('birthday')
    age=request.GET.get('age')
    friend = Friend(name=name, email=email, birthday=birthday, age=age)
    friend.save()
    return render(request, 'friends/create.html')
    # , {'name'=name, 'email'=email, 'birthday'=birthday, 'age'=age})

def delete(request, pk):
    friend = Friend.objects.get(pk=pk)
    friend.delete()
    return redirect('/friends/')