from django.contrib import admin
from .models import post,Author,Tag,comments
# Register your models here.
class postadmin(admin.ModelAdmin):
    list_filter= ('author','tag','date')
    list_display= ('title','date','author')
    prepopulated_fields={'slug':('title',)}

class CommenteDisplay(admin.ModelAdmin):
    list_display = ('username','post')
admin.site.register(post,postadmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(comments,CommenteDisplay)
