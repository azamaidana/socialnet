# Generated by Django 4.2.3 on 2023-08-18 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_post_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='short',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]