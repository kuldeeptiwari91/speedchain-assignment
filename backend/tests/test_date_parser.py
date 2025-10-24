import pytest
from datetime import datetime, timedelta
from utils.date_parser import parse_date, parse_time, format_datetime

class TestDateParser:
    def test_parse_today(self):
        expected = datetime.now().date().strftime('%Y-%m-%d')
        assert parse_date("today") == expected
    
    def test_parse_tomorrow(self):
        expected = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        assert parse_date("tomorrow") == expected
    
    def test_parse_standard_format(self):
        assert parse_date("2024-12-25") == "2024-12-25"
    
    def test_parse_invalid(self):
        assert parse_date("invalid date") is None


class TestTimeParser:
    def test_parse_12h_format(self):
        assert parse_time("2pm") == "14:00"
        assert parse_time("3:30pm") == "15:30"
        assert parse_time("10am") == "10:00"
    
    def test_parse_24h_format(self):
        assert parse_time("14:00") == "14:00"
        assert parse_time("09:30") == "09:30"
    
    def test_parse_phrases(self):
        assert parse_time("morning") == "09:00"
        assert parse_time("afternoon") == "14:00"
    
    def test_parse_invalid(self):
        assert parse_time("invalid") is None


class TestDateTimeFormatter:
    def test_format_datetime(self):
        result = format_datetime("2024-12-25", "14:00")
        assert "December 25, 2024" in result
        assert "2:00 PM" in result