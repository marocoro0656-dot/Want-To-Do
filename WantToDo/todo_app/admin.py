# todo_app/admin.py
from django.contrib import admin
from .models import Want
@admin.register(Want)
class WantAdmin(admin.ModelAdmin):
    list_display = ('title','user','category','difficulty','deadline','done','updated_at')
    list_filter = ('category','difficulty','done')
    search_fields = ('title',)
