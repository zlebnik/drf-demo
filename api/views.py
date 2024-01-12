from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import permissions

import random

from cats import models

from .serializers import CatSerializer, CatShortSerializer, FeedbackSerializer, MedalSerializer


class CatsViewSet(viewsets.ModelViewSet):
    queryset = models.Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CatShortSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.owner = None
        instance.save()

    @action(detail=True,
            methods=['post'],
            permission_classes=(permissions.AllowAny,),
            serializer_class=serializers.Serializer
            )
    def pet(self, request, pk=None):
        cat = self.get_object()
        if request.user == cat.owner:
            return Response({'response': f'{cat.name} likes you'})
        return Response({'response': f'{cat.name} {random.choice(["bites", "likes"])} you'})


@api_view(['POST'])
def feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class MedalViewSet(viewsets.ModelViewSet):
    serializer_class = MedalSerializer

    def perform_create(self, serializer):
        cat = get_object_or_404(models.Cat, pk=self.kwargs.get('cat_id'))
        serializer.save(cat=cat)

    def get_queryset(self):
        cat = get_object_or_404(models.Cat, pk=self.kwargs.get('cat_id'))
        return cat.medals.all()


router = routers.SimpleRouter()
router.register('cats', CatsViewSet)
router.register(
    r'cats/(?P<cat_id>\d+)/medals',
    MedalViewSet,
    basename='cats-medals'
)
