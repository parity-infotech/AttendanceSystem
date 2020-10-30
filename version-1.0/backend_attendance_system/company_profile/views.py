from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
import os  
import shutil          
from datetime import datetime
from django.db.models import F
#models import
from .models import (CompanyDetails, CompanySites, CompanySiteIncharge, CompanyDepts, CompanyDeptIncharge )
#serializers import
from .serializers import (
    #Company details
    CompanyDetails_Serializer, CompanyDetails_EditSerializer, 
    #Company Sites
    CompanySites_Serializer, CompanySites_EditSerializer, CompanySiteIncharge_Serializer, 
    CompanySiteIncharge_EditSerializer, 
    #Company Depts
    CompanyDepts_Serializer, CompanyDepts_EditSerializer, CompanyDeptsIncharge_Serializer, 
    CompanyDeptsIncharge_EditSerializer
    )

from django.shortcuts import get_object_or_404

home = os.getcwd()
print(home)

######################################################################################################################
######################################################################################################################
######################################## COMPANY DETAILS ############################################################
######################################################################################################################
######################################################################################################################

class CompanyDetails_View(APIView):
    ser_class = CompanyDetails_Serializer

    #to fill the details of the company in the db    
    def post(self, request):
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            print(ser.data)
            company_folder = "static//master_dataset//" + str(ser.data["company_id"])+ "__" + str(ser.data["company_name"])
            print(company_folder)
            try:
                os.makedirs(company_folder)
            except OSError:
                print("Company Folder already exists.")           
            logos_folder = company_folder + "//logos//Company_logo"
            print(logos_folder)
            depts_logo_folder = company_folder + "//logos//Depts_logo"
            print(depts_logo_folder)
            logos_path = str(ser.data["company_logo"])
            try:
                os.makedirs(logos_folder)
                print("Company Folder has created Logos Folder.")
                shutil.move(logos_path, logos_folder)
                print("Company Logo File moved.")
                obj.company_logo = logos_folder + "//" + str(logos_path).split("/")[2]
                obj.save()
            except OSError:
                print("Logos Folder already exists.")
            try:
                os.makedirs(depts_logo_folder)
                print("Company Folder has created Logos Folder.")
            except OSError:
                print("Depts Logo Folder already exists.")
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    #to retrieve details of all the companies in the contract from the db
    def get(self, request):
        data = CompanyDetails.objects.all()
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanyDetailsStatus_View(APIView):
    ser_class = CompanyDetails_Serializer

    #to get the details of the companies actively/inactively using/used the bot
    def get(self, request):
        data = CompanyDetails.objects.filter(company_status=True).values(
            "company_id",
            "company_name",
            "company_ceo",
            "company_founding_date",
            "company_CIN_num",
            "company_billing_address",
            "company_telephone",
            "company_email",
            "company_logo",
            "company_record",
            "company_record_last_modification",
            "company_alias"
        ).order_by("company_record")
        return Response(data, status=status.HTTP_200_OK)

class CompanyDetailsSingle_View(APIView):
    ser_class = CompanyDetails_Serializer

    #to get the details of a single company
    def get(self, request, company_alias):
        data = CompanyDetails.objects.filter(company_alias=company_alias).values(
            "company_id",
            "company_name",
            "company_ceo",
            "company_founding_date",
            "company_CIN_num",
            "company_billing_address",
            "company_telephone",
            "company_email",
            "company_logo",
            "company_record",
            "company_record_last_modification",
            "company_alias",
            "company_status",
        )
        return Response(data, status=status.HTTP_200_OK)

class CompanyFrontPage_View(APIView):
    ser_class = CompanyDetails_Serializer

    #to retrieve the company logo and name for the front page cover
    def get(self, request, company_alias):
        data = CompanyDetails.objects.filter(company_alias=company_alias).values(
            "company_id",
            "company_name",
            "company_logo",
        )
        return Response(data, status=status.HTTP_200_OK)

class CompanyDetailsSingleEdit_View(APIView):    
    ser_class = CompanyDetails_EditSerializer

    #to update the details of a single company in the db
    def post(self, request, company_alias):
        x = CompanyDetails.objects.filter(company_alias=company_alias).first()
        print(x)
        ser = self.ser_class(x, data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            print(obj)
            data_folder = "static//master_dataset//"
            try: 
                for company_folders in os.listdir(data_folder):
                    print(company_folders)
                    if str(company_folders).split("__")[0] == str(obj.company_id):
                        old_company_name = "static//master_dataset//" + company_folders
                        print(old_company_name)
                        new_company_name = "static//master_dataset//" + str(obj.company_id) + "__" + str(obj.company_name)
                        print(new_company_name)
                        os.rename(old_company_name, new_company_name)
            except PermissionError:
                print("Access is denied.")
            logos_folder = "static//master_dataset//" + str(obj.company_id) + "__" + str(obj.company_name) + "//logos//Company_logo"
            print(logos_folder)
            shutil.move(str(obj.company_logo), logos_folder)
            obj.company_logo = logos_folder + "//" + str(obj.company_logo).split("/")[2]
            print(obj.company_logo)
            obj.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class CompanyDetailsSingleDelete_View(APIView):
    ser_class = CompanyDetails_EditSerializer

    #to soft-delete the records of a single company by putting company_status to false
    def post(self, request, company_alias):
        x = []
        CompanyDetails.objects.filter(company_alias=company_alias).update(company_status=False, company_record_last_modification=datetime.now())
        company_id = int(CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
        CompanySites.objects.filter(company_id=company_id).update(site_status=False, site_record_last_modification=datetime.now())    
        CompanyDepts.objects.filter(company_id=company_id).update(dept_status=False, dept_record_last_modification=datetime.now())
        dept_s_num = CompanyDepts.objects.filter(company_id=company_id).values_list("dept_s_num")
        print("dept_s_num", dept_s_num)
        for j in dept_s_num:
            print(j)
            k = int(str(j).split("(")[1].split(",")[0])
            print(k)
            x.append(k)
        company_name_folder = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id", "company_name")
        print(company_name_folder)
        search_folder = "static//master_dataset//"
        global company_folder_2
        try:
            for company_folders in os.listdir(search_folder):
                print(company_folders)
                if str(company_folders) == str(company_name_folder[0][0]) + "__" + company_name_folder[0][1]:
                    company_folder_2 = search_folder + company_folders
                    print("company_folder", company_folder_2)
                    #shutil.rmtree(company_folder_2)
        except OSError:
            print("Company Folder does not exist")
        return Response("Record deleted", status=status.HTTP_200_OK)

######################################################################################################################
######################################################################################################################
#########################################COMPANY SITES################################################################
######################################################################################################################
######################################################################################################################

class CompanySitesCompany_View(APIView):
    ser_class = CompanySites_Serializer

    #to fill all the details of the site/geographical location of the company
    def post(self, request, company_alias):
        company_details = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id", "company_name")[0]
        print(company_details)
        ser = self.ser_class(data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            search_folder = "static//master_dataset//"
            try: 
                CompanySites.objects.filter(site_s_num=int(obj.site_s_num)).update(company_id=CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
            except AttributeError:
                print("Attribute error.")
            for company_folders in os.listdir(search_folder):
                print(company_folders)
                if company_folders == str(str(company_details[0]) + "__" + company_details[1]):
                    print(company_folders)
                    site_folder = "static//master_dataset//" + company_folders + "//" + str(obj.site_id) + "__" + str(obj.site_name)
                    try:
                        os.makedirs(site_folder)
                    except OSError:
                        print("Site Folder already exists.")
                    employees_folder = os.path.join(site_folder, "employees")
                    try:
                        os.makedirs(employees_folder)
                        print("Site Folder has cretaed Employees Folder.")
                    except OSError:
                        print("Employees Folder already exists.")
                    visitors_path = os.path.join(site_folder, "visitors")
                    try:
                        os.makedirs(visitors_path)
                        print("Site Folder has created Visitors Folder.")
                    except OSError:
                        print("Visitors Folder already exists.")
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    #to view the sites as per the company filter
    def get(self, request, company_alias):
        x = int(CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
        data = CompanySites.objects.filter(company_id=x).values(
            "site_s_num",
            "site_id",
            "site_GST_num",
            "site_name",
            "site_address",
            "site_telephone",
            "site_record",
            "site_status",
            "site_alias",
            "site_record_last_modification",
            # company_name = F("company_id__company_name")
        ).order_by("site_record")
        return Response(data, status=status.HTTP_200_OK)

#to view the details of a single site in the company's db 
class CompanySitesSingle_View(APIView):
    ser_class = CompanySites_Serializer

    def get(self, request, company_alias, site_alias):
        x = int(CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
        data = CompanySites.objects.filter(company_id=x, site_alias=site_alias).values(
            "site_s_num",
            "site_id",
            "site_GST_num",
            "site_name",
            "site_address",
            "site_telephone",
            "site_record",
            "site_status",
            "site_record_last_modification",
            "site_alias",
            # company_name = F("company_id__company_name"),
        )
        return Response(data, status=status.HTTP_200_OK)

class CompanySitesSingleEdit_View(APIView):    
    ser_class = CompanySites_EditSerializer

    #to update the details of a single company-site in the db
    def post(self, request, company_alias, site_alias):
        company_details = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id", "company_name")[0]
        site_details = CompanySites.objects.filter(site_alias=site_alias).values_list("site_id", "site_name")[0]
        x = CompanySites.objects.filter(company_id=int(company_details[0]), site_alias=site_alias).first()
        ser = self.ser_class(x, data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            search_folder = "static//master_dataset//"
            for company_folders in os.listdir(search_folder):
                if company_folders == str(company_details[0]) + "__" + company_details[1]:
                    print(company_folders)
                    for site_folders in os.listdir(str(search_folder + "//" +company_folders)):
                        print(site_folders)
                        print(site_details[0], site_details[1])
                        print(site_details)
                        if site_folders == site_details[0] + "__" + site_details[1]:
                            old_site_name = "static//master_dataset//" + company_folders + "//" + site_folders
                            print(old_site_name)
                            new_site_name = "static//master_dataset//" + company_folders + "//" + obj.site_id + "__" + obj.site_name
                            print(new_site_name)
                            os.rename(old_site_name, new_site_name)
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class CompanySitesCompanyStatus_View(APIView):
    ser_class = CompanySites_Serializer
    
    #to retrieve details of active sites of a company
    def get(self, request, company_alias):
        data = CompanySites.objects.filter(site_status=True).all().order_by("site_record")
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanySitesSingleDelete_View(APIView):
    ser_class = CompanySites_Serializer

    #to delete the records of a single site of the company
    def post(self, request, company_alias, site_alias):
        x = []
        CompanySites.objects.filter(site_alias=site_alias).update(site_status=False, site_record_last_modification=datetime.now())
        company_details = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id", "company_name")[0]
        site_details = CompanySites.objects.filter(site_alias=site_alias).values_list("site_id", "site_name", "site_s_num")[0]
        CompanyDepts.objects.filter(site_s_num=site_details[2]).update(dept_status=False, dept_record_last_modification=datetime.now())
        try:
            z = CompanyDepts.objects.filter(site_s_num=site_details[2]).values_list("dept_s_num")[0][0]
            x.append(z)
        except IndexError:
            print("Index Error occurred")
        search_folder = "static//master_dataset//"
        for company_folders in os.listdir(search_folder):
            if company_folders == str(company_details[0]) + "__" + company_details[1]:
                print(company_folders)
                for site_folders in os.listdir(search_folder + "//" + company_folders):
                        print(site_folders)
                        if site_folders == site_details[0] + "__" + site_details[1]:
                            #shutil.rmtree(search_folder + "//" + company_folders + "//" + site_folders)
                            print("Site_folder Not deleted")
        return Response("Record deleted", status=status.HTTP_200_OK)

class CompanySites_View(APIView):
    ser_class = CompanySites_Serializer
    
    #to view companies-sites which are/were using this system at any time on the developer's end
    def get(self, request):
        data = CompanySites.objects.all()
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanySiteIncharge_View(APIView):
    ser_class = CompanySiteIncharge_Serializer

    #to fill the details of incharges of sites in the company
    def post(self, request, company_alias, site_alias):
        x = int(CompanySites.objects.filter(site_alias=site_alias).values_list("site_s_num")[0][0])
        print(x)
        ser = self.ser_class(CompanySiteIncharge.objects.filter(site_s_num=x), data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    #to retrieve the details of the site-incharges of the company
    def get(self, request, company_alias, site_alias):
        x = CompanySites.objects.filter(site_alias=site_alias).values_list("site_s_num")[0][0]
        print(x)
        data = CompanySiteIncharge.objects.filter(site_s_num=x).values(
            "site_incharge_id",
            "site_incharge_from",
            "site_incharge_to",
            "site_incharge_record",
            "site_incharge_record_last_modification",
            employee_name = F("emp_id__employee_name"),
            # site_name = F("site_s_num__site_name"),
            # company_name = F("site_s_num__company_id__company_name"),
        )
        return Response(data, status=status.HTTP_200_OK)

class CompanySiteInchargeSite_View(APIView):
    ser_class = CompanySiteIncharge_Serializer

    # to view the site-incharges of a particular site of the company
    def get(self, request, site_s_num):
        data = CompanySiteIncharge.objects.filter(site_s_num=site_s_num).all()
        ser = self. ser_class(data=request.data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanySiteInchargeEdit_View(APIView):
    ser_class = CompanySiteIncharge_EditSerializer

    #to fill in the last details of a site incharge by editing the write-only-fields
    def post(self, request, site_incharge_id):
        x = CompanySiteIncharge.objects.filter(site_incharge_id=site_incharge_id).first()
        ser = self.ser_class(x, data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


######################################################################################################################
######################################################################################################################
#########################################COMPANY DEPARTMENTS##########################################################
######################################################################################################################
######################################################################################################################

class CompanyDeptsCompany_View(APIView):
    ser_class = CompanyDepts_Serializer

    #to fill all the details of the dept of the company-site
    def post(self, request, company_alias):
        x = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id", "company_name")[0]
        print(x)
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = ser.save()
            img_file = str(obj.dept_logo)
            company_folder = str(x[0]) + "__" + x[1]
            search_folder = "static//master_dataset//" 
            for company_folders in os.listdir(search_folder):
                print(company_folders)
                if company_folders == company_folder:
                    try:
                        destination_folder = "static//master_dataset//" + company_folders + "//logos//Depts_logo//" + str(obj.dept_name)
                        os.makedirs(destination_folder)   
                        shutil.move(img_file, destination_folder)
                        obj.dept_logo = destination_folder
                        obj.save()
                    except OSError:
                        print("OSError")
            try:
                CompanyDepts.objects.filter(dept_s_num=obj.dept_s_num).update(company_id=CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
            except AttributeError:
                print("Attribute Error occurred.")
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    #to retrieve details of active dept at various sites
    def get(self, request, company_alias):
        data = CompanyDepts.objects.filter(dept_status=True).values(
            "dept_id",
            "dept_name",
            "dept_description",
            "dept_alias",
            "dept_record",
            "dept_record_last_modification",
            "dept_logo",
            site_name = F("site_s_num__site_name"),
            company_name = F("company_id__company_name"),
        ).order_by("dept_record")
        return Response(data, status=status.HTTP_200_OK)

class CompanyDeptsSite_View(APIView):
    ser_class = CompanyDepts_Serializer

    #to view the details of a dept at a single site of the company
    def get(self, request, site_s_num):
        data = CompanyDepts.objects.filter(site_s_num=site_s_num).all()
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanyDeptsSingle_View(APIView):
    
    #to view the details of a single dept at a particular site in the db 
    def get(self, request, company_alias, dept_alias):
        x = CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0]
        data = CompanyDepts.objects.filter(dept_alias=dept_alias, company_id=x[0], dept_status=True).values(
            "dept_id",
            "dept_name",
            "dept_description",
            "dept_record",
            "dept_record_last_modification",
            "dept_logo",
        )
        return Response(data, status=status.HTTP_200_OK)

class CompanyDeptsSingleEdit_View(APIView):    
    ser_class = CompanyDepts_EditSerializer

    #to update the details of a single dept at a company-site in the db
    def post(self, request, company_alias, dept_alias):
        x = CompanyDepts.objects.filter(dept_alias=dept_alias).first()
        ser = self.ser_class(x, data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class CompanyDeptsSingleDelete_View(APIView):
    ser_class = CompanyDepts_Serializer

    #to delete the records of a single site of the company
    def post(self, request, company_alias, dept_alias):
        CompanyDepts.objects.filter(dept_alias=dept_alias).update(dept_status=False, dept_record_last_modification=datetime.now())
        x = CompanyDepts.objects.filter(dept_alias=dept_alias).values_list("dept_s_num")[0][0]
        return Response("Record deleted", status=status.HTTP_200_OK)

class CompanyDepts_View(APIView):
    ser_class = CompanyDepts_Serializer

    #to view companies-sites depts which are/were using this system
    def get(self, request):
        data = CompanyDepts.objects.all()
        ser = self.ser_class(data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanyDeptsIncharge_View(APIView):
    ser_class = CompanyDeptsIncharge_Serializer

    #to fill the details of incharges of sites-dept in the company
    def post(self, request, company_alias, dept_alias):
        ser = self.ser_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    #to retrieve the details of the dept-incharges of the company
    def get(self, request, company_alias, dept_alias):
        data = CompanyDeptIncharge.objects.all()
        ser = self.ser_class(data=request.data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanyDeptsInchargeDept_View(APIView):
    ser_class = CompanyDeptsIncharge_Serializer

    # to view the dept-incharges of a particular site of the company
    def get(self, request, company_alias, dept_alias):
        x = int(CompanyDetails.objects.filter(company_alias=company_alias).values_list("company_id")[0][0])
        data = CompanyDeptIncharge.objects.filter(company_id=x, dept_alias=dept_alias).all()
        ser = self. ser_class(data=request.data, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class CompanyDeptsInchargeEdit_View(APIView):
    ser_class = CompanyDeptsIncharge_EditSerializer

    #to fill in the last details of a dept incharge by editing the write-only-fields
    def post(self, request, company_alias, dept_alias, dept_incharge_id):
        x = CompanyDeptIncharge.objects.filter(dept_incharge_id=dept_incharge_id).first()
        ser = self.ser_class(x, data=request.data, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

