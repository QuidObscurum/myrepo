from django.contrib import admin
from .models import Video, Comment

class VideoInline(admin.StackedInline):
    model = Comment
    readonly_fields = ['Comment_likers']
    extra = 2

class VideoAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    list_filter = ['Video_date']
    readonly_fields = ['Video_likers']

admin.site.register(Video, VideoAdmin)


# Register your models here.
