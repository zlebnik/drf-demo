from rest_framework import serializers
from cats.models import Cat, Medal


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = '__all__'
        read_only_fields = ('cat',)


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    medals = MedalSerializer(read_only=True, many=True)

    class Meta:
        model = Cat
        fields = '__all__'
        read_only_fields = ('owner', 'medals')


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
        return validated_data
