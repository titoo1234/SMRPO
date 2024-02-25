from django.shortcuts import render
from  django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from scrum.models import User
from scrum.serializers import UserSerializer

# Create your views here.
@csrf_exempt
def userApi(request,user_id=0):
    if request.method =='GET':
        users = User.objects.all()
        user_serializer = UserSerializer(users,many=True)
        return render(request, 'login.html')
        return JsonResponse(user_serializer.data,safe=False)
    elif request.method == 'POST':
        # ime = request.POST['username']
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data = user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully",safe=False)
        return JsonResponse("Failed to add",safe=False)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        user_serializer = UserSerializer(user,data = user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succesfully",safe=False)
        return JsonResponse("Failed to update",safe=False)
    elif request.method == 'DELETE':
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse("Deleted succesfully")