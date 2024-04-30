from django.urls import path
from .views import  employee_signup, user_login, user_logout, dashboard, index, register_company,employee,Pricing, CompetencyLibraries
from .views import  *

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='user_login'),
    path('getdemo/', register_company, name='register_company'),
    path('add-employee/', employee_signup, name='employee_signup'),
    path('employee/', employee, name='employee'),
    path('logout/', user_logout, name='user_logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('Pricing/', Pricing, name='Pricing'),
    path('CompetencyLibraries/', CompetencyLibraries , name='CompetencyLibraries'),
    path('verify_email/<str:token>/', verify_email, name='verify_email'),
    path('verificationDone/', verificationDone, name='verificationDone'),
    path('verifyEmail/', verifyEmail, name='verifyEmail'),
    path('companymessageRegister/', companymessageRegister, name='companymessageRegister'),
]
