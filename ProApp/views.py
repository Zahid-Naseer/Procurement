from django.shortcuts import render , redirect
from ProApp.models import Project  , UserProfile , Employee , Role , UserEmployeeMapping
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404
from .forms import UserProfileForm
from django.db import IntegrityError
from django.contrib import messages
from django.dispatch import receiver
from ProApp.forms import CustomUserChangeForm , CustomProjectChangeForm , CustomEmployeeChangeForm , RoleForm , CustomRoleChangeForm , UserEmployeeMappingForm 
#from .forms import UserEditForm

# Create your views here.
@login_required
def projects(request):
    projects = Project.objects.all()
    users = User.objects.all()
    
    context = {
        'projects': projects,
        'users' : users
    }
    return render(request , 'projects.html' , context)

@login_required
def projects_desc(request , projects_id):   
    project = get_object_or_404(Project, id=projects_id)

    context = {'project': project}
    return render(request, 'projects_desc.html' , context)

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    context ={
        'project' : project,
    }
    return render(request, 'project_detail.html', context)

@login_required
def newProject(request):
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_code = request.POST.get('project_code')
        customer = request.POST.get('customer')
        end_user = request.POST.get('end_user')
        project_currency = request.POST.get('project_currency')
        currency_rate = request.POST.get('currency_rate')
        payment_terms = request.POST.get('payment_terms')
        project_manager = request.POST.get('project_manager')
        company = request.POST.get('company')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        initial_so_value = request.POST.get('initial_so_value')
        change_order_1 = request.POST.get('change_order_1')
        change_order_2 = request.POST.get('change_order_2')
        change_order_3 = request.POST.get('change_order_3')
        change_order_4 = request.POST.get('change_order_4')
        total_so = request.POST.get('total_so')
        bid_bom_price = request.POST.get('bid_bom_price')
        bid_cogs = request.POST.get('bid_cogs')
        bid_va = request.POST.get('bid_va')
        design_cogs = request.POST.get('design_cogs')
        design_va = request.POST.get('design_va')
        running_cogs = request.POST.get('running_cogs')
        running_va = request.POST.get('running_va')

        data = Project(
            project_name=project_name ,
            project_code=project_code ,
            customer=customer,
            end_user=end_user,
            project_currency=project_currency,
            currency_rate=currency_rate,
            payment_terms = payment_terms,
            project_manager= project_manager,
            company= company,
            address_line_1= address_line_1,
            address_line_2= address_line_2,
            mobile= mobile,
            email= email,
            initial_so_value= initial_so_value,
            change_order_1= change_order_1,
            change_order_2= change_order_2,
            change_order_3= change_order_3,
            change_order_4= change_order_4,
            total_so= total_so,
            bid_bom_price=bid_bom_price,
            bid_cogs =bid_cogs,
            bid_va =bid_va,
            design_cogs =design_cogs,
            design_va =design_va,
            running_cogs =running_cogs,
            running_va = running_va ,
            )
        data.save()


    return render(request, 'newProject.html' )


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    context = {user_profile : 'userprofile' , }
    return render(request, 'role/admin_dashboard.html' , context)

@login_required
@user_passes_test(lambda u: u.userprofile.role.full_access)
def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Check for existing username before saving the form
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username "%s" already exists. Please choose a different username.' % username)
                return render(request, 'register.html', {'form': form})

            form.save()
            return redirect('users')  # Redirect to a success page
    else:
        form = UserProfileForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'Username or Password is Invalid')
            return render(request, 'login.html',)

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_projects_desc(request , projects_id):
    project = get_object_or_404(Project , id=projects_id)
    form = CustomProjectChangeForm(instance=project)
    
    if request.method == 'POST':
        form = CustomProjectChangeForm(request.POST, instance=project)

        if form.is_valid():
            form.save()

    context = { 
        'project': project,
        'form': form,
    }
            
    return render(request , 'role/edit_projects_desc.html' , context)

@login_required
@user_passes_test(lambda u: u.userprofile.role.full_access)
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Ensure the admin cannot delete their own account
        user_to_delete.delete()
        return redirect('users')

    return redirect('users')

@login_required
def delete_employee(request, employee_id):
    employee_to_delete = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        employee_to_delete.delete()
        return redirect('employee')

    return redirect('employee')

@login_required
def delete_project(request, project_id):
    project_to_delete = get_object_or_404(Project, id=project_id)
    
    if request.user.userprofile.role.full_access:
        # Admin users can delete any project
        project_to_delete.delete()
    
    return redirect('projects')

@login_required
@user_passes_test(lambda u: u.userprofile.role.full_access)
def delete_role(request, role_id):
    role_to_delete = get_object_or_404(Role, id=role_id)

    if request.method == 'POST':
        # Ensure the admin cannot delete their own account
        role_to_delete.delete()
        return redirect('role')

    return redirect('role')


@login_required
def edit_users_desc(request , user_id):
    
    user = get_object_or_404(User, id=user_id)


    return render(request, 'role/edit_users_desc.html', {'user': user} )

@login_required
def users(request):
    users_with_role = User.objects.filter(userprofile__role__isnull=False)
    projects = Project.objects.all()
    
    context = {
        'users' : users_with_role,
        'projects' : projects,
    }
    return render(request , 'users.html' , context)

@login_required
def users_desc(request , user_id):
    
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user.userprofile)


        if form.is_valid():
            username = form.cleaned_data['username']
            if username:
                user.username = username
                user.save
                
            form.save()
    else:
        form = CustomUserChangeForm()
    
    context= {
        'user' : user,    
        'form' : form,
    }
    return render(request , 'role/users_desc.html' , context)


@login_required
def employee(request ):
    employees = Employee.objects.all()
    
    
    context = {
        'employees' : employees,
    }
    
    return render(request , 'employee.html' , context)


def employee_register(request):
    if request.method == 'POST':
        Fullname = request.POST['Fullname']
        adress = request.POST['Adress']
        service = request.POST['Service']
        Email = request.POST['Email']

        try:
            # Try to create a new Employee
            user_profile = Employee(Fullname=Fullname, adress=adress, service=service, Email=Email)
            user_profile.save()
        except IntegrityError:
            # Handle the case where the employeeID already exists
            error_message = "EmployeeID already in use. Please choose a different one."
            return render(request, 'employee_register.html', {'error_message': error_message})
        
        

        return redirect('employee_register')  # Redirect to the dashboard or any other page
    
    return render(request, 'employee_register.html')


def edit_employee_desc(request , employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    return render(request , 'edit_employee_desc.html' , {  'employee': employee})   

@login_required
def employee_desc(request , employee_id):
    
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = CustomEmployeeChangeForm(request.POST, instance=employee.employee)


        if form.is_valid():
            employeeID = form.cleaned_data['id']
            if employeeID:
                employee.id = employeeID
                employee.save
                
            form.save()
    else:
        form = CustomEmployeeChangeForm()
    
    context= {
        'employee' : employee,    
        'form' : form,
    }
    return render(request , 'employee_desc.html' , context) 

@login_required
def new_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role')
    else:
        form = RoleForm()
    return render(request , 'new_role.html' , {'form' : form})

@login_required
def new_role_edit(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    if request.method == 'POST':
        form = CustomRoleChangeForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
    else:
        form = CustomRoleChangeForm(instance=role)

    return render(request, 'new_role_edit.html', {'form': form, 'role': role})

@login_required
def new_role_desc(request , role_id):
    role = get_object_or_404(Role, id=role_id)
    
    context = {
        'role' : role,
    }
    
    return render(request , 'new_role_desc.html' , context)

@login_required
def id_assingment(request):
    if request.method == 'POST':
        form = UserEmployeeMappingForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserEmployeeMappingForm()

    return render(request, 'id_assingment.html', {'form': form})    

@login_required
def mapping(request):
    relations = UserEmployeeMapping.objects.all()
    
    return render(request, 'mapping.html', {'relations': relations})   

@login_required
def role(request):
    roles = Role.objects.all()
    users = User.objects.all()
    
    context = {
        'roles' : roles,
        'users' : users,
    }
    return render(request , 'role.html' , context)


@login_required
def invoice(request):
    return render(request , 'projects/invoice.html')


@login_required
def bom(request):
    return render(request , 'projects/bom.html')

@login_required
def vendor_list(request):
    return render(request , 'projects/vendor_list.html')

@login_required
def vendor_price(request):
    return render(request , 'projects/vendor_price.html')

@login_required
def po_list(request):
    return render(request , 'projects/po_list.html')

@login_required
def po(request):
    return render(request , 'projects/po.html')
