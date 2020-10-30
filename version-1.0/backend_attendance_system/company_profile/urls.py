from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    #Company Details
    CompanyDetails_View, CompanyDetailsStatus_View, CompanyDetailsSingle_View, CompanyFrontPage_View,
    CompanyDetailsSingleEdit_View, CompanyDetailsSingleDelete_View,

    #Company Sites
    CompanySitesCompany_View, CompanySitesSingle_View, CompanySitesSingleEdit_View, CompanySitesCompanyStatus_View,
    CompanySitesSingleDelete_View, CompanySites_View, CompanySiteIncharge_View, CompanySiteInchargeSite_View,
    CompanySiteInchargeEdit_View,

    #Company Depts
    CompanyDeptsCompany_View, CompanyDepts_View, CompanyDeptsSingle_View, CompanyDeptsSingleEdit_View,
    CompanyDeptsSingleDelete_View, CompanyDeptsIncharge_View, CompanyDeptsInchargeDept_View, CompanyDeptsInchargeEdit_View 
)

app_name = "company_profile"

urlpatterns = [
    #company_details
    path("company_details/all/", CompanyDetails_View.as_view()),  #verified final time
    path("company_details/", CompanyDetailsStatus_View.as_view()),  #verified final time
    path("company_details_single/<slug:company_alias>/", CompanyDetailsSingle_View.as_view()), #verified final time
    path("company_header/<slug:company_alias>/", CompanyFrontPage_View.as_view()),  #verified final time
    path("company_details_edit/<slug:company_alias>/", CompanyDetailsSingleEdit_View.as_view()),  #verified final time
    path("company_details_delete/<slug:company_alias>/", CompanyDetailsSingleDelete_View.as_view()), #verified final time

    #company_sites 
    path("company_sites_details/<slug:company_alias>/", CompanySitesCompany_View.as_view()), #verified final time
    path("company_sites_details/<slug:company_alias>/<slug:site_alias>/", CompanySitesSingle_View.as_view()), #verified final time
    path("company_sites_details_edit/<slug:company_alias>/<slug:site_alias>/", CompanySitesSingleEdit_View.as_view()), #verified final time
    path("company_sites_details_delete/<slug:company_alias>/<slug:site_alias>/", CompanySitesSingleDelete_View.as_view()), #verified final time
    path("company_site_incharges/<slug:company_alias>/", CompanySiteIncharge_View.as_view()), 
    path("company_site_incharges/<slug:company_alias>/<slug:site_alias>/", CompanySiteInchargeSite_View.as_view()),
    path("company_site_incharges_edit/<slug:company_alias>/<slug:site_alias>/<int:site_incharge_id>/", CompanySiteInchargeEdit_View.as_view()),
    
    #company_depts
    path("company_depts_details/<slug:company_alias>/", CompanyDeptsCompany_View.as_view()), #verified final time
    path("company_depts_details/<slug:company_alias>/<slug:dept_alias>/", CompanyDeptsSingle_View.as_view()), #verified final time
    path("company_depts_details_edit/<slug:company_alias>/<slug:dept_alias>/", CompanyDeptsSingleEdit_View.as_view()), #verified final time
    path("company_depts_details_delete/<slug:company_alias>/<slug:dept_alias>/", CompanyDeptsSingleDelete_View.as_view()), #verified final time
    path("company_dept_incharges/", CompanyDeptsIncharge_View.as_view()),
    path("company_dept_incharges/dept/site/company", CompanyDeptsInchargeDept_View.as_view()),
    path("company_dept_incharges/dept/<int:dept_incharge_id>/site/company/edit/", CompanyDeptsInchargeEdit_View.as_view()),

] 

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
