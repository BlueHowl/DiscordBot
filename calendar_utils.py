import requests
from datetime import datetime, timedelta
from icalendar import Calendar
import logging

def get_birthday_message_if_today(ical_url):
    """
    Check iCal calendar for birthday events today and return formatted messages.
    
    Args:
        ical_url (str): URL to the iCal calendar feed
    
    Returns:
        str: Formatted birthday messages for today, or empty string if none
    """
    try:
        # Get today's date
        today = datetime.now().date()
        print(f"Checking for birthdays on: {today}")
        
        # Fetch the iCal data
        response = requests.get(ical_url)
        response.raise_for_status()
        
        # Parse the iCal data
        calendar = Calendar.from_ical(response.content)
        
        birthday_messages = []
        
        for component in calendar.walk():
            if component.name == "VEVENT":
                # Get event details
                summary = str(component.get('summary', ''))
                description = str(component.get('description', ''))
                start_date = component.get('dtstart')
                
                # Check if it's a birthday event
                if ('birthday' in summary.lower() or 'birthday' in description.lower() or 
                    'bday' in summary.lower() or 'anniversaire' in summary.lower()):
                    
                    # Handle different date formats
                    event_date = None
                    if start_date:
                        if hasattr(start_date.dt, 'date'):
                            event_date = start_date.dt.date()
                        elif hasattr(start_date.dt, 'year'):
                            event_date = start_date.dt
                        else:
                            event_date = start_date.dt
                    
                    # Check if it's today
                    if event_date and event_date == today:
                        # Extract person's name from summary
                        name = summary
                        for term in ['Birthday', 'birthday', "'s Birthday", "'s birthday", 'Bday', 'bday', 'Anniversaire', 'anniversaire']:
                            name = name.replace(term, '').strip()
                        
                        # Remove common prefixes/suffixes
                        name = name.replace('of ', '').replace('de ', '').strip()
                        
                        # Create birthday message
                        msg = (
                            f"🎂 BIRTHDAY ALERT 🎂\n"
                            f"Today is {name}'s Birthday!\n"
                            f"Don't forget to wish them a happy birthday! 🎉"
                        )
                        birthday_messages.append(msg)
        
        print(f"Found {len(birthday_messages)} birthday(s) today")
        return "\n\n".join(birthday_messages) if birthday_messages else ""
        
    except requests.RequestException as error:
        print(f"Error fetching calendar data: {error}")
        logging.error(f"Error fetching calendar data: {error}")
        return ""
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        logging.error(f"An unexpected error occurred: {error}")
        return ""


def get_upcoming_birthdays(ical_url, days_ahead=7):
    """
    Check iCal calendar for upcoming birthday events in the next few days.
    
    Args:
        ical_url (str): URL to the iCal calendar feed
        days_ahead (int): Number of days to look ahead (default: 7)
    
    Returns:
        str: Formatted upcoming birthday messages, or empty string if none
    """
    try:
        # Get date range
        today = datetime.now().date()
        start_date = today + timedelta(days=1)
        end_date = today + timedelta(days=days_ahead)
        
        print(f"Checking for upcoming birthdays from {start_date} to {end_date}")
        
        # Fetch the iCal data
        response = requests.get(ical_url)
        response.raise_for_status()
        
        # Parse the iCal data
        calendar = Calendar.from_ical(response.content)
        
        upcoming_birthdays = []
        
        for component in calendar.walk():
            if component.name == "VEVENT":
                # Get event details
                summary = str(component.get('summary', ''))
                description = str(component.get('description', ''))
                start_date_prop = component.get('dtstart')
                
                # Check if it's a birthday event
                if ('birthday' in summary.lower() or 'birthday' in description.lower() or 
                    'bday' in summary.lower() or 'anniversaire' in summary.lower()):
                    
                    # Handle different date formats
                    event_date = None
                    if start_date_prop:
                        if hasattr(start_date_prop.dt, 'date'):
                            event_date = start_date_prop.dt.date()
                        elif hasattr(start_date_prop.dt, 'year'):
                            event_date = start_date_prop.dt
                        else:
                            event_date = start_date_prop.dt
                    
                    # Check if it's in the upcoming range
                    if event_date and start_date <= event_date <= end_date:
                        # Extract person's name from summary
                        name = summary
                        for term in ['Birthday', 'birthday', "'s Birthday", "'s birthday", 'Bday', 'bday', 'Anniversaire', 'anniversaire']:
                            name = name.replace(term, '').strip()
                        
                        # Remove common prefixes/suffixes
                        name = name.replace('of ', '').replace('de ', '').strip()
                        
                        # Calculate days until birthday
                        days_until = (event_date - today).days
                        
                        # Create upcoming birthday message
                        if days_until == 1:
                            day_text = "tomorrow"
                        else:
                            day_text = f"in {days_until} days"
                        
                        msg = (
                            f"📅 UPCOMING BIRTHDAY 📅\n"
                            f"{name}'s Birthday is {day_text} ({event_date.strftime('%B %d')})!"
                        )
                        upcoming_birthdays.append((days_until, msg))
        
        # Sort by days until birthday
        upcoming_birthdays.sort(key=lambda x: x[0])
        messages = [msg for _, msg in upcoming_birthdays]
        
        print(f"Found {len(messages)} upcoming birthday(s)")
        return "\n\n".join(messages) if messages else ""
        
    except requests.RequestException as error:
        print(f"Error fetching calendar data: {error}")
        logging.error(f"Error fetching calendar data: {error}")
        return ""
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        logging.error(f"An unexpected error occurred: {error}")
        return ""


def list_calendar_events(ical_url, days_range=30):
    """
    List all events in the calendar for debugging purposes.
    
    Args:
        ical_url (str): URL to the iCal calendar feed
        days_range (int): Number of days to look ahead and behind (default: 30)
    
    Returns:
        list: List of event information dictionaries
    """
    try:
        # Get date range
        today = datetime.now().date()
        start_date = today - timedelta(days=days_range)
        end_date = today + timedelta(days=days_range)
        
        # Fetch the iCal data
        response = requests.get(ical_url)
        response.raise_for_status()
        
        # Parse the iCal data
        calendar = Calendar.from_ical(response.content)
        
        events = []
        
        for component in calendar.walk():
            if component.name == "VEVENT":
                summary = str(component.get('summary', ''))
                description = str(component.get('description', ''))
                start_date_prop = component.get('dtstart')
                
                # Handle different date formats
                event_date = None
                if start_date_prop:
                    if hasattr(start_date_prop.dt, 'date'):
                        event_date = start_date_prop.dt.date()
                    elif hasattr(start_date_prop.dt, 'year'):
                        event_date = start_date_prop.dt
                    else:
                        event_date = start_date_prop.dt
                
                # Only include events in our date range
                if event_date and start_date <= event_date <= end_date:
                    event_info = {
                        'date': event_date,
                        'summary': summary,
                        'description': description,
                        'is_birthday': ('birthday' in summary.lower() or 'birthday' in description.lower() or 
                                      'bday' in summary.lower() or 'anniversaire' in summary.lower())
                    }
                    events.append(event_info)
                    print(f"Event: {summary} on {event_date} (Birthday: {event_info['is_birthday']})")
        
        # Sort by date
        events.sort(key=lambda x: x['date'])
        return events
        
    except requests.RequestException as error:
        print(f"Error fetching calendar data: {error}")
        logging.error(f"Error fetching calendar data: {error}")
        return []
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        logging.error(f"An unexpected error occurred: {error}")
        return []


if __name__ == "__main__":
    ical_url = "https://calendar.google.com/calendar/ical/c_702b545902f6d85b61594f7a0105d1de9cd94496bd643c6449641761047313bc%40group.calendar.google.com/public/basic.ics"
    
    print("=== TESTING iCAL CALENDAR UTILS ===\n")
    
    # List all events for debugging
    print("=== LISTING ALL EVENTS ===")
    events = list_calendar_events(ical_url, days_range=30)
    
    if events:
        print(f"Found {len(events)} events in the calendar\n")
        
        # Test with today's birthdays
        print("=== CHECKING TODAY'S BIRTHDAYS ===")
        birthday_message = get_birthday_message_if_today(ical_url)
        if birthday_message:
            print("Birthday Message(s) for Today:")
            print(birthday_message)
        else:
            print("No birthdays scheduled for today.")
        
        print(f"\n=== CHECKING UPCOMING BIRTHDAYS ===")
        upcoming_message = get_upcoming_birthdays(ical_url, days_ahead=7)
        if upcoming_message:
            print("Upcoming Birthday Message(s):")
            print(upcoming_message)
        else:
            print("No upcoming birthdays in the next 7 days.")
    else:
        print("No events found or failed to fetch calendar data.")
