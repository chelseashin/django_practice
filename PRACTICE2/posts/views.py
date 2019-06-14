from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def list(request):
    posts = Post.objects.order_by('-pk')
    context = {
        'posts' : posts, 
    }
    return render(request, 'posts/list.html', context)
    
@require_POST
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user.id
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    context = {
        'form' : form, 
    }
    return render(request, 'posts/forms.html', context)
    
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form' : comment_form, 
    }
    return render(request, 'posts/detail.html', context)
    
@login_required
@require_POST
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 포스트 유저만 삭제 가능
    # if post.user != request.user:
    #     return redirect('posts:list')
    if post.user == request.user:
        post.delete()
    return redirect('posts:list')
    
@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    # 포스트 유저만 수정 가능
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)
    context = {
        'form' : post_form, 
    }
    return render(request, 'posts/forms.html', context)
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:list')
    
@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post_id = post_pk
            comment.save()
            return redirect('posts:detail', post.pk)
    else:
        comment_form = CommentForm()
    context = {
        'comment_form' : comment_form, 
    }
    return redirect('posts:detail', post_pk)
    
@login_required
@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('posts:detail', post_pk)