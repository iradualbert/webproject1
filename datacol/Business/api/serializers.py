from rest_framework import serializers
from Business.models import Product, UserGuide, ProductQuestion, ProductAnswer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGuide
        fields = '__all__'
class ProductQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = '__all__'

class ProductAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnswer
        fields = '__all__'
