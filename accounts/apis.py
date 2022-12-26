from rest_framework import views, response, exceptions, permissions
from .import serializer as user_serlializer
from .import services, authentication



class RegisterApi(views.APIView):
    
    def post(self, request):
        serializer = user_serlializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)

        print(data)
        return response.Response(data=serializer.data)



class LoginApi(views.APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']

        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid Credentials')

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed('Invalid Credentials')

        token = services.create_token(user_id=user.id)

        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp 



class UserApi(views.APIView):
    """
    this endpoint can only be used if 
    the user is authenticated
    """
    authentication_classes = (authentication.CostomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user

        serializer = user_serlializer.UserSerializer(user)

        return response.Response(serializer.data)


class LogoutApi(views.APIView):
    authentication_classes = (authentication.CostomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie('jwt')
        resp.data = {'message': 'so long farewell'}

        return resp

