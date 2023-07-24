from django.contrib import admin
from . import models
from .models import Tag, TaggedItem

# Register your models here.
# admin.site.register(Tag)
@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    #autocomplete_fields = ['label']
    search_fields = ['tag']
#admin.site.register(TaggedItem)
