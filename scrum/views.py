from django.shortcuts import render,redirect
from  django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from scrum.models import User,Project,AssignedRole, Sprint, UserStory,ProjectMember
from .forms import UserLoginForm,UserRegisterForm,ProjectForm,RoleAssignmentForm,ProjectDisabledForm,SprintForm,UserStoryForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,request, JsonResponse
from django.urls import reverse
from django import forms
from datetime import datetime
from django.utils import timezone

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
    context['user1'] = uporabnik #"ad"#
    context['admin'] = admin #"ad"#
    context['id'] = up_id #1#
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
        existing_user = User.objects.filter(username=username,password=password,active=True).first()
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
            form = UserLoginForm()
            # form.add_error(None, 'Neuspešna prijava. Prosimo, poskusite znova.')
            messages.error(request, "Invalid username or password.")
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
                messages.error(request,"User already exists!")
            else:
                # Ustvari novega uporabnika
                form.save()
                #KO SE REGISTRIRA NOV UPORABNIK POTEM NE ZAMENJAJ KUKIJA
                # request.session['uporabnik'] = username
                # user = authenticate(request, username=username, password=password)
                return redirect('home')

    else:
        form = UserRegisterForm()
        form.fields['password'].required = True
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
        password = request.POST.get('password')
        if not password:
                # Če je polje gesla prazno, nastavi na neko privzeto vrednost
                request.POST = request.POST.copy()
                request.POST['password'] = user.password
        form = UserRegisterForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
        else:
            messages.error(request,"Invalid change!")  
            return redirect('edit_user',user_id)
        #Preveri če urejaš samega sebe:
        if user_id == context['id']:
                request.session['uporabnik'] = form.data['username']
                
        return redirect('home')
        


        # existing_user = User.objects.filter(username=form.data['username']).first()
        # if existing_user:
        #     if existing_user.id == context['id']:
        #         if form.is_valid():
        #             if form.cleaned_data['password'] == '':
        #                 form.cleaned_data['password'] = user.password
        #             form.save()
        #             request.session['uporabnik'] = form.data['username']
        #             return redirect('home',)
        #     messages.error(request,"Invalid change!")  
        #     return redirect('edit_user',user_id)
        # else:
        
        #     if form.is_valid():
        #         if form.cleaned_data['password'] == '':
        #                 form.cleaned_data['password'] = user.password
        #         form.save()
        #         if user_id == context['id']:
        #             request.session['uporabnik'] = form.data['username']
        #         return redirect('home')
        #     else:
        #         form = UserRegisterForm(instance=user)
        #         messages.error(request,"Invalid change!")   
    else:
        messages.error(request, '')
        form = UserRegisterForm(instance=user)
        if not context['admin']:
            form.fields['admin_user'].widget.attrs['disabled'] = True
        context['form'] = form
        context['id_delete'] = user.id
        # if context['id'] != user.id:
        #     form.fields['password'].disabled = True
        return render(request, 'edit_user.html', context)
    


def edit_deleted_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = get_context(request)
    if request.method == 'POST':
        # Tukaj dodajte logiko za posodobitev podatkov uporabnika
        user.active = True
        user.save()
        return redirect("home")
        
    else:
        form = UserRegisterForm(instance=user)    
        if not context['admin']:
            form.fields['admin_user'].widget.attrs['disabled'] = True

        context['form'] = form
        context['id_delete'] = user.id
        return render(request, 'edit_deleted_user.html', context)
    
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.active = False
    user.save()
    return redirect("home")

def new_project(request):  
     if request.method == 'POST':
        # Project.objects.all().delete()
        form = ProjectForm(request.POST)
        if form.is_valid(): 
            name = form.data['name']
            existing_project = Project.objects.filter(name=name).first()
            if existing_project:
                messages.error(request,"Projekt s tem imenom že obstaja!")
                return redirect(request.path)
            else:
                #form.save()
                request.session["forma"] = request.POST# v assign_roles jo shranimo, ker neželimo da se ustvari prej
                # treba je shranit celo POST metodo ker ima zraven token za validacijo
                return redirect(reverse('add_members',kwargs={'ime_projekta': name}))
        else:
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
     
def add_members(request,ime_projekta):
    if request.method == 'POST':
        project_members = request.POST.getlist('project_members')
        request.session["project_members"] = project_members
        if len(project_members) == 0: #MORAŠ IZBRATI VSAJ ENEGA!
            messages.error(request,"Izbrati moraš vsaj enega člana!")
            return redirect(request.path)
        else:
            return redirect(reverse('assign_roles',kwargs={'ime_projekta': ime_projekta}))
    else:
        context = get_context(request)
        all_users = User.objects.all()
        context['project_name'] =  ime_projekta
        context['allusers'] = all_users
        return render(request,'add_members.html',context=context)
     
def assign_roles(request,ime_projekta):
    if request.method == 'POST':
        #nalozim projekt
        data = request.session.get("forma")
        forma = ProjectForm(data)
        forma.save()
        #
        project1 = Project.objects.get(name=ime_projekta)
        product_owner_id = request.POST.get('product_owner')
        methodology_manager_id = request.POST.get('methodology_manager')
        development_team_members = request.POST.getlist('development_team_members')
        # project_name = request.POST.get('project_name')
        existing_project = Project.objects.get(name=ime_projekta)
        if existing_project:
            for member in request.session.get("project_members"):
                u1 = User.objects.get(id = member)
                nov = ProjectMember.objects.create(user = u1,project = project1)
                nov.save()
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
            messages.error(request,"Ojoj, Napaka!")
            return redirect(request.path)
    else:
        context = get_context(request)
        all_users = User.objects.all()
        project_members1 = request.session.get("project_members")
        project_members = [User.objects.get(id = user_id) for user_id in project_members1]
        context['project_members'] = project_members
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
    sprints = Sprint.objects.filter(project=project)
    context['sprints'] = sprints
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

def check_sprint_dates(start_date, end_date, duration, sprints):
    start = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
    end = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
    # Preveri za primer, ko je končni datum pred začetnim.
    if start > end:
        return False

    # Preveri za primer, ko je začetni datum v preteklosti.
    if start < timezone.now():
        return False

    # Preveri za neregularno vrednost hitrosti Sprinta.
    if start + timezone.timedelta(days=duration) != end:
        return False
    
    # Preveri za primer, ko se dodani Sprint prekriva s katerim od obstoječih.
    for sprint in sprints:
        sprint_start = datetime.strptime(sprint.start_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
        sprint_end = datetime.strptime(sprint.end_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
        if start >= sprint_start and start <= sprint_end:
            return False

        if end >= sprint_start and end <= sprint_end:
            return False

        if start <= sprint_start and end >= sprint_end:
            return False
    
    return True

@require_http_methods(["POST", "GET"])
def sprints_list_handler(request, project_name):
    if request.method == 'POST':
        try:
            project = Project.objects.get(name=project_name)
           
            # get start and end date and check for regularity
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            duration = request.POST.get('duration')
            sprints = Sprint.objects.filter(project=project)
            if check_sprint_dates(start_date, end_date, duration, sprints):
                return JsonResponse({'message': 'Sprint dates are not regular'}, status=400)
            sprint = Sprint.objects.create(project=project, start_date=start_date, end_date=end_date)
            sprint.save()
            return redirect('home')#JsonResponse({'message': 'Sprint created successfully'})
        except Project.DoesNotExist:
            return JsonResponse({'message': 'Project does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    if request.method == 'GET':
        try:
            project_name = request.GET.get('project_name')
            project = Project.objects.get(name=project_name)
            sprints = Sprint.objects.filter(project=project)
            return JsonResponse({'sprints': list(sprints.values())})
        except Project.DoesNotExist:
            return JsonResponse({'message': 'Project does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

@require_http_methods(["GET", "POST", "DELETE"])
def sprint_details_handler(request, project_name, sprint_id):
    if request.method == 'GET':
        try:
            sprint = Sprint.objects.get(id=sprint_id)
            return render(request, 'sprint_details.html', context={'sprint': sprint, 'project_name': project_name})
        except Sprint.DoesNotExist:
            return JsonResponse({'message': 'Sprint does not exist'}, status=404)
    
    if request.method == 'DELETE':
        sprint = Sprint.objects.get(id=sprint_id)
        sprint.delete()
        return JsonResponse({'message': 'Sprint deleted successfully'})

def new_sprint(request,project_name):
    context = get_context(request)
    project = Project.objects.get(name=project_name)
    user = User.objects.get(username = context['user1'])
    all_users = User.objects.all()
    context['form'] = SprintForm(initial={'project': project}) 
    # context['formAssignment'] = RoleAssignmentForm()
    context['allusers'] = all_users
    context['project'] = project
    return render(request,'new_sprint.html',context=context)

def edit_sprint(request,project_name,sprint_id):
    if request.method == 'GET':
        sprint = Sprint.objects.get(id=sprint_id)
        context = get_context(request)
        context['sprint'] = sprint
        context['project_name'] = project_name
        form = SprintForm(instance=sprint)
        context['form'] = form
        return render(request, 'sprint_edit.html', context)
    if request.method == 'POST':
        print("POST")
        try: 
            sprint = Sprint.objects.get(id=sprint_id)
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            duration = request.POST.get('duration')
            sprint.start_date = start_date
            sprint.end_date = end_date
            sprint.duration = duration
            sprint.save()
            print(sprint)
            return redirect('sprint_details', project_name=project_name, sprint_id=sprint_id)
        except Sprint.DoesNotExist:
            return JsonResponse({'message': 'Sprint does not exist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)
        
# User story
# ======================================================
def new_user_story(request):
    if request.method == "POST":
        form = UserStoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Uporabniška zgodba uspešno dodana!!")
            return redirect('new_user_story')
        else:
            messages.error(request, "Neveljavni podatki. Vnesi pravilne podatke.")
            return redirect('new_user_story')
    else:
        context = get_context(request)
        user = User.objects.get(username = context['user1'])
        all_users = User.objects.all()
        context['form'] = UserStoryForm(initial={'creator': user}) 
        context['allusers'] = all_users
        return render(request,'new_user_story.html',context=context)
