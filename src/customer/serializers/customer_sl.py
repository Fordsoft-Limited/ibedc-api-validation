from rest_framework import serializers
from customer.models import Customer, CustomerBatch

class CustomerBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBatch
        fields = [
            'slug', 'batch_code', 'validation_type', 'created_by', 'approved_by', 
            'approval_comments', 'aproval_status', 'date_approved', 
            'total_approved', 'total_rejected', 'total_record'
        ]
        read_only_fields = ['slug', 'batch_code', 'created_by', 'total_approved', 'total_rejected', 'total_record', 'date_approved']


class CustomerSerializer(serializers.ModelSerializer):
    customer_batch = CustomerBatchSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'customer_full_name', 'account_no', 'meter_no', 'address', 'city', 'lga', 'state',
            'nearest_landmark', 'setup_date', 'latitude', 'longitude', 'customer_id', 'cin', 
            'application_date', 'mobile', 'email', 'status_code', 'account_type', 
            'current_tariff_code', 'correct_tariff_code', 'tariff_class', 'feeder', 'feeder_id', 
            'service_center', 'distribution_name', 'dss_id', 'lt_pole_id', 'service_wire', 'upriser', 
            'region', 'business_hub', 'account_category', 'connection_type', 'cust_nature_of_business', 
            'customer_nin', 'customer_supply_type', 'customer_estimated_load', 'cust_has_meter', 
            'customer_meter_category', 'customer_meter_manufacturer', 'customer_meter_saled', 
            'customer_meter_accessible', 'customer_meter_location', 'customer_bill_name', 
            'customer_has_account_no', 'customer_group', 'is_landlord', 'landlord_name', 
            'landlord_phone', 'tenant_name', 'tenant_phone', 'meter_ct_ratio', 'customer_batch','slug'
        ]
        read_only_fields = ['slug', 'customer_batch']


