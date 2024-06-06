from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator
# Create your models here.


class Project(models.Model):
    project_code = models.CharField(max_length=25 ,blank=True)
    project_name = models.CharField(max_length=255 , blank=True)
    customer = models.CharField(max_length=255 ,blank=True)
    end_user = models.CharField(max_length=255, blank=True)

    # SO Currency (Dropdown s   election)
    CURRENCY_CHOICES = (
        ('', 'Select Currency'),
        ('SAR', 'Saudi Riyal (SAR)'),
        ('PKR', 'Pakistani Rupee (PKR)'),
        ('USD', 'US Dollar (USD)'),
        # Add more currencies as needed
    )
    project_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='')

    # Set a default value for currency_rate (e.g., 1.00 for USD)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], default=1.00)
    payment_terms = models.PositiveIntegerField(validators=[MinValueValidator(1)] , default=1)  # Minimum payment terms: 1 day

    project_manager = models.CharField(max_length=255 ,blank=True)
    company = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # Monetary fields (consider using a separate model for better organization)
    initial_so_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    change_order_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    change_order_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    change_order_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    change_order_4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    total_so = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)

    bid_bom_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bid_cogs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bid_va = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    design_cogs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    design_va = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    running_cogs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    running_va = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.project_code + " - " + self.project_name





# class Project(models.Model):
#     code = models.CharField(max_length=225, default="1" , unique=True)
#     projectName = models.CharField(max_length=225, default="1")
#     projectDesc = models.TextField(max_length=225, default="1")
#     DateOfStart = models.DateField(blank=True, null=True)  # Adjust the default date as needed
#     DateOfEnd = models.DateField(blank=True, null=True)    # Adjust the default date as needed
#     projectValue = models.FloatField(default=1.0)

#     def __str__(self):
#         return self.projectName    
    
class Employee(models.Model):
    Fullname = models.CharField(default="", max_length=20)
    adress = models.CharField(default="", max_length=20)
    service = models.CharField(default="" , max_length=225)         
    Email = models.EmailField(default="")
    
    def __str__(self):
        return str(self.Fullname)       
      
class Role(models.Model):
    
    GROUP_HR_EMPLOYEE = 'HR'
    GROUP_Procurement = 'Procurement'
    GROUP_Marketing = 'Marketing'
    GROUP_Administrative = 'Administrative'
    GROUP_CHOICES = [
        (GROUP_HR_EMPLOYEE, 'HR'),
        (GROUP_Procurement, 'Procurement'),
        (GROUP_Marketing, 'Marketing'),
        (GROUP_Administrative, 'Administrative'),
    ]
    
    role_name = models.CharField(max_length=255, unique=True)
    group = models.CharField(max_length=22 , choices=GROUP_CHOICES)
    full_access = models.BooleanField(default=False)
    can_view_projects = models.BooleanField(default=False)
    can_edit_projects = models.BooleanField(default=False)
    can_view_employee = models.BooleanField(default=False)
    can_edit_employee = models.BooleanField(default=False)
    can_view_users = models.BooleanField(default=False)
    can_edit_users = models.BooleanField(default=False)
    
    def __str__(self):
        return self.role_name    
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey( Role , on_delete=models.CASCADE)
    employeeID = models.OneToOneField(Employee, default="" , on_delete=models.CASCADE)
    
    #Status = models.BooleanField(default="")

    def __str__(self):
        return str(self.user)
    
class UserEmployeeMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'employee')    


class PageView(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)