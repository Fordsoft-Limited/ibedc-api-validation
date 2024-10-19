import logging
from celery import shared_task
import pandas as pd
from customer.models import CustomerBatch, Customer
from customer.serializers.customer_sl import CustomerSerializer

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def process_customer_records(batch_id, file_path):
    """Asynchronously process customer records from the uploaded file."""
    batch = CustomerBatch.objects.get(id=batch_id)

    try:
        # Load the file using pandas based on its extension
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)

        errors = []
        total_approved = 0
        total_rejected = 0

        # Process each row
        for index, row in df.iterrows():
            customer_data = row.to_dict()
            serializer = CustomerSerializer(data=customer_data)

            if serializer.is_valid():
                serializer.save()
                total_approved += 1
            else:
                # Collect any errors for failed records
                errors.append({
                    "row": index + 1,
                    "errors": serializer.errors
                })
                total_rejected += 1

        # Save failed records to batch as JSON
        batch.upload_histories = errors
        batch.total_approved = total_approved
        batch.total_rejected = total_rejected
        batch.total_record = len(df)  # Total number of records in the file

    except Exception as e:
        # Log any unexpected errors during processing
        logger.error(f"Error processing batch {batch_id}: {str(e)}")
        batch.upload_histories.append({"error": str(e)})

    finally:
        # Ensure we save the batch state whether an error occurred or not
        batch.save()
