from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from demo import models
from demo import serializers


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


class SaleOrderView(APIView):

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
