"""
URL configuration for socialnet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('shorts-list/', shorts,  name='shorts-list'),
    path('shorts-list-cbv/', ShortsListView.as_view(), name='shorts-list-cbv'),
    path('shorts-filter/', ShortsFilterView.as_view(), name='shorts-filter'),
    path('short-cbv/<int:pk>', ShortDetailView.as_view(), name='shorts-info-cbv'),
    path('short-info/<int:id>', short_info, name='short-info'),
    # то что мы тут передаем должно быть идентичным в <a href="">
    # <a href="{% url 'short' short.id %}" вместо <int:id> прописываем short.id
    # short_info - это функция(обработчик)
    path('contact/', contacts),
    path('about_us/', about_us),
    path('post/<int:id>', post_detail, name='post-detail'),
    path('post-cbv/<int:pk>', PostDetailView.as_view(), name='post-detail-cbv'),
    path('posts-list-cbv/', PostsListlView.as_view(), name='posts-list-cbv'),
    path('posts-filter/', PostsFilterView.as_view(), name='posts-filter'),

    # path('posts-filter/', PostsFilterlView.as_view(), name='posts-filter'),
    path('saved_posts/', saved_posts_list, name='saved-posts'),
    path('update-short/<int:id>', update_short, name='update-short'),
    path('profile/<int:id>', profile_detail, name='profile'),
    path('add-profile/', add_profile, name='add-profile'),
    path('categories/<int:id>', category_detail),
    path('<int:user_id>/', user_posts, name='user-posts'),
    path('add-post/', create_post, name='add-post'),
    path('update-post/<int:id>', update_post, name='update-post'),
    path('update-comment/<int:id>', update_comment, name='update-comment'),
    path('delete-post/<int:id>/', delete_post, name='delete-post'),
    path('delete-comment/<int:id>/', delete_comment, name='delete-comment'),
    path('make-post/', make_post, name='make-post'),
    path('add-short/', create_short, name='add-short'),
    path('add-saved/', add_saved, name='add-saved'),
    path('remove-saved/', add_delete, name='remove-saved'),
    path('posts/', post_list, name='posts'),
    path('search-cbv/', SearchView.as_view(), name='search-cbv'),
    path('search-result-cbv/', SearchResultView.as_view(), name='search-result-cbv'),
    path('add-subscriber/<int:profile_id>/', subscriber, name='add-subscriber'),
    path('subscribes/<int:user_id>/', SubscribesView.as_view(), name='subscribes'),
    path('unsubscribe/<int:profile_id>/', unsubscribe, name='unsubscribe'),
    path('notification-cbv/', NotificationListView.as_view(), name='notification-cbv'),
    path('update-profile/<int:id>', update_profile, name='update-profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('workers/', WorkersListView.as_view(), name='workers'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('users', include('userapp.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

