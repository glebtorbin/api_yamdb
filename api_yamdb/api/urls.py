from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewsViewSet, TitleViewSet)
from users.views import UsersViewSet, api_get_token, api_signup

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', api_signup, name='signup'),
    path('token/', api_get_token, name='get_token'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
