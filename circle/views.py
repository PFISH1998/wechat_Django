from rest_framework.pagination import PageNumberPagination

from circle.serializers import PostSerializers, CircleUserSerializer, CommentsSerializer, LikeSerializer
from circle.models import Post, CircleUser, Comments, Like
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status
from wechat.settings import appid, apps
import requests
import json


# 登录功能，未完善， 将继续封装成类

def get_open_id(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code"\
            .format(appid, apps, body.get('code'))
        r = requests.get(url)
        data = json.loads(str(r.text))
        openid = data.get("openid")
        user = CircleUser.objects.get(uid=openid)
        u_type = user.type
        user.objects.update(last_login=now())
        r_data = {
            'openid': data.get("openid"),
            'type': u_type
        }
        return HttpResponse(json.dumps({
            'data': r_data,
            'code': 201
        }))
    except CircleUser.DoesNotExist:
        return HttpResponse(json.dumps({
            'data': data.get("openid"),
            'code': 202
        }))

    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'data': data.get("openid"),
            'code': 300
        }))


def file_upload(request):
    try:
        img_file = request.FILES.get('img_file', None)
        return HttpResponse(status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)



# 发布圈子功能
class PostList(APIView):

    def get(self, request):
        uid = request.GET['uid']
        # post = Post.objects.filter(display=True, type='top')
        post = Post.objects.filter(display=True)
        pg = PageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=post, request=request, view=self)
        serializer = PostSerializers(page_roles, many=True, context={"uid": uid})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
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
            uid = request.GET['uid']
            post = self.get_object(pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializers(post, context={"uid": uid})
        return Response(serializer.data)

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
        try:
            uid = request.data.get('uid')
            post = Post.objects.get(pk=pk)
            user = CircleUser.objects.get(uid=uid)
            if user.type == 'admin' or post.uid_id == uid:
                post.display = False
                post.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CircleUserList(APIView):

    def post(self, request):
        circle_user = CircleUser.objects.filter(uid=request.data['uid'])
        if circle_user.exists():
            return Response(status=status.HTTP_304_NOT_MODIFIED, data='user exists')

        serializer = CircleUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN, data='data not valid')

    def get(self, request):
        user = request.GET['user']
        post = Post.objects.filter(display=True, uid_id=user)
        serializer = PostSerializers(post, many=True, context={"uid": user})
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
            like = Like.objects.get(post=pk, uid=request.data['uid'])  #有记录则更新  改成删除
            Like.delete(like)
            post.change_like(request.data['status'])
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Like.DoesNotExist:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            post.change_like(request.data['status'])
            return HttpResponse(status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)






        # return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk):
        try:
            like = Like.objects.get(post_id=pk)
        except Like.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)












"""
    def post(self, request, pk):
        try:
            post = Post.objects.get(display=True, pk=pk)
            uid = request.data['uid']
            like = Like.objects.filter(uid=uid, post_id=pk, type=1)
            like_status = True
            if like.exists():  # 不存在直接插入数据。存在既更新，将点赞状态取反
                for i in like:
                    like_status = not i.status
                like.update(status=like_status)
                post.change_like(like_status)
                post.save()
                return HttpResponse(status=status.HTTP_201_CREATED)

            Like.objects.create(uid=uid, post_id=pk, type=1)
            post.change_like(like_status)
            post.save()
            return HttpResponse(status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            # print(e)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
"""








