from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import permissions

import random

from cats import models

from .serializers import CatSerializer, CatShortSerializer, FeedbackSerializer


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


router = routers.DefaultRouter()
router.register('cats', CatsViewSet)
