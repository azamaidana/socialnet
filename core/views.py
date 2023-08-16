from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.decorators import login.required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import CommentForm
def homepage(request):
    context = {}
    context['name'] = 'Aidana'
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    category_list = Category.objects.all()
    context['categories'] = category_list
    short_list = Short.objects.all()
    context['shorts'] = short_list

    return render(request, "home.html", context)


def category_detail(request, id):
    context = {}
    category_object = Category.objects.get(id=id)
    context['category'] = category_object
    return render(request, 'category_detail.html', context)
def profile_detail(request, id):
    context = {}
    profile = Profile.objects.get(id=id)
    context['profile'] = profile
    if request.method == "POST":
        profile.subscribers.add(request.user)
        profile.save()
    return render(request, 'profile_detail.html', context)

def saved_posts_list(request):
    posts = Post.objects.filter(saved_post__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_posts.html', context)

def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context['post'] = post_object
    comment_form = CommentForm()
    context["comment_form"] = comment_form
    comments_list = Comment.objects.filter(post=post_object)
    context['comments'] = comments_list
    if request.method == "GET":
        return render(request, 'post_info.html', context)
    elif request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.post = post_object
            new_comment.save()
            return HttpResponse("done")

def shorts(request):
    context = {
        'shorts_list': Short.objects.all()
    }
    return render(request, "shorts.html", context)

def short_info(request, id):
    context = {}
    short_object = Short.objects.get(id=id)
    context['short'] = short_object
    return render(request, 'short_info.html', context)


def user_posts(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(creator=user)
    context = {
        "user": user,
        "posts": posts
    }
    return render(request, 'user_posts.html', context)

def create_post(request):
    if request.method == "GET":
        return render(request, "create_post_form.html")
    elif request.method == "POST":
        data = request.POST   # Словарь с данными с html
        # print(data)
        new_post = Post()
        new_post.name = data["post_name"]
        new_post.description = data["description"]
        new_post.photo = request.FILES["photo"]
        new_post.creator = request.user
        new_post.save()
        return HttpResponse('done')

def create_short(request):
    if request.method == "GET":
        return render(request, "short_form.html")
    elif request.method == "POST":
        new_short = Short(
            user=request.user,
            video=request.FILES["video_file"]
        )
        new_short.save()
        return redirect('shorts-info', id=new_short.id)

def add_saved(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post, created = SavedPosts.objects.get_or_create(
            user=request.user)
        saved_post.post.add(post_object)
        saved_post.save()
        return redirect('/saved_posts/')


def add_delete(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post = SavedPosts.objects.get(user=request.user)
        saved_post.post.remove(post_object)
        saved_post.save()
        return redirect('/saved_posts/')

def post_list(request):
    context = {}
    post_list = Post.objects.all()
    context['posts'] = post_list
    return render(request, 'post_list.html', context)

def search(request):

    return render(request, 'search.html')

def search_result(request):
    key_word = request.GET["key_word"]
    # posts = Post.objects.filter(name__icontains=key_word)
    posts = Post.objects.filter(
        Q(name__icontains=key_word) |
        Q(description__icontains=key_word))
    context = {"posts": posts}
    return render(request, 'home.html', context)

def subscriber(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.add(request.user)
    profile.save()
    messages.success(request, "Вы успешно подписались")
    return redirect(f'/profile/{profile.id}')

def unsubscribe(request,profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.remove(request.user)
    profile.save()
    messages.success(request, "Вы успешно отписались")
    return redirect(f'/profile/{profile.id}')


def contacts():
    return HttpResponse('Наши контакты!')

def about_us():
    return HttpResponse('Информацмя о нас!')
