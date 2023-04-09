from rest_framework import serializers
from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'
        read_only_fields = ('owner',)


class CatShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ('id', 'name',)


class FeedbackSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    text = serializers.CharField(max_length=2048)

    def create(self, validated_data):
        print('sending data:')
        print(validated_data)
        return
