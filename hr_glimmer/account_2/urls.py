from django.urls import path
from .views import superadmin_signup, companyadmin_signup, employee_signup, user_login, user_logout, dashboard, index, register_company,employee,Pricing

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='user_login'),
    path('getdemo/', register_company, name='register_company'),
    path('signup/companyadmin/', companyadmin_signup, name='companyadmin_signup'),
    path('add-employee/', employee_signup, name='employee_signup'),
    path('employee/', employee, name='employee'),
    path('logout/', user_logout, name='user_logout'),
    path('signup/superadmin/', superadmin_signup, name='superadmin_signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('Pricing/', Pricing, name='Pricing'),
]
