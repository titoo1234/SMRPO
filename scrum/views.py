from django.shortcuts import render,redirect
from  django.views.decorators.csrf import csrf_exempt
from scrum.models import User,Project,AssignedRole
from .forms import UserLoginForm,UserRegisterForm,ProjectForm,RoleAssignmentForm,ProjectDisabledForm
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,request
from django.urls import reverse
from django import forms
# Create your views here.
def get_context(request):
    try:
        uporabnik = request.session.get('uporabnik')
        admin = request.session.get('admin')
        up_id = request.session.get('uporabnik_id')
    except:
        uporabnik = None
        admin = False
        up_id = None
    context = {}
    context['user1'] = uporabnik
    context['admin'] = admin
    context['id'] = up_id
    return context


def logout(request):
    try:
        del request.session['uporabnik']
        del request.session['admin']
    except:
        pass
    return redirect('home')
def get_projects(uporabnik_id):
    project_ids = AssignedRole.objects.filter(user_id=uporabnik_id).values_list('project', flat=True).distinct()
    projects = Project.objects.filter(id__in=project_ids)
    return list(projects)
    
def home(request):
    messages.error(request, '')  
    context = get_context(request)
    try:
        projects = get_projects(context['id'])
    except:
        projects = []
    context['projects'] = projects
    return render(request, 'home.html',context)
def test(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        messages.error(request, '')
        form = UserLoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
            # user = UserLoginForm(request, username=username, password=password)
        existing_user = User.objects.filter(username=username,password=password).first()
        if  existing_user:  
            request.session['uporabnik'] = existing_user.username
            request.session['admin'] = existing_user.admin_user
            request.session['uporabnik_id'] = existing_user.id
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
                #KO SE REGISTRIRA NOV UPORABNIK POTEM NE ZAMENJAJ KUKIJA
                # request.session['uporabnik'] = username
                # user = authenticate(request, username=username, password=password)
                return redirect('home')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def allusers(request):
    context = get_context(request)
    context['users'] = User.objects.all()
    return render(request,'all_users.html',context)

def user_detail(request, user_id):
    user = User.objects.get(user_id=user_id)
    return render(request, 'user_detail.html', {'user': user})

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = get_context(request)
    if request.method == 'POST':
        # Tukaj dodajte logiko za posodobitev podatkov uporabnika
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request,"Neveljavna sprememba!")   
    else:
        form = UserRegisterForm(instance=user)
        if not context['admin']:
            form.fields['admin_user'].widget.attrs['disabled'] = True
            print('asd')
        print('asd1')
        context['form'] = form
        return render(request, 'edit_user.html', context)
    

def new_project(request):  
     if request.method == 'POST':
        # Project.objects.all().delete()
        form = ProjectForm(request.POST)
        print(1)
        if form.is_valid(): 
            name = form.data['name']
            existing_project = Project.objects.filter(name=name).first()
            if existing_project:
                print(4)
                messages.error(request,"Projekt s tem imenom že obstaja!")
                return redirect(request.path)
            else:
                print(5)
                form.save()
                #TODO preusemri ga v assign roles
                # return redirect('home')
                return redirect(reverse('assign_roles', kwargs={'ime_projekta': name}))
        else:
            print(3)
            messages.error(request,"Napačni podatki!")
            return redirect(request.path)
     else:
        context = get_context(request)
        user = User.objects.get(username = context['user1'])
        all_users = User.objects.all()
        context['form'] = ProjectForm(initial={'creator': user}) 
        # context['formAssignment'] = RoleAssignmentForm()
        context['allusers'] = all_users
        return render(request,'new_project.html',context=context)
     
def assign_roles(request,ime_projekta):
    if request.method == 'POST':
        project1 = Project.objects.get(name=ime_projekta)
        product_owner_id = request.POST.get('product_owner')
        methodology_manager_id = request.POST.get('methodology_manager')
        development_team_members = request.POST.getlist('development_team_members')
        # project_name = request.POST.get('project_name')
        existing_project = Project.objects.get(name=ime_projekta)
        if existing_project:
            u = User.objects.get(id = product_owner_id)
            nov = AssignedRole.objects.create(user = u,role = 'product_owner',project = project1)
            nov.save()
            u = User.objects.get(id = methodology_manager_id)
            nov = AssignedRole.objects.create(user = u,role = 'methodology_manager',project = project1)
            nov.save()
            for user_id in development_team_members:
                u = User.objects.get(id = user_id)
                nov = AssignedRole.objects.create(user = u,role = 'development_team_member',project = project1)
                nov.save()
            #TODO POŠLJI GA NA PROJEKT    
            return redirect('home')
        else:
            #TODO NEVEM KAJ TUKAJ
            messages.error(request,"Napačni podatki!")
            redirect('home')
    else:
        context = get_context(request)
        all_users = User.objects.all()
        # context['form'] = ProjectForm(initial={'creator': user})
        context['project_name'] =  ime_projekta
        # context['formAssignment'] = RoleAssignmentForm()
        context['allusers'] = all_users
        return render(request,'assign_roles.html',context=context)
    


def project_view(request,project_name):
    context = get_context(request)
    project = Project.objects.get(name=project_name)
    context['project'] = project
    form = ProjectDisabledForm(instance=project)
    context['form'] = form
    is_creator = (project.creator.id == context['id'])
    context['is_creator'] = is_creator
    return render(request, 'project.html', context)

def project_edit(request,project_name):
    project = Project.objects.get(name=project_name)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            project_name = form.cleaned_data['name']
            return redirect('project_name',project_name=project_name)
        else:
            messages.error(request,"Neveljavna sprememba!")
    else:
        context = get_context(request)
        context['project'] = project
        form = ProjectForm(instance=project)
        context['form'] = form
        return render(request, 'project_edit.html', context)

        


