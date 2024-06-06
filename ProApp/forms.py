from django import forms
from .models import UserProfile , Project , Employee , Role , UserEmployeeMapping
from django.contrib.auth.forms import UserChangeForm 
from django.contrib.auth.models import User 

class RoleForm(forms.ModelForm):
    class Meta: 
        model = Role
        fields = '__all__'
        
        
class CustomUserChangeForm(UserChangeForm):
    employeeID = forms.CharField(max_length=150, required=False)
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    group = forms.ChoiceField(choices=Role.GROUP_CHOICES)

    class Meta:
        model = UserProfile
        fields = ('user' , 'role' , 'employeeID' , 'group')  
        
class CustomEmployeeChangeForm(UserChangeForm):
    username = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Employee
        fields = ('Fullname' , 'adress' , 'service' , 'Email')  

class CustomProjectChangeForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
        
class CustomRoleChangeForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'       

class UserProfileForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    role = forms.ModelChoiceField(label='Role' , queryset=Role.objects.all())
    employeeID = forms.ModelChoiceField(label='Employee ID' , queryset=Employee.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
    
    def save(self):
        # Extract data from the form
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        employeeID = self.cleaned_data['employeeID']
        role = self.cleaned_data['role']

        # Create a new user
        user = User.objects.create_user(username=username, password=password)

        # Create UserProfile with the selected Employee and Role
        user_profile = UserProfile.objects.create(user=user, employeeID=employeeID, role=role)

        return user_profile
    
class UserEmployeeMappingForm(forms.ModelForm):
    class Meta:
        model = UserEmployeeMapping
        fields = ['user', 'employee'] 
        

# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         model = Project
#         fields = ['project_code', 'project_name', 'customer', 'end_user',
#                 'project_currency', 'currency_rate', 'payment_terms',
#                 'project_manager', 'company', 'address_line_1', 'address_line_2',
#                 'mobile', 'email', 'initial_so_value', 'change_order_1' ,'change_order_2',
#                 'change_order_3' , 'change_order_4' , 'total_so' , 'bid_bom_price' , 'bid_cogs' ,
#                 'bid_va' , 'design_cogs', 'design_va' , 'running_cogs' , 'running_va' 
#                 ]       

#     def clean(self):
#         cleaned_data = super().clean()  # Get cleaned data from parent
#         change_order_1 = cleaned_data.get('change_order_1', 0)
#         change_order_2 = cleaned_data.get('change_order_2', 0)
#         change_order_3 = cleaned_data.get('change_order_3', 0)
#         change_order_4 = cleaned_data.get('change_order_4', 0)
#         cleaned_data['total_so'] = change_order_1 + change_order_2 + change_order_3 + change_order_4
#         return cleaned_data