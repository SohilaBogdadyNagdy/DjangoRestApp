
from django.contrib.auth.models import Group
from django.db.models import Sum
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from paymobApp.api.serializers import UserSerializer, GroupSerializer, ProductSerializer
from paymobApp.api.models import Product, UserProfile
from django.contrib.auth.models import User
from paymobApp.api.permissions import is_in_group, HasGroupPermission
from paymobApp.api.utils import currencyConverter, getRatesFromBaseCurrency

@method_decorator(ratelimit(key='ip', method=ratelimit.ALL, rate='5/m'), name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

@method_decorator(ratelimit(key='ip', method=ratelimit.ALL, rate='5/m'), name='dispatch')
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@method_decorator(ratelimit(key='ip', method=ratelimit.ALL, rate='5/m'), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['admin'],
        'PUT': ['admin'],
    }
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)

@method_decorator(ratelimit(key='ip', method=ratelimit.ALL, rate='5/m'), name='dispatch')
class ProductDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view product details
    """
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['__all__'],
        'POST': ['admin'],
        'PUT': ['admin'],
    }
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *arg, **kwargs):
        profile = UserProfile.objects.filter(user=self.request.user).first()
        userCurrency = profile['currency'] if profile else 'USD'
        allRates = getRatesFromBaseCurrency(userCurrency)
        queryset = Product.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for record in data:
            record['price'] = allRates.get(record['currency']) * record['price'] if allRates.get(record['currency']) else record['price']
            record['currency'] = userCurrency if allRates.get(record['currency']) else record['currency']
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)

@method_decorator(ratelimit(key='ip', method=ratelimit.ALL, rate='5/m'), name='dispatch')
class ProductPurchaseViewSet(viewsets.ViewSet):
    """
    API endpoint that allow to normal users to purchase a product
    """
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['__all__'],
        'PATCH': ['normal'],
    }
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
@method_decorator(ratelimit(key='ip', method=ratelimit.ALL, rate='5/m'), name='dispatch')
class ProductsTotalRevenue(viewsets.ViewSet):
    """
    API endpoint that allow admin user to get total revenue
    """
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['admin'],
    }
    def list(self, request):
        user = request.user
        total = Product.objects.filter(isPaid=True).aggregate(Sum('price'))
        return Response(total)


