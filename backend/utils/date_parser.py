from datetime import datetime, timedelta
import re
from typing import Optional, Tuple

def parse_date(date_str: str) -> Optional[str]:
    """
    Parse natural language date to YYYY-MM-DD format
    
    Args:
        date_str: Natural language date (e.g., "tomorrow", "next monday")
        
    Returns:
        Formatted date string or None
    """
    date_str = date_str.lower().strip()
    today = datetime.now().date()
    
    # Handle common phrases
    if date_str in ['today', 'now']:
        return today.strftime('%Y-%m-%d')
    
    if date_str == 'tomorrow':
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    if 'next week' in date_str:
        return (today + timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Handle "next [day]" - e.g., "next monday"
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    for day_name, day_num in weekdays.items():
        if day_name in date_str:
            days_ahead = day_num - today.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    
    # Try to parse standard formats
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y']
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt).date()
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return None


def parse_time(time_str: str) -> Optional[str]:
    """
    Parse natural language time to HH:MM format
    
    Args:
        time_str: Natural language time (e.g., "2pm", "3:30 PM", "afternoon")
        
    Returns:
        Formatted time string (24-hour) or None
    """
    time_str = time_str.lower().strip()
    
    # Handle common phrases
    time_phrases = {
        'morning': '09:00',
        'noon': '12:00',
        'afternoon': '14:00',
        'evening': '17:00'
    }
    
    for phrase, time_val in time_phrases.items():
        if phrase in time_str:
            return time_val
    
    # Handle "3pm", "3:30pm", "15:00" formats
    patterns = [
        (r'(\d{1,2}):(\d{2})\s*(am|pm)?', lambda h, m, ap: format_12h_to_24h(int(h), int(m), ap)),
        (r'(\d{1,2})\s*(am|pm)', lambda h, ap: format_12h_to_24h(int(h), 0, ap)),
        (r'(\d{1,2}):(\d{2})', lambda h, m: f"{int(h):02d}:{int(m):02d}")
    ]
    
    for pattern, formatter in patterns:
        match = re.search(pattern, time_str)
        if match:
            try:
                return formatter(*match.groups())
            except:
                continue
    
    return None


def format_12h_to_24h(hour: int, minute: int, am_pm: Optional[str]) -> str:
    """Convert 12-hour format to 24-hour format"""
    if am_pm:
        if am_pm.lower() == 'pm' and hour != 12:
            hour += 12
        elif am_pm.lower() == 'am' and hour == 12:
            hour = 0
    
    return f"{hour:02d}:{minute:02d}"


def format_datetime(date_str: str, time_str: str) -> str:
    """
    Format date and time for display
    
    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HH:MM format
        
    Returns:
        Formatted datetime string
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        time_obj = datetime.strptime(time_str, '%H:%M')
        
        # Format: "Monday, January 15, 2024 at 2:00 PM"
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        formatted_time = time_obj.strftime('%I:%M %p').lstrip('0')
        
        return f"{formatted_date} at {formatted_time}"
    except:
        return f"{date_str} at {time_str}"


def get_day_of_week(date_str: str) -> Optional[str]:
    """Get day of week from date string"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%A')
    except:
        return None


def is_weekend(date_str: str) -> bool:
    """Check if date is weekend (Sunday)"""
    day = get_day_of_week(date_str)
    return day == 'Sunday' if day else False