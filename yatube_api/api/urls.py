from django.urls import include, path
from rest_framework import routers
from api.views import (
    PostViewSet,
    GroupViewSet,
    CommentViewSet,
    FollowListView,
)

v1_router = routers.DefaultRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/follow/', FollowListView.as_view(), name='follow-list'),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
