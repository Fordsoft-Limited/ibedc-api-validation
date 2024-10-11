from rest_framework import serializers
from customer.models import Customer, CustomerBatch
from customer.web_service import call_external_api_to_validate_customer
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  
        fields = ['username', 'uid', 'name'] 

class CustomBatchSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model =CustomerBatch  
        fields = ['batch_code', 'uid', 'validation_type','created_by'] 

class CustomerBatchSerializer(serializers.ModelSerializer):
    created_by =UserSerializer(read_only=True)
    class Meta:
        model = CustomerBatch
        fields = [
            'slug', 'batch_code', 'validation_type', 'created_by',
            'total_approved', 'total_rejected', 'total_record','date_created','last_modified'
        ]
        


class CustomerSerializer(serializers.ModelSerializer):
    customer_batch = CustomBatchSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)

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
            'customer_has_account_no', 'customer_group', 'is_landlord', 'landlord_name', 'approved_by','approval_comments','aproval_status','date_approved',
            'landlord_phone', 'tenant_name', 'tenant_phone', 'meter_ct_ratio', 'customer_batch','slug','data_entry_history',
            'customer_no','date_created','last_modified','uid'
        ]
        read_only_fields = ['slug', 'customer_batch','data_entry_history','customer_no','approved_by','approval_comments',
                            'aproval_status','date_approved','date_created','last_modified','uid']

    def validate(self, data):
        """
        Validates the customer data by calling an external API and updates the data_entry_history.
        No saving should happen here; saving will be handled in create or update.
        """
        validation_result = call_external_api_to_validate_customer(data)

        account_no = data.get('account_no')
        customer_instance = Customer.objects.filter(account_no=account_no).first()

        if customer_instance:
            existing_history = getattr(customer_instance, 'data_entry_history', [])
            existing_history.extend(validation_result)
            data['data_entry_history'] = existing_history 
        else:
            data['data_entry_history'] = validation_result

        return data 
    def create(self, validated_data):
        """
        Create a new customer with the validated data.
        """
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing customer with the validated data.
        """
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


