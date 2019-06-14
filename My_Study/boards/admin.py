from django.contrib import admin
from .models import Board, Comment

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', )
admin.site.register(Board, BoardAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'board_id', )
admin.site.register(Comment, CommentAdmin)