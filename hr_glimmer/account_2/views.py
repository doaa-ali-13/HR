from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SuperAdminSignUpForm, CompanyAdminSignUpForm, EmployeeSignUpForm, LoginForm, CompanyRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from .models import Company




def superadmin_check(user):
    return user.is_authenticated and user.is_superadmin

def companyadmin_check(user):
    return user.is_authenticated and user.is_companyadmin




def superadmin_signup(request):
  
    if request.method == 'POST':
        form = SuperAdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the superadmin
            return redirect('/admin/')
    else:
        form = SuperAdminSignUpForm()
    return render(request, 'account_2/register.html', {'form': form})


@user_passes_test(superadmin_check)
def companyadmin_signup(request):
    if not request.user.is_authenticated or not request.user.is_superadmin:
        return HttpResponseForbidden("Only super admins can access this page.")

    if request.method == 'POST':
        form = CompanyAdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the company admin
            company = user.company_profile
            employees = company.employees.all()  # Using the 'employees' related_name from the Company model
            print('========',employees, company)
            context = {'user':user, 'employees':employees, 'companyName': company.company_name}
            return render(request, 'account_2/HrDash.html', context)
    else:
        form = CompanyAdminSignUpForm()
    return render(request, 'account_2/HrReg.html', {'form': form})


@user_passes_test(companyadmin_check)
def employee_signup(request):
    
    if not request.user.is_authenticated or not request.user.is_companyadmin:
        return HttpResponseForbidden("Only company admins can access this page.")

    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            company = request.user.company_profile
            user = form.save(commit=True, company=company)
            login(request, user)  # Automatically log in the employee
            context = {'user':user, 'company':company}
            return render(request, 'account_2/employee.html',context)
    else:
        form = EmployeeSignUpForm()
    return render(request, 'account_2/empReg.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superadmin:
                    return redirect('/admin/')
                elif user.is_companyadmin:
                    company = user.company_profile
                    employees = company.employees.all()  # Using the 'employees' related_name from the Company model
                    print('========',employees, company.id)
                    context = {'user':user, 'employees':employees.count(), 'companyName': company, 'company_id':company.id}
                    return redirect('dashboard')
                elif user.is_employee:
                    return redirect('dashboard')
                else:
                    return redirect('dashboard')
            else:
                return render(request, 'account_2/login.html',  {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'account_2/login.html', {'form': form})
    else:
        form = LoginForm()  # Ensure this form is correctly defined in forms.py
        return render(request, 'account_2/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')

def dashboard(request):
    if not request.user.is_authenticated or not request.user.is_companyadmin:
        return HttpResponseForbidden("Only company admins can access this page.")
    user = request.user
    company = user.company_profile
    employees = company.employees.all() 
    context = {'user':user, 'employees':employees.count(), 'companyName': company, 'company_id':company.id}
    return render(request, 'account_2/HrDash.html', context)


def index(request):
    return render(request, 'account_2/index.html')

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            # Future: handle user creation here
            company = form.save(commit=False)
            # Placeholder for user creation logic
            # User creation and association would go here
            company.save()
            return  HttpResponseForbidden("We recieve you request, we will catch with you later!")
    else:
        form = CompanyRegistrationForm()

    return render(request, 'account_2/HrReg.html', {'form': form})

def employee(request):
    user_id = request.GET.get('user_id', 'default_value')
    # Use the user_id as needed
    company = Company.objects.get(id=user_id)
    employees = company.employees.all()
    print(employees)
    return render(request, 'account_2/employee.html', {'employees': employees})
