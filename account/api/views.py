from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from account.models import Account
from photos.models import SharedImage, Image
import base64

@api_view(['GET'])
def getUsers(request):
    if request.method == "GET":
        try:
            username = request.GET.get("username")
            data = SharedImage.objects.filter(username=username)
            users = {}
            ids = []
            for d in data:
                if d.friend not in users:
                    ref = Image.objects.filter(id=d.image_id)[0]
                    users[d.friend] = [[ref.id, base64.b64encode(ref.thumbnail)]]
                else:
                    ref = Image.objects.filter(id=d.image_id)[0]
                    users[d.friend].append([ref.id, base64.b64encode(ref.thumbnail)]) 
            remaining_users = Account.objects.exclude(username=username)
            for user in remaining_users:
                if user.username not in users:
                    users[user.username] = ""
            return Response(users)
        except:
            return Response({
                "message": "Could not fetch users."
            })
    else:
        return Response({
                "message": "This API only support GET requests."
            })


@api_view(['POST',])
@permission_classes([AllowAny])
def registration_view(request):
    try:
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = "Successfully registered new user"
                data['email'] = account.email
                data['username'] = account.username
                data['first_name'] = account.first_name
                data['last_name'] = account.last_name
                token = Token.objects.get(user=account).key
                data['token'] = token

            else:
                data = serializer.errors

            return Response(data)
    except :
        return Response({
            "message": "Could not be registered."
        })
