from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from circle.serializers import PostSerializers, CircleUserSerializer, CommentsSerializer, LikeSerializer
from circle.models import Post, CircleUser, Comments, Like


class PostList(APIView):
    def get(self, request):
        post = Post.objects.filter(display=True)
        serializer = PostSerializers(post, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Post.objects.get(pk=pk, display=True)
        except Post.DoesNotExist:
            print("Post DoesNotExist!")
            raise

    def get(self, request, pk):
        try:
            post = self.get_object(pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializers(post)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk):
        try:
            post = self.get_object(pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.display = False
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CircleUserList(APIView):

    def post(self, request):
        print(request.data)
        print(request.data['nick_name'])
        circle_user = CircleUser.objects.filter(nick_name=request.data['nick_name'])
        print(circle_user)
        if circle_user.exists():
            # print("not")
            return Response(status=status.HTTP_304_NOT_MODIFIED, data='user exists')

        serializer = CircleUserSerializer(data=request.data)
        if serializer.is_valid():
            # print('yes')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_304_NOT_MODIFIED, data='data not valid')

    def get(self, request):
        user = CircleUser.objects.all()
        serializer = CircleUserSerializer(user, many=True)
        return Response(serializer.data)


class CircleUserDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return CircleUser.objects.get(pk=pk)
        except CircleUser.DoesNotExist:
            print('CircleUser.DoesNotExist')
            raise

    def put(self, request, pk):
        try:
            circle_user = self.get_object(pk)
        except CircleUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CircleUserSerializer(circle_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            circle_user = self.get_object(pk)
        except CircleUser.DoesNotExist:
            return HttpResponse(status=404)

        serializer = CircleUserSerializer(circle_user)
        return JsonResponse(serializer.data)


class CommentsList(APIView):
    @staticmethod
    def get_post(pk):
        try:
            return Post.objects.get(display=True, pk=pk)
        except Post.DoesNotExist:
            print('Post DoesNotExist!')
            raise

    def get_object(self, pk):
        try:
            self.get_post(pk)
            return Comments.objects.filter(circle=pk)
        except Comments.DoesNotExist or Post.DoesNotExist:
            raise

    def get(self, request, pk):
        try:
            comments = self.get_object(pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            post = self.get_post(pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            post.increase_comments()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_304_NOT_MODIFIED)


class CommentNoteList(APIView):

    def get(self, request, pk):  # 根据用户查找是否有未提醒的评论， pk 为用户ID
        note = Comments.objects.filter(is_view=False, circle__uid=pk)
        serializer = CommentsSerializer(note, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class LikeList(APIView):

    def post(self, request, pk):
        try:
            post = Post.objects.get(display=True, pk=pk)
            user_id = request.data['nick_name']
            like = Like.objects.filter(nick_name_id=user_id, type_id=pk, type=1)
            like_status = True
            if like.exists():  # 不存在直接插入数据。存在既更新，将点赞状态取反
                for i in like:
                    like_status = not i.status
                like.update(status=like_status)
                post.change_like(like_status)
                post.save()
                return HttpResponse(status=status.HTTP_201_CREATED)

            Like.objects.create(nick_name_id=user_id, type_id=pk, type=1)
            post.change_like(like_status)
            post.save()
            return HttpResponse(status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            # print(e)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            like = Like.objects.get(type_id=pk)
        except Like.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = LikeSerializer(like)
        return Response(serializer.data)





