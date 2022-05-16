import jwt
import datetime
from django.conf import settings
from .models import Token
from rest_framework.exceptions import AuthenticationFailed


def make_token(claims):
    claims['exp'] = datetime.datetime.now() + datetime.timedelta(hours=1)
    claims['iat'] = datetime.datetime.now()

    token = jwt.encode(
        claims,
        algorithm="HS256",
        key=settings.SECRET_KEY
    )

    tokens = token.split('.')

    in_cookie = tokens[0]+'.'+tokens[1]
    in_param = tokens[2]

    qs = Token.objects.create(
        token = in_cookie,
        piece = in_param
    )

    return in_cookie, in_param

def get_token(in_cookie):
    try:
        token = Token.objects.get(token=in_cookie)
    except Token.DoesNotExist:
        return ''
    return token.piece

def check_token(in_cookie, in_param):
    if in_cookie is None or in_param is None:
        return None
    token = in_cookie + '.' + in_param
    try:
        claims = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
    except Exception as e:
        raise AuthenticationFailed
    
    return claims