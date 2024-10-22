from rest_framework import serializers
from core.custom_app_error import RecordNotFoundException, StandardApplicationException
from customer.models import Customer, CustomerBatch
from customer.web_service import call_external_api_to_validate_customer
from users.models import CustomUser
from django.utils import timezone

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
            'batch_code','uid', 'validation_type', 
            'total_approved', 'total_rejected', 'total_record',
            'date_created','last_modified','created_by',
        ]

class CustomerBatchDetailSerializer(serializers.ModelSerializer):
    created_by =UserSerializer(read_only=True)
    class Meta:
        model = CustomerBatch
        fields = [
            'batch_code', 'validation_type', 
            'total_approved', 'total_rejected', 'total_record',
            'date_created','last_modified','created_by','upload_histories'
        ]
        
class CustomerSerializer(serializers.ModelSerializer):
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
            'landlord_phone', 'tenant_name', 'tenant_phone', 'meter_ct_ratio', 
            'customer_no','date_created','last_modified','uid'
        ]
        
        
class CustomerDetailsSerializer(serializers.ModelSerializer):
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
            'landlord_phone', 'tenant_name', 'tenant_phone', 'meter_ct_ratio', 'customer_batch','data_entry_history',
            'customer_no','date_created','last_modified','uid'
        ]
        read_only_fields = ['customer_batch','data_entry_history','customer_no','approved_by','approval_comments',
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
            existing_history = customer_instance.data_entry_history if customer_instance.data_entry_history else []
            existing_history.extend(validation_result)
            self.instance = customer_instance
            self.instance.data_entry_history = existing_history
        else:
            data['data_entry_history'] = [validation_result]
        return data 
    def create(self, validated_data):
            user = self.context.get('created_by')
            pre_saved_batch = self.context.get('customer_batch')
            customer_batch =  CustomerBatch.objects.create(
            created_by=user,
            validation_type='Single',
            total_record=1
        ) if not pre_saved_batch else pre_saved_batch
           
            validated_data['customer_batch'] = customer_batch
            customer_instance = Customer.objects.create(**validated_data)
            return customer_instance

    def update(self, instance, validated_data):
        """
        Update an existing customer with the validated data.
        """
        for key, value in validated_data.items():
            if key  not in ['data_entry_history']:
                    setattr(instance, key, value)
        instance.save()
        return instance

class ApproveRejectCustomerSerializer(serializers.Serializer):
    uid = serializers.UUIDField(required=True)  # UUID field for the customer
    approval_status = serializers.ChoiceField(choices=[('Approved', 'Rejected')], required=True)
    approval_comments = serializers.CharField(max_length=500, required=False)  # Optional comment field

    def validate(self, data):
        """
        Custom validation to ensure the customer exists and can be approved/rejected.
        """
        uid = data.get('uid')
        try:
            customer = Customer.objects.get(uid=uid)
        except Customer.DoesNotExist:
            raise RecordNotFoundException("Customer with this UID does not exist.")
        if customer.aproval_status in ['Approved', 'Rejected']:
            raise StandardApplicationException(f"Customer has already been {customer.aproval_status.lower()}.")
        self.customer = customer
        return data

    def update(self, instance, validated_data):
        """
        Update the customer with the approval status and update CustomerBatch counts.
        """
        instance.aproval_status = validated_data.get('approval_status', instance.aproval_status)
        instance.approval_comments = validated_data.get('approval_comments', instance.approval_comments)
        instance.approved_by = self.context['request'].user
        instance.date_approved = timezone.now()
        instance.save()

        # Update the batch counts
        customer_batch = instance.customer_batch  # Access the related CustomerBatch
        if instance.aproval_status == 'Approved':
            customer_batch.total_approved += 1
        elif instance.aproval_status == 'Rejected':
            customer_batch.total_rejected += 1

        customer_batch.save()

        return instance

