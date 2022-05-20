from django.contrib import admin
from .models import Category, Post, PostImage, Tag, Comment

admin.site.register(Comment)
admin.site.register(Tag)


class ImageInline(admin.TabularInline):
    model = PostImage
    list_display = {'post', 'original_image', }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        ImageInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
