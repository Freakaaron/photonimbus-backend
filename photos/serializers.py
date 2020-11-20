from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    image = serializers.CharField()
    thumbnail = serializers.CharField()