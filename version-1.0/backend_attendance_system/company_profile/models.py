from django.db import models

# Create your models here.
from datetime import datetime

# from employee_profile.models import EmployeeRecord
import employee_profile.models

#company details to which we sell this product
#customers to which we sell this bot
class CompanyDetails(models.Model):
    company_id = models.AutoField(primary_key=True, unique=True)
    company_name = models.CharField(max_length=100)
    company_founding_date = models.DateField(null=True, blank=True)
    company_CIN_num = models.CharField(max_length=20, unique=True)
    company_ceo = models.CharField(max_length=100)
    company_billing_address = models.TextField()
    company_telephone = models.CharField(max_length=20)
    company_email = models.EmailField(max_length=100, default="example@email.com")
    company_logo = models.ImageField(max_length=1500, upload_to='static/master_dataset/')
    company_record = models.DateTimeField(auto_now_add=True)
    company_status = models.BooleanField(default=True) 
    #True == Active status #False == Inactive/Shut down status
    company_record_last_modification = models.DateTimeField(auto_now=True)
    company_alias = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "company_details"
        managed = True

#company's various geogrphically distributed sites/locations
class CompanySites(models.Model):
    site_s_num = models.AutoField(primary_key=True, unique=True)
    company_id = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, null=True, blank=True)
    site_id = models.CharField(max_length=20) 
    #this will be a combination of alpha-numbers representing the site
    site_GST_num = models.CharField(max_length=20, default=0)
    site_name = models.CharField(max_length=50)
    site_address = models.TextField()
    site_telephone = models.CharField(max_length=20)
    site_record = models.DateTimeField(auto_now_add=True)
    site_status = models.BooleanField(default=True)
    #True == Active status #False == Inactive/Shut down status
    site_alias = models.SlugField(max_length=20, unique=True)
    site_record_last_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company_sites"
        managed = True

#company's site incharge
#single site can have multiple incharges simultaneously or at different times
class CompanySiteIncharge(models.Model):
    site_incharge_id = models.AutoField(primary_key=True, unique=True)
    emp_id = models.ForeignKey("employee_profile.EmployeeRecord", on_delete=models.CASCADE)
    site_s_num = models.ForeignKey(CompanySites, on_delete=models.CASCADE)
    site_incharge_from = models.DateField()
    site_incharge_to = models.DateField(null=True, blank=True)
    site_incharge_record = models.DateTimeField(auto_now=True)
    site_incharge_record_last_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company_site_incharge"
        managed = True

#company's dept at 1 particular site
class CompanyDepts(models.Model):
    dept_s_num = models.AutoField(primary_key=True, unique=True)
    site_s_num = models.ForeignKey(CompanySites, on_delete=models.CASCADE)
    dept_id = models.CharField(max_length=20, unique=True)
    dept_name = models.CharField(max_length=20)
    dept_description = models.TextField()
    dept_record = models.DateTimeField(auto_now_add=True)
    dept_status = models.BooleanField(default=True)
    #True == Active status #False == Inactive/Shut down status
    dept_alias = models.SlugField(max_length=20, unique=True, default="dept")
    dept_record_last_modification = models.DateTimeField(auto_now=True)
    company_id = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    dept_logo = models.ImageField(max_length=1000, upload_to="static/master_dataset/", null=True, blank=True)

    class Meta:
        db_table = "company_dept"
        managed = True

#company's dept incharge at 1 particular site
class CompanyDeptIncharge(models.Model):
    dept_incharge_id = models.AutoField(primary_key=True, unique=True)
    emp_id = models.ForeignKey("employee_profile.EmployeeRecord", on_delete=models.CASCADE)
    dept_s_num = models.ForeignKey(CompanyDepts, on_delete=models.CASCADE)
    dept_incharge_from = models.DateField()
    dept_incharge_to = models.DateField(null=True, blank=True)
    dept_incharge_record = models.DateTimeField(auto_now_add=True)
    dept_incharge_record_last_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "company_dept_incharge"
        managed = True
