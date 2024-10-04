
from django.db import models
from django.utils import timezone
from core.utils import generate_batch_code
from core.model import BaseModel


class CustomerBatch(BaseModel):
    VALIDATION_TYPE_CHOICES = [('Single', 'Single'), ('Bulk', 'Bulk')]
    REVIEW_STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    slug = models.SlugField(max_length=150, unique=True, blank=False)
    batch_code = models.CharField(max_length=6, default=generate_batch_code, unique=True, editable=False)
    validation_type = models.CharField(max_length=10, choices=VALIDATION_TYPE_CHOICES, default='Single')
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_batches')
    approved_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_batches')
    approval_comments = models.TextField(null=True, blank=True)
    aproval_status = models.CharField(max_length=10, choices=REVIEW_STATUS_CHOICES, default='Pending')
    date_approved = models.DateTimeField(null=True, blank=True)
    total_approved = models.PositiveIntegerField(default=0)
    total_rejected = models.PositiveIntegerField(default=0)
    total_record = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Batch {self.batch_code} - {self.validation_type}"
    
class Customer(BaseModel):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Closed', 'Closed'),
        ('Inactive', 'Inactive'),
    ]
    
    ACCOUNT_TYPE_CHOICES = [
        ('Postpaid', 'Postpaid'),
        ('Prepaid', 'Prepaid'),
    ]
    
    TARIFF_CODE_CHOICES = [
        ('R1', 'R1'), ('R2', 'R2'), ('R3', 'R3'),
        ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3'),
        ('D1', 'D1'), ('D2', 'D2'), ('D3', 'D3'),
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'),
        ('S1', 'S1'),
    ]
    
    ACCOUNT_CATEGORY_CHOICES = [
        ('Resident', 'Resident'),
        ('Commercial', 'Commercial'),
        ('Others', 'Others'),
    ]
    
    CONNECTION_TYPE_CHOICES = [
        ('Metered', 'Metered'),
        ('Un-Metered', 'Un-Metered'),
    ]
    
    SUPPLY_TYPE_CHOICES = [
        ('1-Phase', '1-Phase'),
        ('3-Phase', '3-Phase'),
    ]
    
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    METER_LOCATION_CHOICES = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ]
    
    CUSTOMER_GROUP_CHOICES = [
        ('New', 'New'),
        ('Potential', 'Potential'),
        ('Existing', 'Existing'),
    ]
    TARIFF_CLASS_CHOICES = [
    ('LFN', 'LFN'),
    ('NMD', 'NMD'),
    ('MD1', 'MD1'),
    ('MD2', 'MD2'),
    ('MD3', 'MD3'),
                ]
    
    slug = models.SlugField(max_length=150, unique=True, blank=False)
    customer_full_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=50)
    meter_no = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)  # Local Government Area
    state = models.CharField(max_length=100)  # State
    nearest_landmark = models.CharField(max_length=255, null=True, blank=True)
    setup_date = models.DateField(default=timezone.now)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    customer_id = models.CharField(max_length=200, null=True, blank=True)  # Unique customer ID
    cin = models.CharField(max_length=50, null=True, blank=True)  # Customer Identification Number
    application_date = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    status_code = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='Prepaid')
    current_tariff_code = models.CharField(max_length=2, choices=TARIFF_CODE_CHOICES, null=True, blank=True)
    correct_tariff_code = models.CharField(max_length=2, choices=TARIFF_CODE_CHOICES, null=True, blank=True)
    tariff_class = models.CharField(max_length=3, choices=TARIFF_CLASS_CHOICES, null=True, blank=True)
    feeder = models.CharField(max_length=255, null=True, blank=True)
    feeder_id = models.CharField(max_length=50, null=True, blank=True)
    service_center = models.CharField(max_length=255, null=True, blank=True)
    distribution_name = models.CharField(max_length=255, null=True, blank=True)
    dss_id = models.CharField(max_length=50, null=True, blank=True)
    lt_pole_id = models.CharField(max_length=50, null=True, blank=True)
    service_wire = models.CharField(max_length=255, null=True, blank=True)
    upriser = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    business_hub = models.CharField(max_length=255, null=True, blank=True)
    account_category = models.CharField(max_length=10, choices=ACCOUNT_CATEGORY_CHOICES)
    connection_type = models.CharField(max_length=10, choices=CONNECTION_TYPE_CHOICES)
    cust_nature_of_business = models.CharField(max_length=255, null=True, blank=True)
    customer_nin = models.CharField(max_length=20, null=True, blank=True)  # National Identification Number
    customer_supply_type = models.CharField(max_length=10, choices=SUPPLY_TYPE_CHOICES)
    customer_estimated_load = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cust_has_meter = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')
    customer_meter_category = models.CharField(max_length=50, null=True, blank=True)
    customer_meter_manufacturer = models.CharField(max_length=255, null=True, blank=True)
    customer_meter_saled = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')
    customer_meter_accessible = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='Yes')
    customer_meter_location = models.CharField(max_length=10, choices=METER_LOCATION_CHOICES, default='Outdoor')
    customer_bill_name = models.CharField(max_length=255, null=True, blank=True)
    customer_has_account_no = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='Yes')
    customer_group = models.CharField(max_length=10, choices=CUSTOMER_GROUP_CHOICES, default='New')
    is_landlord = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')
    landlord_name = models.CharField(max_length=255, null=True, blank=True)
    landlord_phone = models.CharField(max_length=15, null=True, blank=True)
    tenant_name = models.CharField(max_length=255, null=True, blank=True)
    tenant_phone = models.CharField(max_length=15, null=True, blank=True)
    meter_ct_ratio = models.CharField(max_length=50, null=True, blank=True)
    customer_batch = models.ForeignKey(CustomerBatch, on_delete=models.CASCADE, related_name="customers")

    def __str__(self):
        return f"{self.customer_full_name} - {self.account_no}"