import pytest
from utils.validators import (
    validate_email,
    validate_date,
    validate_time,
    validate_phone,
    validate_service,
    validate_dentist
)
from datetime import datetime, timedelta

class TestEmailValidator:
    def test_valid_email(self):
        assert validate_email("test@example.com") == True
        assert validate_email("user.name@domain.co.uk") == True
    
    def test_invalid_email(self):
        assert validate_email("invalid.email") == False
        assert validate_email("@example.com") == False
        assert validate_email("test@") == False


class TestDateValidator:
    def test_valid_future_date(self):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        assert validate_date(tomorrow) == True
    
    def test_invalid_past_date(self):
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        assert validate_date(yesterday) == False
    
    def test_invalid_format(self):
        assert validate_date("2024/12/25") == False
        assert validate_date("invalid-date") == False


class TestTimeValidator:
    def test_valid_business_hours(self):
        assert validate_time("10:00") == True
        assert validate_time("14:30") == True
        assert validate_time("17:59") == True
    
    def test_invalid_outside_hours(self):
        assert validate_time("08:00") == False
        assert validate_time("19:00") == False
    
    def test_invalid_format(self):
        assert validate_time("25:00") == False
        assert validate_time("invalid") == False


class TestPhoneValidator:
    def test_valid_phone(self):
        assert validate_phone("+1234567890") == True
        assert validate_phone("(555) 123-4567") == True
    
    def test_invalid_phone(self):
        assert validate_phone("123") == False
        assert validate_phone("invalid") == False


class TestServiceValidator:
    def test_valid_service(self):
        assert validate_service("Teeth Cleaning") == True
        assert validate_service("teeth cleaning") == True  # Case insensitive
    
    def test_invalid_service(self):
        assert validate_service("Invalid Service") == False


class TestDentistValidator:
    def test_valid_dentist(self):
        assert validate_dentist("Dr. Emily Chen") == True
    
    def test_invalid_dentist(self):
        assert validate_dentist("Dr. Unknown") == False