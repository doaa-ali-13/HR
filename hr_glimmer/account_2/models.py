from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    is_superadmin = models.BooleanField(default=False, help_text=_("Designates whether the user can manage all companies and their employees."))
    is_companyadmin = models.BooleanField(default=False, help_text=_("Designates whether the user can manage a specific company and its employees."))
    is_employee = models.BooleanField(default=False, help_text=_("Designates whether the user is an employee of a company."))

class Company(models.Model):
    INDUSTRY_CHOICES = (
        ('tech', _('Technology')),
        ('health', _('Healthcare')),
        ('finance', _('Finance')),
        ('education', _('Education')),
        ('manufacturing', _('Manufacturing')),
        # Add more industries as needed
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile', null=True, blank=True)
    company_name = models.CharField(max_length=255, help_text=_("The name of the company."))
    location = models.CharField(max_length=255, help_text=_("The physical location of the company."))
    industry = models.CharField(max_length=100,choices=INDUSTRY_CHOICES, help_text=_("The industry the company operates in."))
    size = models.IntegerField(help_text=_("The number of employees in the company."))
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field
    temp_email = models.EmailField(blank=True, null=True)
    temp_password_hash = models.CharField(max_length=128, blank=True, null=True)  # Store hashed passwords only
    def __str__(self):
        return self.company_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', help_text=_("The user associated with this employee."))
    first_name = models.CharField(max_length=255, help_text=_("The first name of the employee."))
    last_name = models.CharField(max_length=255, help_text=_("The last name of the employee."))
    position = models.CharField(max_length=100, help_text=_("The job position of the employee."))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')


    def __str__(self):
        return self.user.get_full_name() or self.user.username
