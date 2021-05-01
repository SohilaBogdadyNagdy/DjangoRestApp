from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from paymobApp.api.serializers import UserSerializer, GroupSerializer, ProductSerializer
from paymobApp.api.models import Product

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view product details
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductPurchaseViewSet(viewsets.ViewSet):
    """
    API endpoint that allow to normal users to purchase a product
    """
    def list(self, request):
        user = request.user
        queryset = Product.objects.filter(purchasedBy=user)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        if (product.isPaid):
            return Response({
                'message': 'Not allowed to purhase product'
            }, 400)
        
        product.isPaid = True
        product.purchasedBy = request.user
        product.save(update_fields=['isPaid', 'purchasedBy'])
        return Response({
            'message': 'successs',
        })

