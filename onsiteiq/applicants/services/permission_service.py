from django.contrib.auth import authenticate, login
import json


class PermissionService:

    @classmethod
    def authenticate_and_login_request(cls, request):

        request_json = json.loads(request.body)
        username = request_json.get("username", None)
        password = request_json.get("password", None)

        if username is None or password is None:
            return None

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

        return user
