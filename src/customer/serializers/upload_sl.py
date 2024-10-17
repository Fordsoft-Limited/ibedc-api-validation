from rest_framework import serializers
import pandas as pd
import json 
from core.custom_app_error import InvalidDataFormatException

import json
from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()  # File is required for upload
    constraints = serializers.JSONField(required=False)  # Optional constraints, can be blank

    def validate_file(self, file):
        """Validate file type and apply constraints for CSV and Excel files."""
        if file.name.endswith('.xlsx'):
            # Handle Excel file with constraints (if provided)
            constraints = self.initial_data.get('constraints', None)
            if constraints:
                constraints = self._parse_constraints(constraints)
                return self._validate_excel(file, constraints)
            else:
                return file

        elif file.name.endswith('.csv'):
            constraints = self.initial_data.get('constraints', None)
            if constraints:
                constraints = self._parse_constraints(constraints)
                return self._validate_csv(file, constraints)
            else:
                return file
        else:
            raise InvalidDataFormatException("Unsupported file type. Only .xlsx, .csv, .pdf, .jpg, .png, .gif, .txt, .doc, .ppt, and video files are allowed.")

    def _validate_excel(self, file, constraints):
        try:
            df = pd.read_excel(file)
        except Exception as e:
            raise InvalidDataFormatException(f"Error reading Excel file: {e}")

        self._validate_columns_and_dtypes(df, constraints)
        return file

    def _validate_csv(self, file, constraints):
        try:
            df = pd.read_csv(file)
        except Exception as e:
            raise InvalidDataFormatException(f"Error reading CSV file: {e}")

        self._validate_columns_and_dtypes(df, constraints)
        return file

    def _validate_columns_and_dtypes(self, df, constraints):
        errors = []  # Collect all validation errors here

        required_columns = set(constraints.keys())  # After parsing, constraints should be a dict
        file_columns = set(df.columns)

        # Check for missing and extra columns
        missing_columns = required_columns - file_columns
        extra_columns = file_columns - required_columns

        if missing_columns:
            errors.append(f"Missing columns: {', '.join(missing_columns)}")
        if extra_columns:
            errors.append(f"Extra columns not allowed: {', '.join(extra_columns)}")

        # Validate data types for each column
        for col, expected_dtype in constraints.items():
            if col in df.columns:
                actual_dtype = str(df[col].dtype)

                # Adjust the actual_dtype to display 'string' instead of 'object'
                actual_dtype_display = "string" if actual_dtype == "object" else actual_dtype

                if not self._dtype_matches(expected_dtype, actual_dtype, df[col]):
                    errors.append(
                        f"Incorrect data type for column '{col}'. Expected {expected_dtype}, got {actual_dtype_display}."
                    )

        # If there are any errors, raise a single ValidationError with all errors combined
        if errors:
            raise InvalidDataFormatException(message=" | ".join(errors), code=400)  # Combine errors into a single string

    def _dtype_matches(self, expected_dtype, actual_dtype, column_data):
        """Custom method to match expected and actual data types, handling int, float, str, date, bool."""
        dtype_mapping = {
        'int': 'int64',
        'float': 'float64',
        'str': 'object',  # Treat 'object' as 'str' in Pandas
        'date': 'datetime64[ns]',
        'bool': 'bool',
    }

        # Handle special case for date columns (actual_dtype is object if dates are not parsed correctly)
        if expected_dtype == 'date':
            try:
                pd.to_datetime(column_data)
                return True
            except (ValueError, TypeError):
                return False

        # Handle special case for boolean columns
        if expected_dtype == 'bool':
            return actual_dtype == 'bool' or column_data.isin([0, 1, True, False]).all()

        # General dtype matching
        return dtype_mapping.get(expected_dtype) == actual_dtype

    def _parse_constraints(self, constraints):
        """Helper function to parse constraints from JSON string to dict."""
        if isinstance(constraints, str) and constraints.strip():
            try:
                # Parse the JSON string into a Python dictionary
                constraints = json.loads(constraints)
            except json.JSONDecodeError:
                raise InvalidDataFormatException("Invalid JSON format for constraints.")
        else:
            constraints = {}  # If empty or not provided, return an empty dict
        if not isinstance(constraints, dict):
            raise InvalidDataFormatException("Constraints must be a valid JSON object.")
        return constraints

