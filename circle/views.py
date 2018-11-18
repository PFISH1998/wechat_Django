from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from circle.serializers import PostSerializers, CircleUserSerializer, CommentsSerializer
from circle.models import Post, CircleUser, Comments


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
            return HttpResponse(status=404)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializers(post)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk):
        post = self.get_object(pk)
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
        if circle_user:
            return Response(circle_user, status=status.HTTP_304_NOT_MODIFIED)

        serializer = CircleUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_304_NOT_MODIFIED)

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
            return HttpResponse(status=404)

    def put(self, request, pk):
        circle_user = self.get_object(pk)
        serializer = CircleUserSerializer(circle_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        circle_user = self.get_object(pk)
        serializer = CircleUserSerializer(circle_user)
        return JsonResponse(serializer.data)


class CommentsList(APIView):
    @staticmethod
    def get_post(pk):
        try:
            return Post.objects.get(display=True, pk=pk)
        except Post.DoesNotExist:
            raise Exception('no result')


    def get_object(self, pk):
        try:
            self.get_post(pk)
            return Comments.objects.filter(circle=pk)
        except Comments.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            comments = self.get_object(pk)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            post = self.get_post(pk)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            post.increase_comments()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_304_NOT_MODIFIED)


class Like(APIView):
    def post(self, request, user, circle):
        pass

