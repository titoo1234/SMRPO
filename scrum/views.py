from django.shortcuts import render,redirect
from  django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from scrum.models import User
from scrum.serializers import UserSerializer
from .forms import UserLoginForm,UserRegisterForm
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,request
# Create your views here.
def set_cookie(ime):
    # request.
    response = HttpResponse('blah')
    response.set_cookie('uporabnik', ime)
    uporabniskoIme = request.COOKIES.get('uporabnik')
    print('imee',uporabniskoIme)
def delete_cookie():
    response = HttpResponse()
    response.delete_cookie('uporabnik')

def get_user():
    '''
    Pogleda, kdo je uporabnik
    '''

    uporabniskoIme = request.COOKIES.get('uporabnik')
    print('ime',uporabniskoIme)
    # print("kaze da je od ccokia",uporabniskoIme)
    return uporabniskoIme
def home(request):
    context = {}
    us = 'us'#get_user()
    if us:
        context['user1'] = 'us'

    return render(request, 'home.html',context)



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
            # user = UserLoginForm(request, username=username, password=password)
        existing_user = User.objects.filter(username=username,password=password).first()
        if  existing_user:
            

            
            # set_cookie(existing_user.name)
            
            return redirect('home')
        
            # if user is not None:
            #     login(request, user)
            #     return redirect('home')
        else:
            # messages.error(request.messages)
            messages.error(request, 'Neuspešna prijava. Prosimo, poskusite znova.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            
            username = form.data['username']
            password = form.data['password']
            name = form.data['name']
                        # Preveri, ali uporabnik že obstaja
            existing_user = User.objects.filter(username=username,password=password).first()
            if existing_user:
                
                # Uporabnik že obstaja, tukaj lahko dodate dodatno obdelavo ali vrnete napako
                messages.error(request,"Uporabnik že obstaja!")
            else:
                # Ustvari novega uporabnika
                form.save()
                # new_user = User.objects.create(username=username, password=password, name=name)
 
                # new_user.save()
                # set_cookie(name)
                return redirect('home')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

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