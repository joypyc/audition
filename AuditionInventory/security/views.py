from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView

from security.serializers import UserSerializer


def serialize_user_data(user_instance:User, fields:list=['id','first_name']):
        serialized_data = {}
        user_data = UserSerializer(user_instance).data
        for field in fields:
            serialized_data[field] = user_data.get(field,None)
        return serialized_data


class LoginView(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            user_data = serialize_user_data(user)
            return JsonResponse({'user': user_data}, status=200)
        return JsonResponse({"error": "Unable to authenticate. Username or Password is incorrect"}, status=400)


class LogoutView(APIView):

    def post(self, request):
        request_user = request.user
        if request_user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "Log out successful"}, status=200)
        return JsonResponse({"error": "Unable to log out"}, status=400)


@ensure_csrf_cookie
def get_csrf_token(request):
    try:
        return JsonResponse({'message': 'success'}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'Error': 'An unknown error has occured, please contact your system administrator.'},
                        status=status.HTTP_400_BAD_REQUEST)


def check_authentication(request):
    request_user = request.user
    if request_user.is_authenticated:
        user_data = serialize_user_data(request_user)
        return JsonResponse({'user': user_data}, status=200)
    return JsonResponse({"error": "User is unauthenticated"}, status=400)
