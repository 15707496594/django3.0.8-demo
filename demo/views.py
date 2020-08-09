from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from demo import models
from demo import serializers
from .utils.permissions import SaleOrderPermission
from .utils.throttling import SaleOrderRateThrottle
from rest_framework.throttling import UserRateThrottle


# @csrf_exempt
# def demo_list(request):
#     """
#     List all code demos, or create a new demo.
#     """
#     if request.method == 'GET':
#         demos = Demo.objects.all()
#         serializer = DemoSerializer(demos, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = DemoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             # serializer.data 数据创建成功后所有数据
#             return JsonResponse(serializer.data, status=201)
#         # serializer.errors 错误信息
#         return JsonResponse(serializer.errors, status=400)

# @api_view(['GET', 'POST'])
# def demo_list(request):
#     """
#     列出所有的demos，或者创建一个新的demo。
#     """
#     if request.method == 'GET':
#         demos = models.Demo.objects.all()
#         serializer = DemoSerializer(demos, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = DemoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # serializer.data 数据创建成功后所有数据
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # serializer.errors 错误信息
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def demo_detail(request, pk):
#     """
#     Retrieve, update or delete a code demo.
#     """
#     try:
#         demo = Demo.objects.get(pk=pk)
#     except Demo.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = DemoSerializer(demo)
#         return JsonResponse(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = DemoSerializer(demo, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         demo.delete()
#         return HttpResponse(status=204)


# @api_view(['GET', 'POST', 'DELETE'])
# def demo_detail(request, pk):
#     """
#     获取，更新或删除一个demo实例。
#     """
#     try:
#         demo = models.Demo.objects.get(pk=pk)
#     except models.Demo.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = DemoSerializer(demo)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = DemoSerializer(demo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         demo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class UserAuth(APIView):
    throttle_classes = [UserRateThrottle, ]

    def post(self, request, *args, **kwargs):
        """
        用户登录，生成token，返回给客户端
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = {'code': 200, 'message': None}
        username = request._request.POST.get('username')
        password = request._request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            response['code'] = 403
            response['message'] = '用户名或密码错误'
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if not user.check_password(password):
            response['code'] = 403
            response['message'] = '用户名或密码错误'
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        ip = self.get_client_ip(request)
        # 用户名密码校验通过，生成token
        try:
            token = self.generate_token(username)
            token_obj = models.UserToken.objects.update_or_create(defaults={'token': token}, user=user, address=ip)[0]
        except Exception as e:
            response['code'] = 500
            response['message'] = '生成token失败'
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['message'] = '验证成功'
        response['data'] = serializers.UserTokenSerializer(token_obj).data
        return Response(response, status=status.HTTP_200_OK)

    def get_client_ip(self, request):
        """
        获取客户端ip
        :param request:
        :return:
        """
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def generate_token(self, username):
        """
        生成token字符串
        :param username:
        :return:
        """
        import hashlib
        import time

        ctime = str(time.time())
        token = hashlib.md5(bytes(username, encoding='utf-8'))
        token.update(bytes(ctime, encoding='utf-8'))
        return token.hexdigest()


class SaleOrderView(APIView):

    # authentication_classes = []
    permission_classes = [SaleOrderPermission, ]
    throttle_classes = [SaleOrderRateThrottle, ]

    def get(self, request, pk=None):
        if pk:
            return self.get_sale_order_by_pk(request, pk)
        else:
            return self.get_sale_order(request)

    def get_sale_order_by_pk(self, request, pk):
        try:
            order = models.SaleOrder.objects.get(pk=pk)
        except models.SaleOrder.DoesNotExist:
            return Response({'code': 404, 'message': '找不到对应记录'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.SaleOrderSerializer(order)
        return Response({'code': 200, 'message': '', 'data': serializer.data})


    def get_sale_order(self, request):
        try:
            orders = models.SaleOrder.objects.all()
        except models.SaleOrder.DoesNotExist:
            return Response({'code': 404, 'message': '找不到对应记录'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.SaleOrderSerializer(orders, many=True)
        return Response({'code': 200, 'message': '', 'data': serializer.data})

    def post(self, request):
        serializer = serializers.SaleOrderSerializer(models.SaleOrder(), request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 201, 'message': '', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'code': 400, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            demo = models.SaleOrder.objects.get(pk=pk)
        except models.SaleOrder.DoesNotExist:
            return Response({'code': 404, 'message': '找不到对应记录'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.SaleOrderSerializer(demo, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'message': '', 'data': serializer.data})
        return Response({'code': 400, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            demo = models.SaleOrder.objects.get(pk=pk)
        except models.SaleOrder.DoesNotExist:
            return Response({'code': 404, 'message': '找不到对应记录'}, status=status.HTTP_404_NOT_FOUND)
        demo.delete()
        return Response({'code': 204, 'message': '删除成功'}, status=status.HTTP_204_NO_CONTENT)
