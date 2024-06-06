from django.contrib import admin
from django.urls import path 
from ProApp import views

urlpatterns = [
    #DASHBOARD
    path('dashboard' , views.dashboard, name="dashboard"),
    path('new_role' , views.new_role, name="new_role"),
    #log in/out
    path('login', views.user_login, name='login'),
    path('', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    # project majaor
    path('projects' , views.projects, name="projects"),
    path('invoice' , views.invoice, name="invoice"),
    path('bom' , views.bom, name="bom"),
    path('vendor_list' , views.vendor_list, name="vendor_list"),
    path('vendor_price' , views.vendor_price, name="vendor_price"),
    path('po_list' , views.po_list, name="po_list"),
    path('po' , views.po, name="po"),
    #PROJECT list
    path('projects' , views.projects, name="projects"),
    path('newProject' , views.newProject, name="newProject"),
    path('edit_projects_desc/<int:projects_id>/' , views.edit_projects_desc , name="edit_projects_desc"),
    path('projects_desc/<int:projects_id>/' , views.projects_desc, name="projects_desc"), 
    path('project_detail/<int:project_id>/' , views.project_detail, name="project_detail"), 
    #User    
    path('users' , views.users , name="users"), 
    path('register', views.register, name='register'),
    path('users_desc/<int:user_id>/' , views.users_desc , name="users_desc"),
    path('edit_users_desc/<int:user_id>/', views.edit_users_desc, name='edit_users_desc'),
    #DELETE
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('delete_employee/<int:employee_id>/' , views.delete_employee , name="delete_employee"),
    path('delete_role/<int:role_id>/' , views.delete_role , name="delete_role"),
    #Employee
    path('employee' , views.employee , name="employee"),
    path('employee_register' , views.employee_register , name="employee_register"),
    path('edit_employee_desc/<int:employee_id>/' , views.edit_employee_desc , name="edit_employee_desc"),
    path('employee_desc/<int:employee_id>/' , views.employee_desc , name="employee_desc"),
    #Role
    path('new_role_edit/<int:role_id>/' , views.new_role_edit , name="new_role_edit"),
    path('new_role_desc/<int:role_id>' , views.new_role_desc , name="new_role_desc"),
    
    path('role' , views.role , name="role"),
    #Mapping
    path('mapping' , views.mapping , name="mapping"),
    path('id_assingment' , views.id_assingment , name="id_assingment"),

]
