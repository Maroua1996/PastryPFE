from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)
admin.site.register(Response)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Comment)
