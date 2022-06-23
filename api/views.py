from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from users.EmailBackEnd import EmailBackEnd
from django.contrib.auth import get_user_model
from api.serializers import UserSerializer
from users.models import CustomUser
# Create your views here.


class LoginView(APIView):
    def post(self, request):
        print(request.data['email'])
        email = request.data['email']
        password = request.data['password']

        # user = EmailBackEnd.authenticate(request, username=request.POST.get(
        #     'email'), password=request.POST.get('password'))

        # UserModel = get_user_model()

        # user = UserModel.objects.get(email=request.POST.get('email'))
        # user = UserModel.objects.get(email=email)
        user = CustomUser.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed('User Not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        # serializer = UserSerializer(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='token', value=token, httponly=True)

        response.data = {
            'id': user.id,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'type_user': user.user_type,
            'token': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated !')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated !')

        # UserModel = get_user_model()
        # user = UserModel.objects.get(id=payload['id'])

        user = CustomUser.objects.get(id=payload['id'])

        # user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'success'
        }
        return response
