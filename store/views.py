import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from store.models import Store
from store.serializers import StoreSerializer, CalculatorSerializer


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


class StoreView(APIView):

    def get(self):
        stores = Store.objects.all()
        serializer = StoreSerializer(instance=stores,
                                     many=True)  # данние по спіску магазінов many=True , many=False по дефолту
        return Response(serializer.data)

    def post(self):
        serializer = StoreSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)  # error validate
        serializer.save()
        return Response(serializer.data)
