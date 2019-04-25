from django.contrib import admin
from .models import post, postLike

# Register your models here.

class postLikeModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'totalLike')

#sending to admin panel
admin.site.register(post)
admin.site.register(postLike, postLikeModelAdmin)