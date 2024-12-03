from django.contrib import admin
from .models import Posts, User, Likes, Follow

# Register your models here.
admin.site.register(Posts)
admin.site.register(User)
admin.site.register(Likes)
admin.site.register(Follow)
