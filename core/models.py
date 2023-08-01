from django.db import models
# from django.contrib.auth.models import User
#
# class Profile(models.Model):
#     user = models.OneToOneField(
#         to=User,on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=55)
#     description = models.TextField(null=True, blank=True)


class Post(models.Model):
    status_choices = (('Published', 'Published'),
                      ('Unpublished', 'Unpublished'))

    name = models.CharField('Заголовок', max_length=80)
    description = models.TextField('Описание', null=True)
    photo = models.ImageField('Фотография', upload_to='photo_post/', null=True, blank=True)
    status = models.CharField('Статус публикации', max_length=100, choices=status_choices)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    def __str__(self):
        return f'{self.name}'

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
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=rating_choices)

    class Meta:
        verbose_name = 'Категория '
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'





