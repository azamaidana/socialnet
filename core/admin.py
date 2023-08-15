from django.contrib import admin
from .models import Post, Category
from .models import *


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Short)
admin.site.register(SavedPosts)