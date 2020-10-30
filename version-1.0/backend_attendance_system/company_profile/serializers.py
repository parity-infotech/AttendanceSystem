from rest_framework import serializers
from .models import ( CompanyDetails, CompanySites, CompanySiteIncharge, CompanyDepts, CompanyDeptIncharge)

class CompanyDetails_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ('__all__')

class CompanyDetails_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ('company_name', 'company_ceo', 'company_billing_address', 'company_telephone', 'company_email', 
                'company_logo')
        read_only_fields = ('company_id', 'company_founding_date', 'company_CIN_num', 'company_alias')

class CompanySites_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySites
        fields = ('__all__')

class CompanySites_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySites
        fields = ('site_name', 'site_id', 'site_address','site_telephone')
        read_only_fields = ('site_s_num', 'company_id', 'site_GST_num', 'site_alias')

class CompanySiteIncharge_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySiteIncharge
        fields = ('__all__')

class CompanySiteIncharge_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySiteIncharge
        fields = ('__all__')
        write_only_fields = ('site_incharge_id', 'site_incharge_to', 'site_incharge_record_last_modification')
        
class CompanyDepts_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDepts
        fields = ('dept_id', 'dept_name', 'dept_description', 'dept_alias', 'dept_logo')

class CompanyDepts_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDepts
        fields = ('dept_id', 'dept_name', 'dept_description', 'dept_logo')
        read_only_fields = ('dept_s_num', 'site_s_num', 'dept_alias', 'company_id', 'dept_status')

class CompanyDeptsIncharge_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDeptIncharge
        fields = ('__all__')

class CompanyDeptsIncharge_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDeptIncharge
        fields = ('__all__')
        write_only_fields = ('dept_s_num', 'dept_incharge_to', 'dept_incharge_record_last_modification')