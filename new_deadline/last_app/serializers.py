from rest_framework import serializers

from last_app.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'price', 'quantity']


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
                stock=stock,
                products=letters['product'],
                quantity=letters['quantity'],
                price=letters['price'],
                defaults={'quantity': 0, 'price': 1000}
            )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for letters in positions:
            StockProduct.objects.create_or_update(
                stock=stock,
                products=letters['product'],
                quantity=letters['quantity'],
                price=letters['price'],
                defaults={'quantity': 0, 'price': 1000}
            )
        return stock
