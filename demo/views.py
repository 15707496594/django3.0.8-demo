from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from demo.models import Demo
from demo.serializers import DemoSerializer


@csrf_exempt
def demo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        demos = Demo.objects.all()
        serializer = DemoSerializer(demos, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DemoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # serializer.data 数据创建成功后所有数据
            return JsonResponse(serializer.data, status=201)
        # serializer.errors 错误信息
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def demo_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Demo.objects.get(pk=pk)
    except Demo.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = DemoSerializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DemoSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
