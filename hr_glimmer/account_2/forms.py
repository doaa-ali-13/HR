from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Company, Employee
from django.contrib.auth.hashers import make_password

class SuperAdminSignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superadmin = True
        user.is_staff = True  # Allow access to the admin site
        user.is_admin = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

class CompanyAdminSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    location = forms.CharField(max_length=255)
    industry = forms.CharField(max_length=100)
    size = forms.IntegerField()
    phone_number = forms.CharField(max_length=15) 
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'company_name', 'location', 'industry', 'size', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_companyadmin = True
        if commit:
            user.save()
            Company.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                location=self.cleaned_data['location'],
                industry=self.cleaned_data['industry'],
                size=self.cleaned_data['size'],
                phone_number=self.cleaned_data['phone_number'],
            )
        return user

class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter first name',
            'id': 'employeeName',
            'required': 'required'
        })
    )
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter last name',
            'id': 'employeeNameLast',
            'required': 'required'
        })
    )
    position = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter position',
            'id': 'position',
            'required': 'required'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'position']
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'form-control',
                'placeholder': 'Username',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'companyEmail',
                'placeholder': 'Email address',
                'required': 'required'
            }),
            'password1': forms.PasswordInput(attrs={
                'id': 'password',
                'placeholder': 'Password',
                'required': 'required'
            }),
            'password2': forms.PasswordInput(attrs={
                'id': 'confirmPassword',
                'placeholder': 'Confirm password',
                'required': 'required'
            })
        }

    def save(self, commit=True, company=None):
        user = super().save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
            Employee.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                position=self.cleaned_data['position'],
                company=company  
            )
        return user


class CompanyRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'id': 'email',
        'name': 'email',
        'placeholder': 'Your company name',
        'required': 'required'
    }))
    password1 = forms.CharField( label="Password",widget=forms.PasswordInput(attrs={
        'id': 'pass1',
        'name': 'pass1',
        'placeholder': 'input your password',
        'required': 'required'
    }))
    password2 = forms.CharField( label="Confirm Password",widget=forms.PasswordInput(attrs={
        'id': 'pass2',
        'name': 'pass2',
        'placeholder': 'verify your password',
        'required': 'required'
    }))

    class Meta:
        model = Company
        fields = ['company_name', 'location', 'industry', 'size', 'phone_number']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'id': 'company-name',
                'name': 'company-name',
                'placeholder': 'Enter company name',
                'class': 'form-control',
                'required': 'required'
            }),
            'location': forms.TextInput(attrs={
                'id': 'location',
                'name': 'location',
                'placeholder': 'Enter company location',
                'class': 'form-control',
                'required': 'required'
            }),
            'industry': forms.Select(attrs={
                'id': 'industry',
                'name': 'industry',
                'class': 'form-control',
                'required': 'required'
            }),
            'size': forms.NumberInput(attrs={
                'id': 'size',
                'name': 'size',
                'placeholder': 'Number of employees',
                'class': 'form-control',
                'required': 'required'
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'phone-number',
                'name': 'phone-number',
                'placeholder': 'Enter phone number',
                'class': 'form-control'
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        return cleaned_data

    def save(self, commit=True):
        company = super().save(commit=False)
        company.temp_email = self.cleaned_data['email']
        company.temp_password_hash = self.cleaned_data['password1']
        
        if commit:
            company.save()
        return company


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'name': 'username',
        'placeholder': 'Your user name',
        'required': 'required'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name': 'password',
        'placeholder': 'Your password',
        'required': 'required'
    }))