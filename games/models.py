from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AbstractUser

User = get_user_model()

class Video(models.Model):
    class Meta:
        db_table = 'Video'

    Video_url = models.URLField()
    Video_name = models.CharField(max_length=200)
    Video_discr = models.TextField()
    Video_date = models.DateTimeField(auto_now_add=True)
    # Video_likes = models.IntegerField(default=0)
    Video_likers = models.ManyToManyField(User, related_name='Video_likers')
    def __str__(self):
        return self.Video_name

class Comment(models.Model):
    class Meta:
        db_table = 'Comment'

    Comment_text = models.TextField()
    Comment_data = models.DateTimeField(auto_now_add=True)
    Comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # Comment_likes = models.IntegerField(default=0)
    Comment_likers = models.ManyToManyField(User, related_name='Comment_likers')

# class Like(models.Model):
#     class Meta:
#         db_table = 'Like'
#     Liked_Comment = models.ForeignKey(Comment, related_name='Like_Comment')
#     Liked_Video = models.ForeignKey(Video, related_name='Liked_Video')
#     Liker = models.ForeignKey(User, related_name='Liker')
# Create your models here.
