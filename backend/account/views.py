from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.template import loader
from rest_framework.response import Response
from .models import User
from .tokens import make_token, check_token, get_token
import json


class Login(APIView):
    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user
        }
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(
                email=request.data['email'],
            )
        except User.DoesNotExist:
            return Response('login fail', 401)
        
        if check_password(request.data['password'], user.password) is False:
                return Response('login fail', 401)

        claims = dict(
            nickname = user.nickname
        )
        in_cookie, in_param = make_token(claims=claims)

        res = HttpResponse(json.dumps(dict(
            token = in_param
        )), content_type='application/json')
        res.set_cookie('jwt', in_cookie, httponly=True)

        return res

class GetToken(APIView):
    def get(self, request):
        if 'jwt' in request.COOKIES:
            in_cookie = request.COOKIES['jwt']
            piece = get_token(in_cookie)
            if piece != '':
                return Response(dict(piece=piece), content_type='application/json')
        else:
            raise AuthenticationFailed
        return Response(status=400)

class Info(APIView):
    def post(self, request):
        nickname = ''
        if 'jwt' in request.COOKIES:
            in_cookie = request.COOKIES['jwt']
            if 'jwt' not in request.data:
                raise AuthenticationFailed
            claims = check_token(in_cookie, request.data['jwt'])
            nickname = claims['nickname']
        return Response(data=nickname)
