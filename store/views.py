import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from store.models import Store
from store.serializers import StoreSerializer, CalculatorSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


@api_view(http_method_names=['GET'])
def today(request):
    my_day = datetime.date.today()
    return Response({
        'date': my_day.today(),
        'year': my_day.year,
        'month': my_day.month,
        'day': my_day.day})


@api_view(http_method_names=['GET'])
def hello_world(request):
    return Response({"message": "Hello My World"})


@api_view(['GET', 'POST'])
def my_name(request):
    if request.method == 'GET':
        return Response({"message": "What is your name Hacker?"})
    return Response({"message": f"Hello, {request.data.get('name')}", })


@api_view(http_method_names=['POST'])
def calculator(request):
    serializer = CalculatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    number1 = serializer.validated_data['number1']
    number2 = serializer.validated_data['number2']
    action = serializer.validated_data['action']

    if action == 'add':
        result = number1 + number2
    elif action == 'sub':
        result = number1 - number2
    elif action == 'mul':
        result = number1 * number2
    elif action == 'div':
        result = number1 / number2

    return Response({'result': result})


# New api for All Store
@api_view(http_method_names=['GET'])
def all_stores(request):
    stores = Store.objects.all()
    # return  Response([{'text': store.text,
    # 'description': store.description,
    # 'rating': store.rating, 'id': store.id}
    # for store in stores])
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


# Created Stores
@api_view(http_method_names=['POST'])
def create_stores(request):
    serializer = StoreSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=HTTP_201_CREATED, data=serializer.data)


class StoreApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        stores = Store.objects.all()

        # ограніченія пользователям
        # stores = Stores.objects.filter(owner__isnull=True)
        serializer = StoreSerializer(stores,
                                     many=True)
        return Response(serializer.data)

    def post(self):
        serializer = StoreSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED, data=serializer.data)


# class StoreViewSet(CreateModelMixin,
#                   ListModelMixin,
#                   RetrieveModelMixin,
#                   UpdateModelMixin,
#                   DestroyModelMixin,
#                   GenericViewSet)


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['status']
    search_fields = ['title', 'rating']

    # проверка юзера на аунтификацию
    def perform_owner(self, serializer):
        serializer.save(**{"owner": self.request.user})

    @action(detail=True, methods=['post'])
    def mark_as_in_review(self, request, pk=None):
        store = self.get_object()
        store.status = 'in_review'
        store.save()
        serializers = self.get_serializer(store)
        return Response(serializers.data)

    @action(detail=True, methods=['post'])
    def mark_as_active(self, request, pk=None):
        store = self.get_object()
        if store.status == 'active':
            store.status = 'in_review'
            store.save()
        serializers = self.get_serializer(store)
        return Response(serializers.data)

    @action(detail=True, methods=['post'])
    def mark_as_deactivated(self, request, pk=None):
        store = self.get_object()
        if store.status == 'deactivated':
            store.status = 'in_review'
            store.save()
        serializers = self.get_serializer(store)
        return Response(serializers.data)
