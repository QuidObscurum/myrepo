from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Video(models.Model):
    class Meta:
        db_table = 'Video'

    Video_url = models.URLField()
    Video_name = models.CharField(max_length=200)
    Video_discr = models.TextField()
    Video_date = models.DateTimeField(auto_now_add=True)
    Video_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.Video_name

class Comment(models.Model):
    class Meta:
        db_table = 'Comment'

    Comment_text = models.TextField()
    Comment_data = models.DateTimeField(auto_now_add=True)
    Comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    Comment_likes = models.IntegerField(default=0)


# Create your models here.
