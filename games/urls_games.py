from django.urls import re_path
from . import views

urlpatterns = [
    re_path('all/', views.show),
    re_path('showOne/(?P<video_id>\d+)/$', views.showOneVideo),
    re_path('addcomment/(?P<video_id>\d+)/$', views.addcomment),
    re_path('sign/', views.sign),
    re_path('out/', views.goout),
    re_path('in/', views.goin),
    # re_path('addliketovideo/(?P<video_id>\d+)/$', views.likevideo),
    # re_path('addliketocomment/(?P<comment_id>\d+)/$', views.likecomment),
    re_path('addliketovideo/ajax/', views.ajaxvid),
    re_path('addliketocomment/ajax/', views.ajaxcomm),
]