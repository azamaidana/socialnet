from django.db import models
from django.contrib.auth.models import User
#
class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE)
    nickname = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    subscribers = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='followed_user'
    )

    photo = models.ImageField(
        upload_to='profile.photo/',
        null=True
    )
    link_fb = models.CharField(
        max_length=255, null=True, blank=True
    )
    whatsapp = models.CharField(
        max_length=30, null=True, blank=True
    )
    telegram = models.CharField(
        max_length=55, null=True, blank=True
    )

class Post(models.Model):
    status_choices = (('Published', 'Published'),
                      ('Unpublished', 'Unpublished'))

    name = models.CharField('Заголовок', max_length=80, null=True, blank=True)
    description = models.TextField('Описание', null=True)
    photo = models.ImageField('Фотография', upload_to='photo_post/', null=True, blank=False)
    status = models.CharField('Статус публикации', max_length=200, choices=status_choices,)
    likes = models.PositiveIntegerField('Лайк', default=0)
    # M2O
    creator = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Автор поста",
        related_name="posts"  # default == post_set
    )

    category = models.ManyToManyField(
        to='Category',
        blank=True,
        verbose_name='Категории',
    )


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    def __str__(self):
        return f'{self.name} - {self.status}'

class Category(models.Model):
    rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )
    name = models.CharField('Название категории', max_length=50)
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=rating_choices, null=True, blank=True)

    class Meta:
        verbose_name = 'Категория '
        verbose_name_plural = 'Категории'
    def __str__(self):
        return f'{self.name} - {self.rating}'


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    comment_text = models.TextField()
    likes_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True, blank=False
    )


    def __str__(self):
        return self.comment_text[:20]  # Первые 20 символов

    class Meta:
     verbose_name = "Комментарий"
     verbose_name_plural = "Комментарии"
     ordering = ['created_at']


class Short(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Автор',
        related_name='short')

    video = models.FileField('Видео', upload_to='video_post/', null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views_qty = models.PositiveIntegerField('Просмотры', default=0)
    viewed_users = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='viewed_shorts',
    )
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f'{self.video} - {self.created_at}'

class SavedPosts(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE)
    post = models.ManyToManyField(
        to=Post,
        related_name='saved_post'
    )

    class Meta:
        verbose_name = 'saved_post'
        verbose_name_plural = 'saved_posts'

    def __str__(self):
        return f'{self.user}'

class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    text = models.CharField(max_length=255)
    is_showed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
