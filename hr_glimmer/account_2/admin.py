from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, Employee
from django.contrib.auth.hashers import make_password
from .utils import generate_verification_token, verify_token
from django.urls import reverse
from django.core.mail import send_mail

def create_user_for_company(modeladmin, request, queryset):
    for company in queryset:
        if not company.user and company.temp_email:  # Check if a user does not already exist
            user = User.objects.create(
                username=company.temp_email,
                email=company.temp_email
            )
            user.is_companyadmin = True
            user.is_active = False
            user.set_password(company.temp_password_hash)  # Assuming you have a valid hash stored
            email = user.email
            token = generate_verification_token(email)
            verification_url = request.build_absolute_uri(reverse('verify_email', args=[token]))

            # Send verification email
            send_mail(
                'Email Verification',
                f'Click the link to verify your email: {verification_url}',
                'no-reply@example.com',
                [email]
            )
            user.save()
            company.user = user
            company.temp_email = None
            company.temp_password_hash = None  # Clear temporary data after creating the user
            company.save()
            modeladmin.message_user(request, f"User created for {company.company_name}")

create_user_for_company.short_description = "Create user for selected companies"




class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_superadmin', 'is_companyadmin', 'is_employee']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_superadmin', 'is_companyadmin', 'is_employee')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_superadmin', 'is_companyadmin', 'is_employee')}),
    )

admin.site.register(User, CustomUserAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'location', 'industry', 'size','phone_number','temp_email', 'temp_password_hash']
    search_fields = ['name', 'industry']  # Allow searching by company name and industry
    actions = [create_user_for_company]
admin.site.register(Company, CompanyAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user','first_name', 'last_name', 'position', 'company']
    search_fields = ['user__username', 'user__email', 'position']  # Search by username, email, and position

admin.site.register(Employee, EmployeeAdmin)


