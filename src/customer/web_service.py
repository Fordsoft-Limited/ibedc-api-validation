import datetime
def call_external_api_to_validate_customer(customer_data):
     return  [{
                'is_valid': True,
                'message': 'Validation successful',
                'validation_date': datetime.datetime.now().isoformat()
            }]
