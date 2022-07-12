from rest_framework import serializers
from store.models import Store


class StoreSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=800)
    rating = serializers.IntegerField(min_value=1, max_value=100)

    def create(self, validated_data):
        return Store.objects.create(**validated_data)


class CalculatorSerializer(serializers.Serializer):
    number1 = serializers.IntegerField()
    number2 = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['add', 'sub', 'mul', 'div'])

    def validate(self, attrs):
        if attrs['action'] == 'div' and not attrs['number2']:
            raise serializers.ValidationError('Number2 cannot be zero for action div')
        return attrs
