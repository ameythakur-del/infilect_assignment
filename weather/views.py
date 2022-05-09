from django.contrib.auth import authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
import requests

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    # username and password will be passed from the frontend
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    # Token is unique for every session. It gets when user logs out
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key},
                    status=HTTP_200_OK)

@api_view(["GET"])
def User_logout(request):
    # Here, we are deleting the token to expire the session
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')

@csrf_exempt
@api_view(["GET"])
def sample_api(request, page=1):
    # We are calling the weather API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=648eb266e5c66ade214f030a0ffd0273'
    city_weather = None

    # Creating a list of 30 cities
    cities = ['Chicago', 'New York City', 'Mumbai', 'Pune', 'Hong Kong', 'Tokyo', 'Moscow', 'Delhi', 'Kolkata', 'Chennai', 
    'Bangalore', 'Hyderabad', 'London', 'Paris', 'Dubai', 'Singapore', 'Los Angeles', 'Barcelone', 'Shanghai', 'Beijing',
    'Dhaka', 'Karachi', 'Istanbul', 'Rio de Janeiro', 'Osaka', 'Manila', 'Lahore', 'Lima', 'Bangkok', 'Ahmedabad']
    
    # Initializing dictionary result which will be sent as a JSON response
    results = {'data': []}
    
    # Here, the logic of pagination is implemented. 
    # Data of 10 cities is appended in the list in results dictionary depending on the number of page passed from the app
    for city in cities[(page-1)*10:page*10]:
        city_weather = requests.get(url.format(city)).json()
        results['data'].append(city_weather)
    
    return Response(results)