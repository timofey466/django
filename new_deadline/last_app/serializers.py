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

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'product']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for letters in positions:
            StockProduct.objects.create(
                stock=stock,
                product=letters['product'],
                quantity=letters['quantity'],
                price=letters['price'],
            )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for letters in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                products=letters['product'],
                defaults={
                    'quantity': letters['quantity'],
                    'price': letters['price']}
            )
        return stock
