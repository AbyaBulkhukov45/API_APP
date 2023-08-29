from rest_framework import viewsets, status, filters, permissions, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)
from .permissions import OwnerOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get']

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user,
                        post=post)


class FollowListView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (permissions.IsAuthenticated, OwnerOnly)

    def get_queryset(self):
        return self.request.user.followings.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        search_username = self.request.query_params.get('search')
        if search_username:
            queryset = queryset.filter(
                following__username=search_username)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
