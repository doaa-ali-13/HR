from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from .forms import SuperAdminSignUpForm, CompanyAdminSignUpForm, EmployeeSignUpForm, LoginForm, CompanyRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from .models import Company

from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from .utils import generate_verification_token, verify_token

owner_email = 'doaa34333@gmail.com'

def superadmin_check(user):
    return user.is_authenticated and user.is_superadmin

def companyadmin_check(user):
    return user.is_authenticated and user.is_companyadmin






@user_passes_test(companyadmin_check)
def employee_signup(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            token = generate_verification_token(email)
            verification_url = request.build_absolute_uri(reverse('verify_email', args=[token]))
            try:
            # Send verification email
                send_mail(
                    'Email Verification',
                    f'Click the link to verify your email: {verification_url}',
                    'no-reply@example.com',
                    [email]
                )
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
            company = request.user.company_profile
            user = form.save(commit=True, company=company)
            login(request, user)  # Automatically log in the employee
            context = {'user':user, 'company':company}
            return  redirect('verifyEmail')
    else:
        form = EmployeeSignUpForm()
    return render(request, 'account_2/empReg.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
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
                    return HttpResponseForbidden("On progress...")
            else:
                return render(request, 'account_2/login.html',  {'form': form, 'error': 'Invalid credentials'})
        else:
            return redirect('user_login')
    else:
        form = LoginForm()  # Ensure this form is correctly defined in forms.py
        return render(request, 'account_2/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
@user_passes_test(companyadmin_check)
def dashboard(request):
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
            customer_email = request.POST['email']
            company_name = request.POST['company_name']
            phone_number = request.POST['phone_number']
            # Future: handle user creation here
            company = form.save(commit=False)
            # Placeholder for user creation logic
            # User creation and association would go here
            company.save()
            try: 
                send_mail(
                subject='Order Confirmation',
                message=f'Dear {company_name}, thank you for your interest in our srvices. we will catch with you as soon as possible! ',
                from_email='no-reply@example.com',
                recipient_list=[customer_email],
                fail_silently=False,
                )
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
            # Email 2: Notification to the owner
            email_to_owner = EmailMessage(
                subject='New Order Notification',
                body=f'A new demo has been requested from {company_name} with these contact info: phone: {phone_number}/ email: {customer_email}.',
                from_email='no-reply@example.com',
                to=[owner_email]
            )
            try:
                email_to_owner.send()
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
            return  redirect('companymessageRegister')
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

def CompetencyLibraries(request):
    return render(request, 'account_2/Competency.html')

def Pricing(request):
    return render(request, 'account_2/pricing.html')

def verify_email(request, token):
    email = verify_token(token)
    if email:
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user.is_active = True  # Activate the user's account
            user.save()
            return  redirect('verificationDone')
        except User.DoesNotExist:
            return render(request, 'account_2/verification_failed.html')
    else:
        return render(request, 'account_2/verification_failed.html')


def verifyEmail(request):
    return HttpResponseForbidden('please verify your email!')        

def verificationDone(request):
    return HttpResponseForbidden('your email has been verified!')        

def companymessageRegister(request):
     return HttpResponseForbidden('we got your request, we will catch with yiu later!')    