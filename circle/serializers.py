from rest_framework import serializers
from circle.models import CircleUser, Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'nick_name', 'content', 'pub_time')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.content = validated_data.get()


class CircleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircleUser
        fields = ('id', 'nick_name', 'we_name', 'head_pic', 'description')

    def create(self, validated_data):
        return CircleUser.objects.create(**validated_data)