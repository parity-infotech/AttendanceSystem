from django.urls import path
from .views import (
    #Employeerecord
    EmployeeRecord_View, EmployeeRecordCompany_View, EmployeeRecordDepts_View, EmployeeRecordBand_View,
    
    #Employee attendance
    FacialRecognition_View, EmployeeAttendanceInTime_View, EmployeeAttendanceExitRecord_View, EmployeeAttendanceVerification_View,

    #Employee audio
    MoralLines_View, EmployeeVoice_View, EmployeeVoiceSave_View 
)
     
app = "employee_profile"

urlpatterns = {
    #Employee Record
    path("<slug:site_alias>/new_employee/", EmployeeRecord_View.as_view()), #Verified final time
    path("company_view/", EmployeeRecordCompany_View.as_view()), #Verified final time
    path("<slug:dept_alias>/dept_view/", EmployeeRecordDepts_View.as_view()), #Verified final time
    path("<slug:emp_band>/band_view/", EmployeeRecordBand_View.as_view()), #Verified final time

    #Employee Attendance
    path("<slug:site_alias>/attendance_in/", FacialRecognition_View.as_view()), #Verified
    path("<slug:site_alias>/mark_attendance/", EmployeeAttendanceInTime_View.as_view()),
    
    #Employee audio - not included so far
    # path("<slug:site_alias>/moral_lines/", MoralLines_View.as_view()), #Verified
    # path("<slug:site_alias>/moral_line/", EmployeeVoice_View.as_view()), #verified
    # path("<slug:site_alias>/moral_line_record/<slug:moral_line_id>/", EmployeeVoiceSave_View.as_view()), #Verified
    
}