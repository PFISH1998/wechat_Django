from rest_framework import serializers
from circle.models import CircleUser, Post, Comments, Like


class PostSerializers(serializers.ModelSerializer):
    pub_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, required=False)
    comments_count = serializers.IntegerField(read_only=True, required=False)
    like_count = serializers.IntegerField(read_only=True, required=False)
    post_user = serializers.CharField(source='uid.nick_name', required=False)
    head_pic = serializers.CharField(source='uid.head_pic', required=False)
    is_like = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'post_user', 'head_pic', 'uid', 'content',
                  'pub_time', 'comments_count', 'like_count',
                  'is_like', 'dis_like_count')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def get_is_like(self, obj):
        try:
            Like.objects.get(uid=self.context['uid'], status=True, post_id=obj.id)
            return True
        except Like.DoesNotExist:
            return False





    # def update(self, instance, validated_data):
    #     instance.content = validated_data.get()


class CircleUserSerializer(serializers.ModelSerializer):
    # uid = serializers.IntegerField(read_only=True)

    class Meta:
        model = CircleUser
        fields = ('uid', 'nick_name', 'we_name', 'head_pic', 'description', 'gender')

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
        fields = ('id', 'post', 'type', 'uid', 'like_time', 'status')

    def create(self, validated_data):
        return Like.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Like.objects.update(**validated_data)