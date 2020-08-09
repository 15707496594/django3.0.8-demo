from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from demo.models import UserToken


class JulyTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        if request._request.path == '/api/v1/auth':
            return
        token_str = request._request.GET.get('token')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")
        token = UserToken.objects.filter(token=token_str, address=ip).first()
        if not token:
            raise AuthenticationFailed('用户未登录认证！')
        return (token.user, token)

    def authenticate_header(self, request):
        pass
