from rest_framework import serializers

from pw_app.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        quantity = serializers.IntegerField(default=0)
        price = serializers.IntegerField(default=0)
        model = StockProduct
        fields = ['stock', 'product', 'price', 'quantity']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    product = ProductSerializer(many=False)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'product']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for letters in positions:
            StockProduct.objects.create(
                stock=letters['stock_id'],
                products=letters['products_id'],
            )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for letters in positions:
            StockProduct.objects.create_or_update(
                stock=letters['stock_id'],
                products=letters['products_id'],
            )
        return stock
