from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    # list_editable = ('pk',)
    search_fields = ('name',)
    list_filter = ('name',)
    # empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )


# class FollowAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'author'
#     )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
# admin.site.register(Follow, FollowAdmin)

admin.site.register(CustomUser, UserAdmin)
