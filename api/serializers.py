from rest_framework import serializers
from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'
        read_only_fields = ('owner',)


class FeedbackSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    text = serializers.CharField(max_length=2048)
