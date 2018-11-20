from rest_framework import serializers
from circle.models import CircleUser, Post, Comments, Like


class PostSerializers(serializers.ModelSerializer):
    pub_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, required=False)
    comments_count = serializers.IntegerField(read_only=True, required=False)
    like_count = serializers.IntegerField(read_only=True, required=False)
    post_user = serializers.CharField(source='uid.nick_name', required=False)

    class Meta:
        model = Post
        fields = ('id', 'post_user', 'uid', 'content',
                  'pub_time', 'comments_count', 'like_count', 'dis_like_count')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.content = validated_data.get()


class CircleUserSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(read_only=True)

    class Meta:
        model = CircleUser
        fields = ('uid', 'nick_name', 'we_name', 'head_pic', 'description')

    def create(self, validated_data):
        return CircleUser.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    comment_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, required=False)

    class Meta:
        model = Comments
        fields = ('id', 'comment_content', 'circle', 'comment_time', 'from_user')

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)


# class NotesSerializer(serializers.ModelSerializer):
#     comment_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, required=False)



class LikeSerializer(serializers.ModelSerializer):
    like_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, required=False)
    class Meta:
        model = Like
        fields = ('id', 'type_id', 'type', 'nick_name', 'like_time')

    def create(self, validated_data):
        return Like.objects.create(**validated_data)