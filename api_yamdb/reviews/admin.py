from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    search_fields = (
        'username',
        'role',
    )
    list_filter = (
        'username',
        'role',
    )
    empty_value_display = '>empty<'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    list_editable = ('category',)
    search_fields = (
        'name',
        'year',
    )
    list_filter = ('name',)
    empty_value_display = '>empty<'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '>empty<'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '>empty<'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'pub_date',
        'author',
        'score',
        'title',
    )
    search_fields = (
        'text',
        'author',
        'title',
    )
    list_filter = (
        'pub_date',
        'author',
        'title',
    )
    empty_value_display = '>empty<'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'pub_date',
        'author',
        'review',
    )
    search_fields = (
        'text',
        'author',
        'review',
    )
    list_filter = (
        'pub_date',
        'author',
        'review',
    )
    empty_value_display = '>empty<'


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
