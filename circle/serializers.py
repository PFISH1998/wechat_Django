from rest_framework import serializers
from circle.models import CircleUser, Post, Comments, Like


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'nick_name', 'content',
                  'pub_time', 'comments_count', 'like_count', 'dis_like_count')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.content = validated_data.get()


class CircleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircleUser
        fields = ('nick_name', 'we_name', 'head_pic', 'description')

    def create(self, validated_data):
        return CircleUser.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'comment_content', 'circle', 'comment_time', 'from_user')

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'type_id', 'type', 'nick_name', 'like_time')

    def create(self, validated_data):
        return Like.objects.create(**validated_data)