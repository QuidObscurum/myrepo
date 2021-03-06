from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Video, Comment
from . import form
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import get_user_model, login, logout
from django.db.models import Count

User = get_user_model()

def redirect_to_valid_url(request):
    return redirect("/games/all/")

def show(request):
    content = []
    for v in Video.objects.all():
        tmp = []
        l_videos = []
        l_videos.append(v)
        l_videos.append(len(v.Video_likers.all()))
        tmp.append(l_videos)
        # comments = Comment.objects.filter(Comment_video_id=v.id)
        comments_set = Comment.objects.filter(Comment_video_id=v.id) \
            .annotate(likes_count=Count('Comment_likers')) \
            .order_by('-likes_count')[:2]
        l_users = []
        l_comment_likes = []
        for com in comments_set:
            comment_likes_len = len(com.Comment_likers.all())
            l_comment_likes.append(comment_likes_len)
            l_users.append(User.objects.get(id=com.Comment_user_id))
        tmp.append(list(zip(comments_set, l_users, l_comment_likes)))

        content.append(tmp)
    # <content>[
    #   <tmp>[
    #       <videos>[video, Likes], <comms>[(Comment, User, Likes),(Comment, User, Likes)...]]]
    return render(request, 'dj_template.html', {'content': content, 'user': auth.get_user(request).username})
    # return render(request, 'dj_template.html', {'name': 'Diana'})
    # return HttpResponse('Hello')


def showOneVideo(request, video_id):
    kargs = {}
    kargs.update(csrf(request))  # TOKEN
    kargs['form'] = form.CommentForm
    video = Video.objects.get(id=video_id)
    kargs['video'] = video
    kargs['video_likes'] = len(video.Video_likers.all())
    kargs['user'] = auth.get_user(request).username
    comments = Comment.objects.filter(Comment_video_id=video_id)
    Users_list = []
    l_comment_likes = []
    for com in comments:
        comment_likes_len = len(com.Comment_likers.all())
        l_comment_likes.append(comment_likes_len)
        Users_list.append(User.objects.get(id=com.Comment_user_id))
    kargs['comments'] = list(zip(comments, Users_list, l_comment_likes))
    return render(request, 'oneVideo.html', kargs)


def addcomment(request, video_id):
    if request.POST:  # реквест - словарь элементов гет и элементов пост
        forma = form.CommentForm(request.POST)  # здесь словарь. форму заполнил юзер, она оделась в токен и приехала
        if forma.is_valid():
            comment = forma.save(commit=False)
            comment.Comment_video = Video.objects.get(id=video_id)
            comment.Comment_user = User.objects.get(id=request.user.id)
            forma.save()
    return redirect("/games/showOne/" + str(video_id) + "/")


def sign(request):
    if request.POST:

        user = User.objects.create_user(username=request.POST.get('username', ''),
                                        email=request.POST.get('email', ''),
                                        password=request.POST.get('password', ''))
        if user:
            login(request, user)

        return redirect("/games/all/")
    else:
        kargs = {}
        kargs.update(csrf(request))  # TOKEN
        kargs['user'] = ''
        kargs['form'] = form.UserForm
        kargs['url'] = '/games/sign/'
        return render(request, 'sign.html', kargs)


def goout(request):
    logout(request)
    return redirect("/games/all/")


def goin(request):
    if request.POST:
        user = auth.authenticate(username=request.POST.get('username', ''),
                                 password=request.POST.get('password', ''))

        if user:
            login(request, user)
            return redirect("/games/all/")

        else:
            kargs = {}
            kargs.update(csrf(request))  # TOKEN
            kargs['form'] = form.UserFormL
            kargs['user'] = auth.get_user(request).username
            kargs['url'] = '/games/in/'
            kargs['error'] = 'No such user'
            return render(request, 'sign.html', kargs)
    else:
        kargs = {}
        kargs.update(csrf(request))  # TOKEN
        kargs['form'] = form.UserFormL
        kargs['user'] = auth.get_user(request).username
        kargs['url'] = '/games/in/'
        return render(request, 'sign.html', kargs)


# def likevideo(request, video_id):
#     video = Video.objects.get(id=video_id)
#     # kargs['user'] = User.objects.get(id=request.user.id)
#     video.Video_likes += 1
#     video.save()
#     return redirect("/games/showOne/" + str(video_id) + "/")

# def likecomment(request, comment_id):
#     comment = Comment.objects.get(id=comment_id)
#     # kargs['user'] = User.objects.get(id=request.user.id)
#     comment.Comment_likes += 1
#     comment.save()
#     video_id = comment.Comment_video_id
#     return redirect("/games/showOne/" + str(video_id) + "/")

def ajaxvid(request):
    if request.GET:
        video_id = request.GET['addlike']
        video = Video.objects.get(id=video_id)
        liker = User.objects.get(id=request.user.id)
        # video.Video_likes += 1
        if liker in video.Video_likers.all():
            video.Video_likers.remove(liker)
        else:
            video.Video_likers.add(liker)
        video.save()
    return HttpResponse(len(video.Video_likers.all()))

def ajaxcomm(request):
    if request.GET:
        comment_id = request.GET['addlike']
        comment = Comment.objects.get(id=comment_id)
        # comment.Comment_likes += 1
        liker = User.objects.get(id=request.user.id)
        if liker in comment.Comment_likers.all():
            comment.Comment_likers.remove(liker)
        else:
            comment.Comment_likers.add(liker)
        comment.save()
    return HttpResponse(len(comment.Comment_likers.all()))

# Create your views here.
