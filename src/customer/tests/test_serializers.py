from django.test import TestCase
from io import BytesIO
import pandas as pd
from customer.serializers import FileUploadSerializer  
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from core.custom_app_error import InvalidDataFormatException


class FileUploadSerializerTest(TestCase):

    def setUp(self):
        """Set up test data and reusable file generation."""
        # Create a sample DataFrame to simulate Excel/CSV file content
        self.data = {
            'account_number': ['L123', 'T456', 'D789'],
            'first_name': ['John', 'Jane', 'Doe'],
            'last_name': ['Doe', 'Doe', 'Smith'],
            'email': ['john@example.com', 'jane@example.com', 'doe@example.com'],
            'dob': ['2020-01-01', '2021-02-01', '2019-03-01'],
            'amount': [123.45, 678.90, 234.56]
        }

        # Constraints that expect proper columns and types
        self.constraints = json.dumps({
            "account_number": "str",
            "first_name": "str",
            "last_name": "str",
            "email": "str",
            "dob": "date",
            "amount": "float"
        })

    def _create_excel_file(self, df):
        """Helper method to create an Excel file in memory."""
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        return SimpleUploadedFile(
            "test_file.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    def _create_csv_file(self, df):
        """Helper method to create a CSV file in memory."""
        csv_file = BytesIO()
        df.to_csv(csv_file, index=False)
        csv_file.seek(0)
        return SimpleUploadedFile(
            "test_file.csv",
            csv_file.read(),
            content_type="text/csv"
        )

    def test_file_upload_with_correct_constraints(self):
        """Test that the serializer validates the file and constraints successfully."""
        df = pd.DataFrame(self.data)
        excel_file = self._create_excel_file(df)

        data = {
            'constraints': self.constraints,
            'file': excel_file
        }

        serializer = FileUploadSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # If False, show errors

    def test_file_upload_with_csv(self):
        """Test that the serializer validates a CSV file with correct constraints successfully."""
        df = pd.DataFrame(self.data)
        csv_file = self._create_csv_file(df)

        data = {
            'constraints': self.constraints,
            'file': csv_file
        }

        serializer = FileUploadSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # If False, show errors

    def test_missing_columns(self):
        """Test that the serializer returns an error if required columns are missing."""
        # Remove 'email' column from the DataFrame
        invalid_data = self.data.copy()
        del invalid_data['email']
        df = pd.DataFrame(invalid_data)
        excel_file = self._create_excel_file(df)

        data = {'constraints': self.constraints, 'file': excel_file}
        serializer = FileUploadSerializer(data=data)

        with self.assertRaises(InvalidDataFormatException) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Missing columns", str(context.exception))

    def test_extra_columns(self):
        """Test that the serializer returns an error if extra columns are present."""
        # Add an extra column 'extra_column' to the DataFrame
        invalid_data = self.data.copy()
        invalid_data['extra_column'] = ['extra1', 'extra2', 'extra3']
        df = pd.DataFrame(invalid_data)
        excel_file = self._create_excel_file(df)

        data = {'constraints': self.constraints, 'file': excel_file}
        serializer = FileUploadSerializer(data=data)

        with self.assertRaises(InvalidDataFormatException) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Extra columns not allowed: extra_column", str(context.exception))

    def test_incorrect_data_types(self):
        """Test that the serializer returns an error if data types are incorrect."""
        # Change 'amount' column to strings (incorrect type)
        invalid_data = self.data.copy()
        invalid_data['amount'] = ['wrong_type', 'wrong_type', 'wrong_type']
        df = pd.DataFrame(invalid_data)
        excel_file = self._create_excel_file(df)

        data = {'constraints': self.constraints, 'file': excel_file}
        serializer = FileUploadSerializer(data=data)

        with self.assertRaises(InvalidDataFormatException) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Incorrect data type for column 'amount'. Expected float, got string", str(context.exception))

    def test_file_upload_without_constraints(self):
        """Test that the serializer allows file upload without constraints."""
        df = pd.DataFrame(self.data)
        excel_file = self._create_excel_file(df)

        serializer = FileUploadSerializer(data={'file': excel_file})
        self.assertTrue(serializer.is_valid(), serializer.errors)


    

