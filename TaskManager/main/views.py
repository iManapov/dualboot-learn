from rest_framework import viewsets
import django_filters
from main.serializers import UserSerializer, TaskSerializer, TagSerializer
from main.models import User, Task, Tag


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ('username', 'email',)


class TagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ('title',)


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ('state', 'priority', 'assignee__username', 'author__username', 'tag__title')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    filterset_class = TagFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('assignee', 'author').prefetch_related('tag').order_by("id")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
