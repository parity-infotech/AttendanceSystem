from rest_framework import serializers
from .models import (EmployeeRecord, EmployeeAttendanceVerification, MoralLines, EmployeeVoice)

class EmployeeRecord_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRecord
        fields = ('__all__')

class EmployeeRecord_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRecord
        fields = ('__all__')
        write_only_fields = ('emp_family_details', 'emp_address', 'emp_personal_mail', 'emp_personal_phone', 
        'emp_education_qualifications', 'dept_s_num', 'emp_designation','emp_band', 'emp_status')

class EmployeeAttendanceRecord_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendanceVerification
        fields = ('attendance_time', 'emp_entry_type')

class EmployeeAttendanceVerification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendanceVerification
        fields = ('attendance_id', 'attendance_out_time', 'emp_attendance_verified_status', 'emp_s_num')
        write_only_fields = ('emp_attendance_verified_status', 'emp_s_num', 'emp_attendance_verified_record_time')

class MoralLines_Serializer(serializers.ModelSerializer):
    class Meta:
        model = MoralLines
        fields = ('__all__') 

class EmployeeVoiceSave_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeVoice
        fields = ('__all__')