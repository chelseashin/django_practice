from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
# CRUD 로직
# 1. 사용자의 정보를 받을 수 있도록 한다.
#     - Form을 줘야 하는데,
#     - 옛날에는 <form></form>을 직접 만들어썼지만
#     - 지금은 모델폼을 쓴다!
#     - 그래서 GET 요청으로 들어오면 나는 모델폼을 context에 담아서 보내줘야 한다.

# 2. 사용자가 이제 정보를 보내준다. 
# 이건 POST 요청이다. 그러니까 if를 해야지.
# 사용자의 정보는 request.POST에 담겨있네...
# 모델폼에게 넘겨줘야지.
# 그리고 모델폼은 검증을 해줄거야.. (.is_valid())
# 검증에 통과하면 저장해야 하는데,
# 저장하기 전에 정보가 더 필요하면 commit=False로 잠시 멈춰놓고
# 해당하는 값을 넣고 .save 해줘야지.
# 그리고 상세페이지나 아무데나 보내버리자!

def list(request):
    posts = Post.objects.order_by('-pk')
    context = {
        'posts' : posts,
    }
    return render(request, 'posts/list.html', context)
    
@login_required
def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            # post_form.user = request.user
            post_form.user_id = request.user.id
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
    context = {
        'form' : post_form,
    }
    return render(request, 'posts/form.html', context)
    
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)
    
@login_required
@require_POST
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('posts:list')
    
@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        update_form = PostForm(request.POST, instance=post)
        if update_form.is_valid():
            post = update_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', post.pk)
    else:
        update_form = PostForm(instance=post)
    context = {
        'form' : update_form,
    }
    return render(request, 'posts/form.html', context)
        
@login_required
@require_POST
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post_id = post_pk
            comment.save()
    else:
        comment_form = CommentForm()
    content = {
        'comment_form' : comment_form, 
    }
    return redirect('posts:detail', post_pk)
    
@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('posts:detail', post_pk)
    
# Like

# 1번글에 좋아요를 로그인한 1번 사용자가 눌렀다.
# post = get_object_or_404(Post, pk=post_pk)

# 1번글(post)에 좋아요를 누른 적이 있다면(post.like_users.all())
# 좋아요 취소를 해준다(DB에서 삭제)

# 1번글(post)에 좋아요를 누른 적이 없다면(post.like_users.all())
# 좋아요를 해준다(DB에 추가)

def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
        
    return redirect('posts:list')