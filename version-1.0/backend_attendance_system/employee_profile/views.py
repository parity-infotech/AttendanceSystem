from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
from company_profile.models import (CompanyDetails, CompanySites, CompanyDepts)
from .models import ( EmployeeRecord, EmployeeAttendanceVerification, MoralLines, EmployeeVoice )

from .serializers import (
    EmployeeRecord_Serializer, EmployeeRecord_EditSerializer, #Employee record
  
    # Employee attendance
    EmployeeAttendanceRecord_Serializer, EmployeeAttendanceVerification_Serializer,

    #Moral line
    MoralLines_Serializer, EmployeeVoiceSave_Serializer
)

from auxillary_codes.web_cam_photo_capture_save import web_cam_capture_image
from auxillary_codes.face_recognition_image_captured_by_webcam.recognize_faces_image import image_recognition
from auxillary_codes.moral_line import check_and_record_moral_line

import os
import shutil
import random
from datetime import datetime
from playsound import playsound
from pydub import AudioSegment
from django.core.exceptions import ObjectDoesNotExist
import base64
import six
import json
from PIL import Image
from io import BytesIO
import re, time
from django.db.models import F

home = os.getcwd()
print(home)

######################################################################################################################
######################################################################################################################
################################################# EMPLOYEE RECORD #################################################### 
######################################################################################################################
######################################################################################################################

class EmployeeRecord_View(APIView):
    ser_class = EmployeeRecord_Serializer

    #to write and save to db the information about an employee
    def post(self, request, company_alias, site_alias):
        company_details = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id", "company_name")[0]
        print(company_details)
        site_details = CompanySites.objects.filter(site_alias=site_alias).values_list("site_id", "site_name", "site_s_num")
        print(site_details)
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            employee_folder = str(ser.data["emp_id"]) + "__" + str(ser.data["emp_name"])
            print(employee_folder)
            search_folder = "static//master_dataset//"
            for company_folders in os.listdir(search_folder):
                print(company_folders)
                if company_folders == str(company_details[0]) + "__" + company_details[1]:
                    for site_folders in os.listdir(search_folder + company_folders):
                        print(site_folders)
                        if site_folders == str(site_details[0][0]) + "__" + site_details[0][1]:
                            employee_path = search_folder + company_folders + "//" + site_folders + "//employees//" + str(employee_folder)
                            print(employee_path)
                            try: 
                                os.makedirs(employee_path)
                                print("Employees Folder created an employee folder with emp_id and emp_name.")
                            except OSError:
                                print("Employee Folder already exists.")
                            training_dataset = os.path.join(employee_path, "training_dataset")
                            try: 
                                os.makedirs(training_dataset)
                                print("Employee Folder created an employee folder with training dataset folder.")
                            except OSError:
                                print("Training Dataset Folder already exists.")
                            audio_dataset = os.path.join(employee_path, "audio_dataset")
                            try:
                                os.makedirs(audio_dataset)
                                print("Employees Folder created an employee folder with audio_dataset folder.")
                            except:
                                print("Audio_dataset Folder already exists.")        
                            documents = os.path.join(employee_path, "documents")
                            os.makedirs(documents)
                            print("Employees Folder created an employee folder with documents folder.")
                            aadhar_file = str(obj.emp_AADHAR_num)
                            shutil.move(aadhar_file, documents)
                            obj.emp_AADHAR_num = documents
                            obj.save()
                            pan_file = str(obj.emp_PAN_card)
                            shutil.move(pan_file, documents)
                            obj.emp_PAN_card = documents
                            obj.save()
                            bank_file = str(obj.emp_bank_account_num)
                            shutil.move(bank_file, documents)
                            obj.emp_bank_account_num = documents
                            obj.save()
                            try:
                                EmployeeRecord.objects.filter(emp_s_num=obj.emp_s_num).update(site_s_num=site_details[0][2])
                            except AttributeError:
                                print("Site not allocated")
                            try:
                                EmployeeRecord.objects.filter(emp_s_num=obj.emp_s_num).update(company_id=CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
                            except AttributeError:
                                print("Attribute error occurred")
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class EmployeeRecordCompany_View(APIView):
    ser_class = EmployeeRecord_Serializer

    #to see the employees of a company working at a particular site name
    def get(self, request, company_alias):
        x = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0]
        print(x)
        data = EmployeeRecord.objects.filter(company_id=int(x)).values(
            "emp_id",
            "emp_name",
            "emp_gender",
            "emp_dob",
            "emp_mark_of_identification",
            "emp_AADHAR_num",
            "emp_PAN_card",
            "emp_bank_account_num",
            "emp_family_details",
            "emp_address",
            "emp_personal_email",
            "emp_personal_phone",
            "emp_doj",
            "emp_company_email",
            "emp_education_qualifications",
            "dept_s_num",
            "company_id",
            "site_s_num",
            "emp_designation",
            "emp_leaves_max",
            "emp_band",
            "emp_record",
            "emp_status",
            "emp_resigning_date",
            "emp_alias",
            "emp_record_last_modification_date",
        ).order_by("emp_doj")
        return Response(data, status=status.HTTP_200_OK)

class EmployeeRecordDepts_View(APIView):
    ser_class = EmployeeRecord_Serializer

    #to see all the employees working in a particular dept
    def get(self, request, company_alias, dept_alias):
        company_id = int(CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
        print(company_id)
        dept_s_num = int(CompanyDepts.objects.filter(dept_alias=dept_alias).values_list("dept_s_num")[0][0])
        print(dept_s_num)
        data = EmployeeRecord.objects.filter(company_id=company_id, dept_s_num=dept_s_num).values(
            "emp_id",
            "emp_name",
            "emp_gender",
            "emp_dob",
            "emp_mark_of_identification",
            "emp_AADHAR_num",
            "emp_PAN_card",
            "emp_bank_account_num",
            "emp_family_details",
            "emp_address",
            "emp_personal_email",
            "emp_personal_phone",
            "emp_doj",
            "emp_company_email",
            "emp_education_qualifications",
            "dept_s_num",
            "company_id",
            "site_s_num",
            "emp_designation",
            "emp_leaves_max",
            "emp_band",
            "emp_record",
            "emp_status",
            "emp_resigning_date",
            "emp_alias",
            "emp_record_last_modification_date",
        ).order_by("emp_doj")
        return Response(data, status=status.HTTP_200_OK)

class EmployeeRecordBand_View(APIView):
    ser_class = EmployeeRecord_Serializer

    #to view the employees of different bands/categorizations set by the company
    def get(self, request, company_alias, emp_band):
        company_id = int(CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
        data = EmployeeRecord.objects.filter(company_id=company_id, emp_band=emp_band, emp_status=True).values(
            "emp_id",
            "emp_name",
            "emp_gender",
            "emp_dob",
            "emp_mark_of_identification",
            "emp_AADHAR_num",
            "emp_PAN_card",
            "emp_bank_account_num",
            "emp_family_details",
            "emp_address",
            "emp_personal_email",
            "emp_personal_phone",
            "emp_doj",
            "emp_company_email",
            "emp_education_qualifications",
            "dept_s_num",
            "company_id",
            "site_s_num",
            "emp_designation",
            "emp_leaves_max",
            "emp_band",
            "emp_record",
            "emp_status",
            "emp_resigning_date",
            "emp_alias",
            "emp_record_last_modification_date",
        ).order_by("emp_doj")
        return Response(data, status=status.HTTP_200_OK)

######################################################################################################################
######################################################################################################################
########################################### EMPLOYEE IN TIME ######################################################### 
######################################################################################################################
######################################################################################################################







class FacialRecognition_View(APIView):
    ser_class = EmployeeAttendanceRecord_Serializer

    #to write and save to db information on the employee image whether it is for training or attendance
    def post(self, request, company_alias, site_alias):
        x = request.body
        #print("data", data)
        data = str(x).split(';base64,')[1]
        #print("data", data)
        f = open(str(str(datetime.now().today()).replace(" ", "__").replace(":", "__").split(".")[0] + ".jpeg"),"wb")
        byte_data = base64.b64decode(data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        img.save(f, "JPEG")
        print("f", f)
        image_name = f.name
        print("image_name--->", image_name)
        image_name_predicted = image_recognition(image_name, "employees")
        print("image_name_predicted", image_name_predicted)
        return Response(image_name_predicted, status=status.HTTP_200_OK)
        
class EmployeeAttendanceInTime_View(APIView):
    ser_class = EmployeeAttendanceRecord_Serializer

    #to save the record of entry time in db
    def post(self, request, company_alias, site_alias):
        name_sent = request.data
        print("body", name_sent)
        name_id_correct_2 = name_sent["name"]
        print(name_id_correct_2)
        print("name_correct", type(name_id_correct_2), name_id_correct_2)
        name_id_correct = name_id_correct_2
        print("name_id", name_id_correct)
        predicted_emp_name = name_id_correct.split("__")[1]
        print(predicted_emp_name)
        predicted_emp_id = name_id_correct.split("__")[0]
        print(predicted_emp_id)
        predicted_emp_s_num = EmployeeRecord.objects.filter(emp_id=predicted_emp_id).values_list("emp_s_num")[0][0] #.split("(")[1].split(",")[0]
        print(predicted_emp_s_num, type(predicted_emp_s_num))
        entry_type = name_sent["entry_type"]
        print("entry_type", entry_type)
        ser = self.ser_class(data=name_sent)
        print("data", ser.initial_data)
        if ser.is_valid():
            obj = ser.save()
            obj.emp_entry_type = entry_type
            obj.save()
            try:
                EmployeeAttendanceVerification.objects.filter(attendance_id=int(obj.attendance_id)).update(emp_s_num=EmployeeRecord.objects.filter(emp_id=predicted_emp_id).values_list("emp_s_num")[0][0])
            except AssertionError:
                print("Assertion Error occurred")
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EmployeeAttendanceExitRecord_View(APIView):
    ser_class = EmployeeAttendanceRecord_Serializer

    #to record exit time of the employee
    def post(self, request, company_alias, site_alias):
        body_unicode = request.body.decode('utf-8')
        print(body_unicode)
        body = json.loads(body_unicode)
        print(body, type(body))
        entry_s_num = body['entry_s_num']
        print(entry_s_num)
        exit_time = body['exitTime']
        print(exit_time)
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            EmployeeAttendanceVerification.objects.filter(attendance_id=obj.attendance_id).update(entry_s_num=entry_s_num)
            try:
                EmployeeInTime.objects.filter(entry_s_num=entry_s_num).update(emp_exit_bool=True).save()
            except AttributeError:
                print("AttributeError")
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request, company_alias, site_alias):
        data = EmployeeAttendanceVerification.objects.filter(entry_s_num=entry_s_num).all()
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class EmployeeAttendanceVerification_View(APIView):
    ser_class = EmployeeAttendanceVerification_Serializer

    #to verify the attendance_record by the boss
    def post(self, request, company_alias, site_alias, attendance_id):
        print(attendance_id)
        ser = self.ser_class(EmployeeAttendanceVerification.objects.get(attendance_id=attendance_id), data=request.data, partial=True)
        print(ser.initial_data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            print(obj.attendance_id)
            obj.emp_attendance_verified_status = True
            obj.save()
            obj.emp_attendance_verified_by_emp_id = "PI0004" #to be changed to request.emp_id
            obj.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

######################################################################################################################
######################################################################################################################
############################################# MORAL LINE #############################################################
######################################################################################################################
######################################################################################################################

class MoralLines_View(APIView):
    ser_class = MoralLines_Serializer

    #to save in db, the moral lines by company head
    def post(self, request, company_alias, site_alias):
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    #to retrieve the moral_lines used till now from the db
    def get(self, request, company_alias, site_alias):
        data = MoralLines.objects.all()
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class EmployeeVoice_View(APIView):
    ser_class = MoralLines_Serializer

    #to display the moral line to the employee
    def get(self, request, company_alias, site_alias):
        moral_line_record = dict()
        moral_lines = int(str(MoralLines.objects.latest("moral_line_id")).split("(")[1].split(")")[0])
        moral_line_id_predictor = random.randint(1, moral_lines)
        print(int(moral_line_id_predictor))
        moral_line_identification = MoralLines.objects.filter(moral_line_id=int(moral_line_id_predictor)).values_list("moral_line_text")
        moral_line_text = moral_line_identification[0][0]
        moral_line_record["moral_line_id"] = moral_line_id_predictor
        moral_line_record["moral_line_text"] = moral_line_text
        return Response(moral_line_record)

class EmployeeVoiceSave_View(APIView):
    ser_class = EmployeeVoiceSave_Serializer

    #to set up the record mode for moral line
    def post(self, request, company_alias, site_alias, moral_line_id):
        moral_line_identification = MoralLines.objects.filter(moral_line_id=int(moral_line_id)).values_list("moral_line_text")
        print(moral_line_identification[0][0])
        emp_id_told_identified = check_and_record_moral_line(moral_line_identification[0][0])
        emp_id_told = str(emp_id_told_identified).split("__")[0]
        print(emp_id_told, type(emp_id_told))
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            obj.moral_line_id = moral_line_id
            obj.emp_id = emp_id_told.split(".")[0]
            obj.save()
            emp_name_identified = EmployeeRecord.objects.filter(emp_id=emp_id_told.split(".")[0]).values_list("emp_name", "company_id", "emp_s_num")[0]
            obj.emp_s_num = int(emp_name_identified[2])
            obj.save()
            emp_name = emp_name_identified[0][0]
            print(emp_name)
            emp_folder = emp_id_told + "__" + emp_name
            print(emp_folder)
            company_id = emp_name_identified[0][1]
            print(company_id)
            company_name = CompanyDetails.objects.filter(company_id=company_id).values_list("company_name")
            company_name = str(company_id) + "__" + company_name[0][0]
            print(company_name)
            site_details = CompanySites.objects.filter(site_alias=site_alias).values_list("site_id", "site_name")[0]
            print(site_details)
            site_name = str(site_details[0]) + "__" +  site_details[1]
            print(site_name)
            audio_location = str(emp_id_told_identified)
            print(audio_location)
            audio_destination = "static//master_dataset//" + company_name + "//" + site_name + "//employees//" + emp_folder + "//audio_dataset//" + str(datetime.today().date()) 
            print(audio_destination)
            audio_location_compressed = audio_location.split(".")[0] + ".mp3"
            try:
                os.makedirs(audio_destination)
            except OSError:
                print("Folder already exists.")
            AudioSegment.from_wav(audio_location).export(audio_location_compressed, format="mp3") 
            shutil.move(audio_location_compressed, audio_destination)
            print("Audio file has been moved to the respective employee folder.")
            obj.emp_voice = audio_destination
            obj.save()
            os.remove(audio_location)
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
