# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=Customer)
def create_customer_no(sender, instance, created, **kwargs):
    """
    Automatically generate a unique 11-digit customer number when a Customer is created.
    """
    if created and not instance.customer_no:
        # Generate customer_no based on the ID (which is auto-incrementing)
        # Padding to ensure it's 11 digits
        customer_no = str(instance.id).zfill(11)
        instance.customer_no = customer_no
        instance.save(update_fields=['customer_no'])  # Save only the customer_no
