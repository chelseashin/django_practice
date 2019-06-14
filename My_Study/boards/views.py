from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Board, Comment
from .forms import BoardForm, CommentForm



# Create your views here.
def list(request):
    boards = Board.objects.order_by('-pk')
    context = {
        'boards' : boards,
    }
    return render(request,'boards/list.html', context)
    
# CREATE - 이 아이가 어떤 방식으로 들어오는지 나누어 form을 먼저 짜고 요청인자 받음. 그다음 유효성 체크하고 
def create(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        # form 유효성 체크(form이 유효한지 체크!)
        if form.is_valid():
            board = form.save()
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm()
    context = {'form' : form}
    return render(request, 'boards/form.html', context)
     
# 로직 상으로 delete와 detail은 같다!
# READ
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    comment_form = CommentForm()
    context = {
        'board' : board,
        'comment_form': comment_form,
    }
    return render(request, 'boards/detail.html', context)
    
# DELETE
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == "POST":
        board.delete()
        return redirect('boards:list')
    else:
        return redirect('boards:detail', board.pk)

# UPDATE   
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        # 기존에 작성했던 내용을 instance에 넣어줌.(수정하기 용이하도록!)
        board_form = BoardForm(request.POST, instance=board)   # 1
        if board_form.is_valid():
            # board = Board()
            # board.title = request.POST.get('title')
            # board.content = request.POST.get('content')
            # === commit=False === 둥둥 떠다니는 user를 board와 함께 저장하기 위해 잠시 묶어 두는 것
            # board.user = request.user
            # board.save()
            
            board = board_form.save(commit=False)    # 2
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.pk)
    else:    # GET 방식
        board_form = BoardForm(instance=board)
    context = {
        'board' : board,
        'board_form': board_form,
    }
    return render(request, 'boards/form.html', context)
 
# User를 불러오는 방식   
# 1. get_user_model() => User (등록된 User모델을 가져옴)
# 2. settings.AUTH_USER_MODEL => 'accounts.User' (스트링 형태의 모델 그대로)

@require_POST
@login_required
def comment_create(request, board_pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.board_id = board_pk
        comment.save()
    return redirect('boards:detail', board_pk)
    
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('boards:detail', board_pk)