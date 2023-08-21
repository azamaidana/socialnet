from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.decorators import login.required
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .models import *
from .forms import CommentForm, ProfileForm, PostForm, UpdateProfileForm


class NoContextView(View):
    template_name = None # required
    def get(self, request):
        return render(request, self.template_name)

class AboutView(NoContextView):
    template_name = 'about.html'

class ContactsView(NoContextView):
    template_name = 'contacts.html'

class WorkersListView(NoContextView):
    template_name = 'worker_lst.html'

class FAQView(NoContextView):
    template_name = 'faq.html'

# class AboutView(View):
#     def get(self, request):
#         return render(request, 'about.html')


def homepage(request):
    context = {}     # это словарь, ключами которого являются название переменных,
                     # в html странице
    context['name'] = 'Aidana'
    posts_list = Post.objects.all()  # Мы получаем список постов с бд(все объекты в бд)                     # SELECT * FROM Post
    context['posts'] = posts_list    # теперь список постов хранится в переменной posts(список объектов)
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

def add_profile(request):
    profile_form = ProfileForm()
    context = {'profile_form': profile_form}

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            return redirect(profile_detail, id=profile_object.id)
        else:
            return HttpResponse("Not valid")

    return render(request, 'add_profile.html', context)

def make_post(request):
    post_form = PostForm()
    context = {'post_form': post_form}

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.creator = request.user
            post_object.save()
            return redirect(post_detail, id=post_object.id)
        else:
            return HttpResponse('Не валидно')
    return render(request, 'making_post.html', context)


def saved_posts_list(request):
    posts = Post.objects.filter(saved_post__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_posts.html', context)

def post_list(request):
    context = {}
    post_list = Post.objects.all()
    context['posts'] = post_list
    return render(request, 'post_list.html', context)

def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id) # select запрос, можно использовать get() метод,
                                          # если знаю что существует только один объект, соответствующий моему запросу
    context['post'] = post_object # один запрос(один пост)
    comment_form = CommentForm()
    context["comment_form"] = comment_form
    comments_list = Comment.objects.filter(post=post_object)
    context['comments'] = comments_list

    if request.method == "GET":
        return render(request, 'post_info.html', context)
    elif request.method == "POST":
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f'{request.user.username} лайкнул ваш пост c id {post_object.id}')
            return redirect(post_detail, id=id)
        elif 'dislike' in request.POST:
            post_object.likes -= 1
            post_object.save()

            Notification.objects.create(
                user=post_object.creator,
                text=f'{request.user.username} дислайкнул ваш пост c id {post_object.id}')
            return redirect(post_detail, id=id)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()

                Notification.objects.create(
                    user=post_object.creator,
                    text=f'{request.user.username} оставил комментарий!')
        return HttpResponse("done")
        #


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

def shorts(request):
    context = {
        'shorts_list': Short.objects.all()
    }
    return render(request, "shorts.html", context)

def short_info(request, id):
    short = Short.objects.get(id=id)
    short.views_qty += 1
    short.viewed_users.add(request.user)
    short.save()
    context = {"short": short}
    return render(request, 'short_info.html', context)

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

    new_notification = Notification(
        user=profile.user,
        text=f'Пользователь {request.user.username} подписался на вас!')
    new_notification.save()
    return redirect(f'/profile/{profile.id}')

def unsubscribe(request,profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.remove(request.user)
    profile.save()
    messages.success(request, "Вы успешно отписались")
    return redirect(f'/profile/{profile.id}')

def notification(request):
    notification_list = Notification.objects.filter(user=request.user)
    for notification in notification_list:
        notification.is_showed = True
    Notification.objects.bulk_update(notification_list, ['is_showed'])
    context = {'notifications': notification_list}
    return render(request, 'notification.html', context)

def update_short(request, id):
    short = Short.objects.get(id=id)
    if request.method == "POST":
        new_description = request.POST['description']
        short.description = new_description
        short.save()
        return redirect(short_info, id=short.id)
    context = {'short': short}
    return render(request, 'update_short.html', context)

def update_post(request,id):
    context = {}
    post_object = Post.objects.get(id=id)


    if request.user != post_object.creator:
        return HttpResponse("нет доступа")

    if request.method == 'POST':
        post_form = PostForm(
            data=request.POST,
            files=request.FILES,
            instance=post_object)

        if post_form.is_valid():
            post_form.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, "Форма не валидна")
            context['post_form'] = post_form
            return render(request, 'update_post.html', context)
    post_form = PostForm(instance=post_object)
    context['post_form'] = post_form
    return render(request, 'update_post.html', context)

def make_post(request):
    post_form = PostForm()
    context = {'post_form': post_form}

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.creator = request.user
            post_object.save()
            return redirect(post_detail, id=post_object.id)
        else:
            return HttpResponse('Не валидно')
    return render(request, 'making_post.html', context)

def update_comment(request, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.created_by:
        messages.warning(request, 'Нет доступа')
        return redirect(post_detail, id=comment.post.id)

    if request.method == "POST":
        comment_form = CommentForm(instance=comment, data=request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return redirect(post_detail, id=comment.post.id)

    comment_form = CommentForm(instance=comment)
    context = {'comment_form': comment_form}
    return render(request, "update_comment.html", context)


def delete_comment(request,id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.created_by:
        return HttpResponse("нет доступа")

    comment.delete()
    return redirect(post_detail, id=comment.post.id)




def delete_post(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.creator:
        return HttpResponse("нет доступа")

    post.delete()
    return redirect(homepage)

def update_comment(request, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.created_by:
        messages.warning(request, 'Нет доступа')
        return redirect(post_detail, id=comment.post.id)

    if request.method == "POST":
        comment_form = CommentForm(instance=comment, data=request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return redirect(post_detail, id=comment.post.id)

    comment_form = CommentForm(instance=comment)
    context = {'comment_form': comment_form}
    return render(request, "update_comment.html", context)
def update_profile(request, id):
    profile = Profile.objects.get(id=id)

    if request.method == 'POST':
        profile_form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(profile_detail, id=profile.id)

    profile_form = ProfileForm(instance=profile)
    context = {'profile_form': profile_form}
    return render(request, 'update_profile.html',context)



def contacts():
    return HttpResponse('Наши контакты!')

def about_us():
    return HttpResponse('Информацмя о нас!')


