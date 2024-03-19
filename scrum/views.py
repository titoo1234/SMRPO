from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from scrum.models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse,request, JsonResponse
from django.urls import reverse

from django import forms

from datetime import datetime, time
from django.utils import timezone
from .tables import *
from django_tables2 import RequestConfig
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
    project_ids = ProjectMember.objects.filter(user=uporabnik_id).values_list('project', flat=True).distinct()
    projects = Project.objects.filter(id__in=project_ids)
    return list(projects)
    
def home(request):
    # messages.error(request, '')
    context = get_context(request)
    try:
        projects = get_projects(context['id'])
    except:
        projects = []
    context['projects'] = projects
    queryset = Project.objects.all()
    tabela = ProjectTable(projects, admin = context['admin'],user_id = context['id'])
    RequestConfig(request).configure(tabela)
    context['tabela'] = tabela

    other = [p for p in queryset if p not in projects]
    tabela_other = ProjectTable(other, admin = True,user_id = context['id'])
    RequestConfig(request).configure(tabela_other)
    context['tabela_other'] = tabela_other

    return render(request, 'home.html',context)

def test(request):
    return render(request, 'index.html')

def user_login(request):
    context = get_context(request)
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
            messages.success(request,"User " + existing_user.username +" successfully logged in.")
            return redirect('home')
            # if user is not None:
            #     login(request, user)
            #     return redirect('home')
        else:
            # messages.error(request.messages)
            form = UserLoginForm()
            # form.add_error(None, 'Neuspešna prijava. Prosimo, poskusite znova.')
            messages.error(request, "Invalid username or password.")
            return redirect(request.path)
    else:
        form = UserLoginForm()
        
        context['form'] = form
        return render(request, 'login.html', context)

def user_register(request):
    context = get_context(request)
    if request.method == 'POST':
        form = UserRegisterForm1(request.POST)
        if form.is_valid():
            
            username = form.data['username']
            password = form.data['password']
            name = form.data['name']
                        # Preveri, ali uporabnik že obstaja
            existing_user = User.objects.filter(username=username,password=password).first()
            if existing_user:
                
                # Uporabnik že obstaja, tukaj lahko dodate dodatno obdelavo ali vrnete napako
                messages.error(request,"User already exists!")
                return redirect(request.path)
            else:
                # Ustvari novega uporabnika
                form.save()
                messages.success(request,"Usser added succesfuly!")
                #KO SE REGISTRIRA NOV UPORABNIK POTEM NE ZAMENJAJ KUKIJA
                # request.session['uporabnik'] = username
                # user = authenticate(request, username=username, password=password)
                return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect(request.path)

    else:
        form = UserRegisterForm1()
        form.fields['password'].required = True
        context = get_context(request)
        context['form'] = form
        return render(request, 'register.html', context)

def allusers(request):
    context = get_context(request)
    active_users = User.objects.filter(active=True)
    active_users = UserTable(active_users, admin = True)
    RequestConfig(request).configure(active_users)
    context['active_users'] = active_users

    no_active_users = User.objects.filter(active=False)
    no_active_users = DeletedUserTable(no_active_users, admin = True)
    RequestConfig(request).configure(no_active_users)
    context['no_active_users'] = no_active_users
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
        form = UserUpdateForm(request.POST, instance=user)
        password = request.POST.get('password')
        if not password:
                # Če je polje gesla prazno, nastavi na neko privzeto vrednost
                request.POST = request.POST.copy()
                request.POST['password'] = user.password
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            
        else:
            messages.error(request,form.errors)  
            return redirect('edit_user',user_id)
        #Preveri če urejaš samega sebe:
        if user_id == context['id']:
                request.session['uporabnik'] = form.data['username']
        messages.success(request,"User details successfully updated.")     
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
    else: #GET
        messages.error(request, '')
        form = UserUpdateForm(instance=user)
        if not context['admin']:
            form.fields.pop('admin_user')
        context['form'] = form
        context['id_delete'] = user.id
        return render(request, 'edit_user.html', context)
    


def edit_deleted_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = get_context(request)
    if request.method == 'POST':
        # Tukaj dodajte logiko za posodobitev podatkov uporabnika
        user.active = True
        user.save()
        messages.success(request,"User " + user.username + " successfully reactivated.")
        return redirect("home")
        
    else:#GET
        form = UserRegisterForm(instance=user)    
        if not context['admin']:
            form.fields['admin_user'].widget.attrs['disabled'] = True

        context['form'] = form
        context['id_delete'] = user.id
        return render(request, 'edit_deleted_user.html', context)
    
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    # Preverimo ali je user v katerem projektu:
    projects = ProjectMember.objects.filter(user=user)
    if len(projects) > 0:
        messages.error(request,"User is member of at least one project!")
        return redirect(edit_user,user_id)
    user.active = False
    user.save()
    messages.success(request,"User " + user.username + " successfully deactivated.")
    return redirect("home")

def new_project(request):  
     if request.method == 'POST':
        # Project.objects.all().delete()
        form = ProjectForm(request.POST)
        if form.is_valid(): 
            name = form.data['name']
            existing_project = Project.objects.filter(name=name).first()
            if existing_project:
                messages.error(request,"Project with this name already exists!")
                return redirect(request.path)
            else:
                #form.save()
                request.session["forma"] = request.POST# v assign_roles jo shranimo, ker neželimo da se ustvari prej
                # treba je shranit celo POST metodo ker ima zraven token za validacijo
                #TUKAJ NE IZPISUJ ŠE MESSAGE.SUCESS !
                return redirect(reverse('add_members',kwargs={'ime_projekta': name}))
        else:
            messages.error(request, form.errors)
            return redirect(request.path)
     else:#GET
        context = get_context(request)
        user = User.objects.get(username = context['user1'])
        all_users = User.objects.filter(active=True)
        context['form'] = ProjectForm(initial={'creator': user}) 
        # context['formAssignment'] = RoleAssignmentForm()
        context['allusers'] = all_users
        return render(request,'new_project.html',context=context)
     
def add_members(request,ime_projekta):
    if request.method == 'POST':
        project_members = request.POST.getlist('project_members')
        request.session["project_members"] = project_members
        if len(project_members) < 2: #MORAŠ IZBRATI VSAJ ENEGA!
            messages.error(request,"You must select at least two members!")
            return redirect(request.path)
        else:
            #TUKAJ TUDI NE MESSAGE.SUCESS
            return redirect(reverse('assign_roles',kwargs={'ime_projekta': ime_projekta}))
    else:
        context = get_context(request)
        all_users = User.objects.filter(active=True)
        context['project_name'] =  ime_projekta
        context['allusers'] = all_users
        return render(request,'add_members.html',context=context)
     
def assign_roles(request,ime_projekta):
    context = get_context(request)
    if request.method == 'POST':
        data = request.session.get("forma")
        forma = ProjectForm(data)
        product_owner_id = request.POST.get('product_owner')
        methodology_manager_id = request.POST.get('methodology_manager')
        development_team_members = request.POST.getlist('development_team_members')
        # Pred shranjevanjem preverimo ali je product owner še kje drugje
        if (product_owner_id == methodology_manager_id) or (product_owner_id in development_team_members):
            messages.error(request, "The Product Owner cannot be the Scrum Master or part of the Development Team!")
            return redirect(request.path)
        

        #Podatki so ok
        forma.save()#to mal kasnej?
        #
        project1 = Project.objects.get(name=ime_projekta)

        existing_project = Project.objects.get(name=ime_projekta)
        if existing_project:
            for member in request.session.get("project_members"):
                u1 = User.objects.get(id = member)
                nov = ProjectMember.objects.create(user = u1,project = project1)
                nov.save()
            if context['id'] not in request.session.get("project_members"): #CREATORJA NASTAVI AVTOMATSKO KOT ČLANA
                try:
                    u1 = User.objects.get(id = context['id'])
                    nov = ProjectMember.objects.create(user = u1,project = project1)
                    nov.save()
                except:
                    pass
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
            messages.success(request,"Project added successfully!")    
            return redirect('project_name',project_name=ime_projekta)
        else:#Mislim da do sem ne bi smelo pridet, ampak če imate idejo napište
            #TODO NEVEM KAJ TUKAJ
            messages.error(request,"Ojoj, Napaka!")
            return redirect(request.path)
    else:
        
        all_users = User.objects.filter(active=True)
        project_members1 = request.session.get("project_members")
        project_members = [User.objects.get(id = user_id) for user_id in project_members1]
        context['project_members'] = project_members
        context['project_name'] =  ime_projekta
        context['allusers'] = all_users
        return render(request,'assign_roles.html',context=context)
    
def edit_assign_roles(request,ime_projekta):
    all_users = User.objects.filter(active=True)
    project = Project.objects.get(name=ime_projekta)
    project_members1 = ProjectMember.objects.filter(project=project)
    project_members = [User.objects.get(id = obj.user.id) for obj in project_members1]
    methodology_manager_role = AssignedRole.objects.get(project = project,role = 'methodology_manager')
    methodology_manager = methodology_manager_role.user
    product_owner_role = AssignedRole.objects.get(project = project,role = 'product_owner')
    product_owner = product_owner_role.user
    development_team_members_roles = AssignedRole.objects.filter(project = project,role = 'development_team_member')
    development_team_members = [obj.user for obj in development_team_members_roles]
    if request.method == 'POST':
        # preverimo kateri podatki se razlikujejo in jih spremenimo 
        product_owner_new = request.POST.get('product_owner')
        methodology_manager_new = request.POST.get('methodology_manager')
        development_team_members_new = request.POST.getlist('development_team_members')
        if (product_owner_new == methodology_manager_new) or (product_owner_new in development_team_members_new):
            messages.error(request, "The Product Owner cannot be the Scrum Master or part of the Development Team!")
            return redirect(request.path)
        u = User.objects.get(id = product_owner_new)
        product_owner_role.user = u
        product_owner_role.save()
        
        u = User.objects.get(id = methodology_manager_new)
        methodology_manager_role.user = u
        methodology_manager_role.save()
        
        development_team_members_new = [User.objects.get(id = obj_id) for obj_id in development_team_members_new]
        # Pogledamo če kakega starega ni v novih -> tega moremo zbrisati
        for obj in development_team_members_roles:
            if obj.user not in development_team_members_new:
                obj.delete()
        # Dodamo še nove:
        for user in development_team_members_new:
            print(user)
            if user not in development_team_members:
                print(user)
                nov = AssignedRole.objects.create(project = project,user = user,role = 'development_team_member')
                nov.save()
        messages.success(request,"Project roles successfully updated.")
        return redirect('project_edit',project_name= ime_projekta)
        
        
    else:#GET
        # methodology_manager,product_owner,project_members
        context = get_context(request)
        context['methodology_manager'] = methodology_manager
        context['product_owner'] = product_owner
        context['development_team_members'] = development_team_members
        context['project_members'] = project_members
        context['project_name'] =  ime_projekta
        context['allusers'] = all_users
        return render(request,'assign_roles_edit.html',context=context)

def project_view(request,project_name):
    context = get_context(request)
    project = Project.objects.get(name=project_name)
    user = User.objects.get(id = context['id'])
    sprints = Sprint.objects.filter(project=project)
    user_stories = UserStory.objects.filter(project=project)
    product_owner = AssignedRole.objects.get(project = project,role = 'product_owner').user
    methodology_manager = AssignedRole.objects.get(project = project,role = 'methodology_manager').user
    form = ProjectDisabledForm(instance=project)
    is_creator = (project.creator.id == context['id'])
    context['new_user_story_enabled'] = (user.admin_user or (user == methodology_manager or user == product_owner))
    context['project'] = project
    context['form'] = form
    context['is_creator'] = is_creator
    context['editable'] = (user.admin_user or (user == methodology_manager))
    context['sprints'] = (sprints)
    user_story_table = UserStoryTable(user_stories, admin = context['admin'],user_id = context['id'])
    RequestConfig(request).configure(user_story_table)
    context['user_story_table'] = user_story_table
    
    sprint_tables = []
    for sprint in sprints:
        userstories = UserStory.objects.filter(project=project, sprint=sprint)
        deleteable = False
        print(len(userstories))
        if len(userstories) == 0:
            deleteable = True
        # sprint_table = SprintTable([sprint])
        userstory_table = UserStoryTable(userstories, admin = context['admin'],user_id = context['id'])
        sprint_tables.append((sprint, userstory_table, deleteable))
    context['sprint_tables'] = sprint_tables
    Backlog = UserStory.objects.filter(project=project, sprint=None)
    Backlog = UserStoryTable(Backlog, admin = context['admin'],user_id = context['id'])
    context['Backlog'] = Backlog
    methodology_manager = AssignedRole.objects.get(project = project, role = 'methodology_manager')
    # methodology_manager = User.objects.get(id = methodology_manager)

    if (methodology_manager.user.id == context['id']) or context['admin']:
        context['create_sprint'] = True
    else:
        context['create_sprint'] = False
        

    return render(request, 'project.html', context)

def project_edit(request,project_name):
    project = Project.objects.get(name=project_name)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            project_name = form.cleaned_data['name']
            messages.success(request,"Project details successfully updated.")
            return redirect('project_name',project_name=project_name)
        else:
            messages.error(request,form.errors)
            return redirect(request.path)
    else:
        context = get_context(request)
        context['project'] = project
        methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
        form = ProjectForm(instance=project)
        all_users = User.objects.filter(active=True)
        project_members1 = ProjectMember.objects.filter(project=project)
        project_members = [User.objects.get(id = obj.user.id) for obj in project_members1]
        users_to_add = [user for user in all_users if user not in project_members]

        context['allusers'] = all_users
        context['project_members'] = project_members
        context['users_to_add'] = users_to_add
        context['form'] = form
        return render(request, 'project_edit.html', context)
    
def add_member_to_project(request,project,user_id):
    # member_id = request.POST.get('add_member') 
    user = User.objects.get(id=user_id)
    project = Project.objects.get(name = project)
    nov = ProjectMember.objects.create(project = project,user = user)
    nov.save()
    messages.success(request,"Member added successfully.")
    return redirect('project_edit',project_name = project)

def remove_member(request,project,user):
    # product_owner_id = request.POST.get('add_member') 
    project = Project.objects.get(name = project)
    user = User.objects.get(id=user)
    #Preverimo če ima kakšen role, če ga ima vrni napako da mora najprej mu odstraniti role!!
    assigned_roles = AssignedRole.objects.filter(project = project,user=user)
    if assigned_roles:
        messages.error(request,"You cannot remove the member as they have an assigned role. First remove their role, then you can remove them!")
        return redirect('project_edit',project_name = project)
    nov = ProjectMember.objects.get(project = project.id,user = user.id)
    nov.delete()
    messages.success(request,"Member removed successfully.")
    return redirect('project_edit',project_name = project)

def delete_project(request,project_name):
    context = get_context(request)
    project = Project.objects.get(name = project_name)
    methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
    if (methodology_manager.id != context['id'] and not context['admin']):
        messages.error(request,"To pa ne bo šlo! Nisi admin ali methodology manager!")
        return redirect('home')
    else:
        project.delete()
        messages.success(request,"Project deleted successfully!")
        return redirect('home')


def check_sprint_dates(start_date, end_date, duration, sprints, sprint_id=-1):
    start = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
    end = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
    # Preveri za primer, ko je končni datum pred začetnim.
    if start > end:
        return False

    # Preveri za primer, ko je začetni datum v preteklosti.
    if start < timezone.now():
        return False

    # Preveri za neregularno vrednost hitrosti Sprinta.
    if start + timezone.timedelta(days=int(duration)) != end:
        return False
    
    # Preveri za primer, ko se dodani Sprint prekriva s katerim od obstoječih.
    for sprint in sprints:
        if sprint_id == sprint.id:
            continue
        #sprint_start_date = datetime.strptime(sprint.start_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
        sprint_start = datetime.combine(sprint.start_date, time()).replace(tzinfo=timezone.get_current_timezone())
        #sprint_start = timezone.make_aware(sprint_start, timezone.get_current_timezone())
        #print(type(sprint.end_date))
        #sprint_end_date = datetime.strptime(sprint.end_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
        sprint_end = datetime.combine(sprint.end_date, time()).replace(tzinfo=timezone.get_current_timezone())
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
            print(type(start_date))
            end_date = request.POST.get('end_date')
            duration = request.POST.get('duration')
            sprints = Sprint.objects.filter(project=project)
            if not check_sprint_dates(start_date, end_date, duration, sprints):
                return JsonResponse({'message': 'Sprint dates are not regular'}, status=400)
            sprint = Sprint.objects.create(project=project, start_date=start_date, end_date=end_date)
            sprint.save()
            return redirect('project_name', project_name=project_name)#JsonResponse({'message': 'Sprint created successfully'})
        except Project.DoesNotExist:
            return JsonResponse({'message': 'Project does not exist'}, status=404)
        except Exception as e:
            print(e)
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
            show_edit = True
            #check if sprint has already started, if it has, disable the edit button
            sprint_start = datetime.combine(sprint.start_date, time()).replace(tzinfo=timezone.get_current_timezone())
            if sprint_start < timezone.now():
                print("Sprint has already started")
                show_edit = False
            #context['show_edit'] = show_edit
            #print(context)
            context = get_context(request)
            context['sprint'] = sprint
            context['project_name'] = project_name
            context['show_edit'] = show_edit
            
            # context={'sprint': sprint, 'project_name': project_name, 'show_edit': show_edit}
            return render(request, 'sprint_details.html', context )
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
    all_users = User.objects.filter(active=True)
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

            project = Project.objects.get(name=project_name)
            sprints = Sprint.objects.filter(project=project)
            print("CHECK")
            if check_sprint_dates(start_date, end_date, duration, sprints, sprint_id):
                sprint.save()
                print(sprint)
                return redirect('sprint_details', project_name=project_name, sprint_id=sprint_id)
            else:
                messages.error(request,"Neveljavna sprememba datuma oz. dolžine sprinta!")
                return redirect(request.path)
        except Sprint.DoesNotExist:
            return JsonResponse({'message': 'Sprint does not exist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)
        

def delete_sprint(request,id,project):
    if request.method == 'POST':
        sprint = Sprint.objects.get(id = id)
        sprint.delete()
        return redirect(request.path) 
    return redirect('/project/'+project) 
        
def wall(request, project_name):
    context = get_context(request)
    project = Project.objects.get(name=project_name)
    context['project'] = project
    if request.method == "POST":
        form = ProjectWallForm(request.POST)
        if form.is_valid():
            current_datetime = timezone.localtime()

            form.instance.project_id = project.id
            form.instance.post_id = context['id']
            form.instance.post_date = current_datetime

            form.save()
            return redirect(request.path) 
        else:
            messages.error(request, "Add text!")
            #return redirect(request.META.get('HTTP_REFERER', '/'))
            return redirect(request.path)
            #return render(request, 'project.html', {'form': form})
    else:
        posts = ProjectWall.objects.filter(project=project)
        context['posts'] = (posts)
        return render(request, "wall.html", context=context)

        
# User story
# ======================================================
def new_user_story(request, project_name):
    context = get_context(request)
    project = Project.objects.get(name = project_name)
    methodology_manager = AssignedRole.objects.filter(project = project, user=context['id'],role = 'methodology_manager')
    product_owner = AssignedRole.objects.filter(project = project, user=context['id'],role = 'product_owner')
    development_team_member = AssignedRole.objects.filter(project = project, user=context['id'],role = 'development_team_member')
    user = User.objects.get(username = context['user1'])
    all_users = User.objects.filter(active=True)
    if request.method == "POST":
        form = UserStoryForm(request.POST, initial={'creator': user, 'project':project})
        if form.is_valid():
            instance = form.save() 
            messages.success(request, f"User story \"{instance.name}\" created!!")
            return redirect('project_name', project_name=project_name)
        else:
            messages.error(request, form.errors)
            return redirect(request.path)
    else:
        form = UserStoryForm(initial={'creator': user, 'project':project})
        if product_owner or methodology_manager:
            form.fields['workflow'].disabled = True
            form.fields['sprint'].disabled = True
            form.fields['size'].disabled = True
            form.fields['original_estimate'].disabled = True
            form.fields['user'].disabled = True
        context['form'] = form
        context['allusers'] = all_users
        context['project'] = project
        return render(request,'new_user_story.html',context=context)
    
def edit_user_story(request, project_name, id):
    context = get_context(request)
    project = Project.objects.get(name = project_name)
    user_story = UserStory.objects.get(id=id)
    form = UserStoryForm(instance=user_story, initial={'project':project})
    methodology_manager = AssignedRole.objects.filter(project = project, user=context['id'],role = 'methodology_manager')
    product_owner = AssignedRole.objects.filter(project = project, user=context['id'],role = 'product_owner')
    development_team_member = AssignedRole.objects.filter(project = project, user=context['id'],role = 'development_team_member')
    if request.method == "POST":
        form = UserStoryForm(request.POST, instance=user_story)
        if form.is_valid():
            if not methodology_manager:
                if form.cleaned_data['original_estimate'] != user_story.original_estimate:
                    messages.error(request, "Original estimate can be provided only by Scrum Master")
                    return redirect('project_name', project_name=project_name)
                if form.cleaned_data['sprint'] != user_story.sprint:
                    messages.error(request, "User story can be added to sprint only by Scrum Master")
                    return redirect('project_name', project_name=project_name)
            if methodology_manager or product_owner:
                if user_story.sprint is None:
                    form.save() 
                    messages.success(request, f"User story \"{user_story.name}\" updated!!")
                    return redirect('project_name', project_name=project_name)
                else:
                    messages.error(request, f"User story \"{user_story.name}\" can't be updated, because it is already in current sprint!!")
                    return redirect('project_name', project_name=project_name)
            else:
                messages.error(request, "User story can be updated only by Product Owner or Scrum Master")
                return redirect(request.path)
        else:
            messages.error(request, form.errors)
            return redirect(request.path)
    print(user_story.sprint)
    if user_story.sprint is not None:
        if product_owner:
            form.fields['name'].disabled = True
            form.fields['description'].disabled = True
            form.fields['priority'].disabled = True
            form.fields['business_value'].disabled = True
            form.fields['acceptance_tests'].disabled = True
            form.fields['workflow'].disabled = True
            form.fields['sprint'].disabled = True
            form.fields['size'].disabled = True
            form.fields['original_estimate'].disabled = True
            form.fields['user'].disabled = True
        elif development_team_member:
            form.fields['name'].disabled = True
            form.fields['description'].disabled = True
            form.fields['priority'].disabled = True
            form.fields['business_value'].disabled = True
            form.fields['acceptance_tests'].disabled = True
            form.fields['sprint'].disabled = True
            form.fields['size'].disabled = True
            form.fields['original_estimate'].disabled = True
            form.fields['user'].disabled = True
        elif methodology_manager:
            form.fields['name'].disabled = True
            form.fields['description'].disabled = True
            form.fields['priority'].disabled = True
            form.fields['business_value'].disabled = True
            form.fields['acceptance_tests'].disabled = True
            form.fields['workflow'].disabled = True
            form.fields['sprint'].disabled = True
            form.fields['size'].disabled = True
            form.fields['original_estimate'].disabled = True
            form.fields['user'].disabled = True
    else:
        print(methodology_manager)
        if development_team_member and methodology_manager:
            pass
        elif product_owner:
            form.fields['workflow'].disabled = True
            form.fields['sprint'].disabled = True
            form.fields['size'].disabled = True
            form.fields['original_estimate'].disabled = True
            form.fields['user'].disabled = True
        elif development_team_member:
            form.fields['name'].disabled = True
            form.fields['description'].disabled = True
            form.fields['priority'].disabled = True
            form.fields['business_value'].disabled = True
            form.fields['acceptance_tests'].disabled = True
            form.fields['workflow'].disabled = True
            form.fields['sprint'].disabled = True
            form.fields['size'].disabled = True
            form.fields['original_estimate'].disabled = True
            form.fields['user'].disabled = True
        elif methodology_manager:
            form.fields['workflow'].disabled = True
    context['form'] = form
    context['project'] = project
    return render(request,'new_user_story.html',context=context)

def delete_user_story(request, project_name, id):
    context = get_context(request)
    user_story = UserStory.objects.get(id=id)
    user_story_name = user_story.name
    project = Project.objects.get(name = project_name)
    methodology_manager = AssignedRole.objects.filter(project = project, user=context['id'],role = 'methodology_manager')
    product_owner = AssignedRole.objects.filter(project = project, user=context['id'],role = 'product_owner')
    print(user_story.sprint)
    if request.method == "POST":
        if methodology_manager or product_owner:
            if user_story.sprint is None:
                user_story.delete()
                messages.success(request, f"User story \"{user_story_name}\" deleted successfully!!")
                return redirect('project_name', project_name=project_name)
            else:
                messages.error(request, f"User story \"{user_story.name}\" can't be deleted, because it is already in current sprint!!")
                return redirect('project_name', project_name=project_name)
        else:
            messages.error(request, "User story can be deleted only by Product Owner or Scrum Master")
            return redirect('project_name', project_name=project_name)
    context["user_story_id"] = user_story.id
    context["user_story_name"] = user_story.name
    context["project_name"] = project.name
    return render(request, 'delete_user_story.html', context=context)


