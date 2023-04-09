from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import routers

from cats import models

from .serializers import CatSerializer, FeedbackSerializer


class CatsViewSet(viewsets.ModelViewSet):
    queryset = models.Cat.objects.all()
    serializer_class = CatSerializer


@api_view(['POST'])
def feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


router = routers.DefaultRouter()
router.register('cats', CatsViewSet)