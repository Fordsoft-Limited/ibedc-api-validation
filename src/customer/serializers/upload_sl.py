import os
from rest_framework import serializers
import pandas as pd
from core import settings
from core.custom_app_error import InvalidDataFormatException
from customer.models import CustomerBatch
import logging

from customer.tasks import process_customer_records

logger = logging.getLogger(__name__)

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()  # File is required for upload

    def _get_constraints(self):
            """Returns a set of required columns for customer data."""
            return {
                'customer_full_name',
                'account_no',
                'meter_no',
                'address',
                'city',
                'lga',
                'state',
                'nearest_landmark',
                'setup_date',
                'latitude',
                'longitude',
                'customer_id',
                'cin',
                'application_date',
                'mobile',
                'email',
                'status_code',
                'account_type',
                'current_tariff_code',
                'correct_tariff_code',
                'tariff_class',
                'feeder',
                'feeder_id',
                'service_center',
                'distribution_name',
                'dss_id',
                'lt_pole_id',
                'service_wire',
                'upriser',
                'region',
                'business_hub',
                'account_category',
                'connection_type',
                'cust_nature_of_business',
                'customer_nin',
                'customer_supply_type',
                'customer_estimated_load',
                'cust_has_meter',
                'customer_meter_category',
                'customer_meter_manufacturer',
                'customer_meter_saled',
                'customer_meter_accessible',
                'customer_meter_location',
                'customer_bill_name',
                'customer_has_account_no',
                'customer_group',
                'is_landlord',
                'landlord_name',
                'landlord_phone',
                'tenant_name',
                'tenant_phone',
                'meter_ct_ratio',
            }

    def validate_file(self, file):
            """Validate file type and ensure that the correct format (CSV or Excel) is provided."""
            if file.name.endswith('.xlsx'):
                return self._validate_excel(file)
            elif file.name.endswith('.csv'):
                return self._validate_csv(file)
            else:
                raise InvalidDataFormatException("Unsupported file type. Only .xlsx and .csv files are allowed.")

    def _validate_excel(self, file):
            try:
                df = pd.read_excel(file)
                self.context['total_record'] = len(df)
            except Exception as e:
                raise InvalidDataFormatException(f"Error reading Excel file: {e}")

            constraints = self._get_constraints()
            self._validate_columns(df, constraints)
            return file

    def _validate_csv(self, file):
            try:
                df = pd.read_csv(file)
                self.context['total_record'] = len(df)
            except Exception as e:
                raise InvalidDataFormatException(f"Error reading CSV file: {e}")

            constraints = self._get_constraints()
            self._validate_columns(df, constraints)
            return file

    def _validate_columns(self, df, constraints):
                errors = []  

                required_columns = constraints
                file_columns = set(df.columns)

                # Check for missing and extra columns
                missing_columns = required_columns - file_columns
                extra_columns = file_columns - required_columns

                if missing_columns:
                    errors.append(f"Missing columns: {', '.join(missing_columns)}")
                if extra_columns:
                    errors.append(f"Extra columns not allowed: {', '.join(extra_columns)}")

                # If there are any errors, raise a single ValidationError with all errors combined
                if errors:
                    raise InvalidDataFormatException(message=" | ".join(errors), code=400)
    def save(self):
                """Create a batch entry, save the file, and trigger asynchronous processing."""
                try:
                    user = self.context['user']
                    total_record = self.context.get('total_record', 0)

                    # Create a batch record for the file
                    batch = CustomerBatch.objects.create(
                        created_by=user,
                        validation_type='Bulk',
                        upload_histories=[],
                        total_approved=0,
                        total_rejected=0,
                        total_record=total_record,
                    )

                    # Save the uploaded file to external storage
                    file = self.validated_data['file']
                    external_file_path = os.path.join(settings.EXTERNAL_STORAGE_ROOT, file.name)

                    with open(external_file_path, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)

                    # Trigger asynchronous task to process the file
                    process_customer_records.delay(batch.id, external_file_path)

                    return batch

                except Exception as e:
                    logger.error(f"Error during save: {str(e)}")
                    raise InvalidDataFormatException("Error creating batch.")


        
