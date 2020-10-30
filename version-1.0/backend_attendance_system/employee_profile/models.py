from django.db import models

# Create your models here.
import company_profile.models 

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.utils import timezone

Bands = (
    ("B1" , "Band-1"),
    ("B2" , "Band-2"),
    ("B3" , "Band-3"),
)

Entry_Type = (
    ("I", "In"),
    ("O", "Out"),
)

#employee record as maintained by the company
class EmployeeRecord(models.Model):
    emp_s_num = models.AutoField(primary_key=True, unique=True)
    emp_id = models.CharField(max_length=10)
    emp_name = models.CharField(max_length=100)
    emp_gender = models.CharField(max_length=1)
    #write M for Male and F for Female and N for Neutral
    emp_dob = models.DateField(null=True, blank=True)
    emp_mark_of_identification = models.TextField(default=0)
    emp_AADHAR_num = models.FileField(max_length=1000, upload_to="static/master_dataset/")
    emp_PAN_card = models.FileField(max_length=1000, upload_to="static/master_dataset/")
    emp_bank_account_num = models.FileField(max_length=1000, upload_to="static/master_dataset/")
    emp_family_details = JSONField()
    """
    "emp_family_details": {
        "Father": {
            "Name": "ABC",
            "Aadhar": "1234567890"
            },
        "Mother": {
            "Name": "DEF",
            "Aadhar":"9876543210"
            },
        "Spouse" : {
            "Name" : "XYZ",
            "Aadhar" : "9517326480"
            },
        "Any other relation": {
            "Name" : "RST",
            "Relationship" : "Brother",
            "Aadhar": "753912684"
            },
        "Nominee" : {
            "Name" : "RST",
            "Relationship" : "Brother",
            "Aadhar": "753912684"
            },
        }
    """
    emp_address = models.TextField(default={})
    emp_personal_email = models.EmailField(default="ishirajk1994@gmail.com")
    emp_personal_phone = models.CharField(max_length=15, default=0)
    emp_doj = models.DateField()
    emp_company_email = models.EmailField(default="ishita.katyal@paritysystems.in")
    emp_education_qualifications = JSONField()
    """
    "emp_education_qualifications": {
        "Schooling_X" : {
            "Name": "Rukmini Devi Public School",
            "Location": "CD-BLock PitamPura",
            "Board" : "CBSE",
            "Percentage/GPA": "10.0",
            },
        "Schooling_XII" : {
            "Name": "Rukmini Devi Public School",
            "Location": "CD-BLock PitamPura",
            "Board" : "CBSE",
            "Percentage/GPA": "90.8",
            },
        "Graduation" : {
            "College Name": "IISER-Mohali",
            "Location": "Mohali, Punjab",
            "Board" : "IISER-M",
            "Percentage/GPA": "7.2",
            },
        "Post-graduation" : {
            "College Name": "IISER-Mohali",
            "Location": "Mohali, Punjab",
            "Board" : "IISER-M",
            "Percentage/GPA": "7.1",
            },
#Put a diploma option to add on a different button and also to add multiple diplomas 
        "Diplomas": {
            "Diploma_1" : {
                "Name": "ABC",
                "Location": "Delhi",
                "Board" : "ABC",
                "Grade": "Pass", #or something else by which u r graded
                },
            "Diploma_2" : {
                "Name": "ABC",
                "Location": "Delhi",
                "Board" : "ABC",
                "Grade": "Pass", #or something else by which u r graded
                },
            },
#Put a certification option to add on a different button and also to add multiple certification
        "Certifications" : {
            "Certificate_1":{
                "Name": "C++ Data Structures and Algorithms",
                "Location": "Delhi",
                "Board": "Coding Ninjas",
                "Grade": "Pass", 
            },
            "Certificate_2":{
                "Name": "C++ Data Structures and Algorithms",
                "Location": "Delhi",
                "Board": "Coding Ninjas",
                "Grade": "Pass", 
            },
        },
    }

    """
    dept_s_num = models.ForeignKey("company_profile.CompanyDepts", on_delete=models.CASCADE, null=True, blank=True)
    #Since this can be null and blank, there is a mention of company_id separately
    company_id = models.ForeignKey("company_profile.CompanyDetails", on_delete=models.CASCADE, null=True, blank=True)
    site_s_num = models.ForeignKey("company_profile.CompanySites", on_delete=models.CASCADE, null=True, blank=True)
    emp_designation = JSONField()
    """
    "designation": [
        "designation_1": {
            "post_name" : "Software Developer",
            "from_date" : "15.06.2019",
            "to_date" : "15.06.2020"
        },
        "designation_2": {
            "post_name" : " Senior Software Developer",
            "from_date" : "15.06.2020",
            "to_date" : "Present"
        },
        ..........
    ]
    """
    emp_leaves_max = models.IntegerField(default=0)
    emp_band = models.CharField(max_length=50, choices=Bands)
    #any specific type of categorization by a company
    emp_record = models.DateTimeField(auto_now_add=True)
    emp_status = models.BooleanField(default=True)
    #True == Active status
    #False == Inactive/Shut down status
    emp_resigning_date = models.DateField(null=True, blank=True)
    emp_alias = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    emp_record_last_modification_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "employee_record"
        managed = True

#employee entry and exit time and verification by the admin
class EmployeeAttendanceVerification(models.Model):
    attendance_id = models.AutoField(primary_key=True, unique=True)
    #this will be used to record the in_time of employee
    emp_entry_type = models.CharField(max_length=1, default="I")
    attendance_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    emp_attendance_verified_status = models.BooleanField(default=False, editable=True)
    emp_s_num = models.ForeignKey(EmployeeRecord, on_delete=models.CASCADE, null=True, blank=True)
    #verified by
    emp_attendance_verified_record_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee_attendance"
        managed = True

#moral lines in the db for further voice recognition
class MoralLines(models.Model):
    moral_line_id = models.AutoField(primary_key=True, unique=True)
    moral_line_text = models.TextField(max_length=500)

    class Meta:
        db_table = "moral_line"
        managed = True

#moral lines as spoken by the employee of the company
class EmployeeVoice(models.Model):
    voice_id = models.AutoField(primary_key=True, unique=True)
    emp_s_num = models.ForeignKey(EmployeeRecord, on_delete=models.CASCADE, null=True, blank=True)
    moral_line_id = models.CharField(max_length=5, default="0", null=True, blank=True)
    emp_voice = models.FileField(max_length=500, upload_to="static/master_dataset/", null=True, blank=True)
    emp_voice_record = models.DateTimeField(auto_now=True)
    emp_voice_alias = models.SlugField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "employee_voice"
        managed = True