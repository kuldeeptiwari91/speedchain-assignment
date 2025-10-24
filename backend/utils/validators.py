import re
from datetime import datetime, timedelta
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_date(date_str: str) -> bool:
    """
    Validate date format (YYYY-MM-DD)
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid and not in the past
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        
        # Check if date is not in the past
        if date_obj < today:
            return False
        
        # Check if date is not too far in future (e.g., 6 months)
        max_future_date = today + timedelta(days=180)
        if date_obj > max_future_date:
            return False
            
        return True
    except ValueError:
        return False


def validate_time(time_str: str, working_hours: tuple = ("09:00", "18:00")) -> bool:
    """
    Validate time format and business hours
    
    Args:
        time_str: Time string to validate (HH:MM)
        working_hours: Tuple of (start_time, end_time)
        
    Returns:
        True if valid and within working hours
    """
    try:
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        start_time = datetime.strptime(working_hours[0], '%H:%M').time()
        end_time = datetime.strptime(working_hours[1], '%H:%M').time()
        
        return start_time <= time_obj <= end_time
    except ValueError:
        return False


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid format
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-KATEX_INLINE_OPENKATEX_INLINE_CLOSE]', '', phone)
    
    # Check if it's a valid format (10-15 digits)
    pattern = r'^\+?[1-9]\d{9,14}$'
    return bool(re.match(pattern, cleaned))


def validate_service(service: str, available_services: list = None) -> bool:
    """
    Validate if service is available
    
    Args:
        service: Service name to validate
        available_services: List of available services
        
    Returns:
        True if service is available
    """
    if available_services is None:
        available_services = [
            "General Checkup",
            "Teeth Cleaning",
            "Root Canal",
            "Teeth Whitening",
            "Braces Consultation",
            "Dental Implants"
        ]
    
    # Case-insensitive match
    return service.lower() in [s.lower() for s in available_services]


def validate_dentist(dentist: str, available_dentists: list = None) -> bool:
    """
    Validate if dentist exists
    
    Args:
        dentist: Dentist name to validate
        available_dentists: List of available dentists
        
    Returns:
        True if dentist is available
    """
    if available_dentists is None:
        available_dentists = [
            "Dr. Emily Chen",
            "Dr. James Wilson",
            "Dr. Priya Sharma",
            "Dr. Mark Johnson"
        ]
    
    return dentist in available_dentists