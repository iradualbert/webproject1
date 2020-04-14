from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from Channel.models import Channel
from .models import Product, ProductQuestion, Picture, ProductAnswer
from .api.serializers import *


def business(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    products = Product.objects.filter(channel=channel)
    questions = ProductQuestion.objects.all()
    pictures = Picture.objects.all()
    answers = ProductAnswer.objects.all()
    context = {
        'products': products,
        'questions': questions,
        'pictures': pictures,
        'answers': answers,
    }
    return render(request, 'business/index.html', context)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def products(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    products = Product.objects.filter(channel=channel)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_product(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    user = request.user
    if channel.is_admin(user) or channel.owner == user:
        return Response({'result':'created'})
    else:
        return Response({'result':'bad request'})
