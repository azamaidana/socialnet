# Generated by Django 4.2.3 on 2023-08-18 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_profile_link_fb_profile_photo_profile_telegram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Заголовок'),
        ),
    ]
