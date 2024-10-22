import datetime
from django.db import models

class CustomDateField(models.DateField):
    def __init__(self, *args, **kwargs):
        # Specify possible date formats that you want to accept
        self.input_formats = [
            '%Y-%m-%d',  # Standard YYYY-MM-DD
            '%Y/%m/%d',  # Accept YYYY/MM/DD
            '%d/%m/%Y',  # Accept DD/MM/YYYY
            '%m/%d/%Y',  # Optional: Accept MM/DD/YYYY
        ]
        super().__init__(*args, **kwargs)
    
    def clean(self, value):
        for format in self.input_formats:
            try:
                return datetime.strptime(value, format).date()  # Convert to date
            except (ValueError, TypeError):
                continue
        raise models.ValidationError(f'Invalid date format: {value}. Accepted formats are {self.input_formats}')
