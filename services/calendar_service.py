import requests
from datetime import datetime, timedelta
from icalendar import Calendar
import logging


class CalendarService:
    """
    A service class for handling iCal calendar operations.
    Provides methods for checking birthdays, workshops, and class schedules.
    """
    
    def __init__(self, ical_url):
        """
        Initialize the CalendarService with an iCal URL.
        
        Args:
            ical_url (str): URL to the iCal calendar feed
        """
        self.ical_url = ical_url
        self._calendar_data = None
        self._last_refresh = None
        
    def refresh(self):
        """
        Refresh the calendar data by fetching from the iCal URL.
        
        Returns:
            bool: True if refresh was successful, False otherwise
        """
        try:
            print(f"Refreshing calendar data from: {self.ical_url}")
            response = requests.get(self.ical_url)
            response.raise_for_status()
            
            self._calendar_data = Calendar.from_ical(response.content)
            self._last_refresh = datetime.now()
            print(f"Calendar refreshed successfully at {self._last_refresh}")
            return True
            
        except requests.RequestException as error:
            print(f"Error fetching calendar data: {error}")
            logging.error(f"Error fetching calendar data: {error}")
            return False
        except Exception as error:
            print(f"An unexpected error occurred during refresh: {error}")
            logging.error(f"An unexpected error occurred during refresh: {error}")
            return False
    
    def _ensure_calendar_data(self):
        """
        Ensure calendar data is available, refresh if needed.
        
        Returns:
            bool: True if calendar data is available, False otherwise
        """
        if self._calendar_data is None:
            return self.refresh()
        return True
    
    def _extract_event_date(self, start_date_prop):
        """
        Extract date from iCal date property, handling different formats.
        
        Args:
            start_date_prop: iCal date property
            
        Returns:
            tuple: (event_date, event_time_str) or (None, "")
        """
        event_date = None
        event_time_str = ""
        
        if start_date_prop:
            if hasattr(start_date_prop.dt, 'date'):
                event_date = start_date_prop.dt.date()
                if hasattr(start_date_prop.dt, 'time'):
                    event_time_str = start_date_prop.dt.strftime('%H:%M')
            elif hasattr(start_date_prop.dt, 'year'):
                event_date = start_date_prop.dt
            else:
                event_date = start_date_prop.dt
                
        return event_date, event_time_str
    
    def _is_birthday_event(self, summary, description):
        """Check if an event is a birthday event."""
        return ('birthday' in summary.lower() or 'birthday' in description.lower() or 
                'bday' in summary.lower() or 'anniversaire' in summary.lower())
    
    def _is_workshop_event(self, summary, description):
        """Check if an event is a workshop event."""
        return ('workshop' in summary.lower() or 'workshop' in description.lower() or 
                'atelier' in summary.lower() or 'formation' in summary.lower() or
                'training' in summary.lower())
    
    def _is_on_site_event(self, summary, description):
        """Check if an event is an 'On Site' event."""
        return ('on site' in summary.lower() or 'on site' in description.lower() or 
                'onsite' in summary.lower() or 'onsite' in description.lower())
    
    def _is_at_home_event(self, summary, description):
        """Check if an event is an 'At home' event."""
        return ('at home' in summary.lower() or 'at home' in description.lower() or 
                'athome' in summary.lower() or 'from home' in summary.lower() or
                'remote' in summary.lower())
    
    def get_birthday_message_if_today(self):
        """
        Check iCal calendar for birthday events today and return formatted messages.
        
        Returns:
            str: Formatted birthday messages for today, or empty string if none
        """
        if not self._ensure_calendar_data():
            return ""
            
        try:
            # Get today's date
            today = datetime.now().date()
            print(f"Checking for birthdays on: {today}")
            
            birthday_messages = []
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    # Get event details
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date = component.get('dtstart')
                    
                    # Check if it's a birthday event
                    if self._is_birthday_event(summary, description):
                        event_date, _ = self._extract_event_date(start_date)
                        
                        # Check if it's today
                        if event_date and event_date == today:
                            # Extract person's name from summary
                            birthday_person = summary.strip()
                            
                            # Clean up common birthday prefixes
                            for prefix in ['Birthday of ', 'birthday of ', 'Happy Birthday ', 'happy birthday ', 
                                         'Birthday: ', 'birthday: ', 'Anniversaire de ', 'anniversaire de ']:
                                if birthday_person.startswith(prefix):
                                    birthday_person = birthday_person[len(prefix):].strip()
                            
                            # Create birthday message
                            msg = f"🎂 HAPPY BIRTHDAY 🎂\nIt's {birthday_person}'s birthday today! 🎉🎈"
                            
                            # Add description if available
                            if description and description.strip() and description.strip() != summary.strip():
                                desc_clean = description.strip()
                                if len(desc_clean) > 80:
                                    desc_clean = desc_clean[:80] + "..."
                                msg += f"\n📝 {desc_clean}"
                            
                            birthday_messages.append(msg)
            
            print(f"Found {len(birthday_messages)} birthday(s) today")
            return "\n\n".join(birthday_messages) if birthday_messages else ""
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return ""

    def get_upcoming_birthdays(self, days_ahead=7):
        """
        Check iCal calendar for upcoming birthday events in the next few days.
        
        Args:
            days_ahead (int): Number of days to look ahead (default: 7)
        
        Returns:
            str: Formatted upcoming birthday messages, or empty string if none
        """
        if not self._ensure_calendar_data():
            return ""
            
        try:
            # Get date range
            today = datetime.now().date()
            start_date = today + timedelta(days=1)
            end_date = today + timedelta(days=days_ahead)
            
            print(f"Checking for upcoming birthdays from {start_date} to {end_date}")
            
            upcoming_birthdays = []
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    # Get event details
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date_prop = component.get('dtstart')
                    
                    # Check if it's a birthday event
                    if self._is_birthday_event(summary, description):
                        event_date, _ = self._extract_event_date(start_date_prop)
                        
                        # Check if it's in the upcoming range
                        if event_date and start_date <= event_date <= end_date:
                            # Extract person's name from summary
                            birthday_person = summary.strip()
                            
                            # Clean up common birthday prefixes
                            for prefix in ['Birthday of ', 'birthday of ', 'Happy Birthday ', 'happy birthday ', 
                                         'Birthday: ', 'birthday: ', 'Anniversaire de ', 'anniversaire de ']:
                                if birthday_person.startswith(prefix):
                                    birthday_person = birthday_person[len(prefix):].strip()
                            
                            # Calculate days until birthday
                            days_until = (event_date - today).days
                            
                            # Create upcoming birthday message
                            if days_until == 1:
                                day_text = "tomorrow"
                            else:
                                day_text = f"in {days_until} days"
                            
                            msg = (
                                f"📅 UPCOMING BIRTHDAY 📅\n"
                                f"{birthday_person}'s Birthday is {day_text} ({event_date.strftime('%B %d')})!"
                            )
                            upcoming_birthdays.append((days_until, msg))
            
            # Sort by days until birthday
            upcoming_birthdays.sort(key=lambda x: x[0])
            messages = [msg for _, msg in upcoming_birthdays]
            
            print(f"Found {len(messages)} upcoming birthday(s)")
            return "\n\n".join(messages) if messages else ""
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return ""

    def get_workshop_message_if_today(self):
        """
        Check iCal calendar for workshop events today and return formatted messages.
        
        Returns:
            str: Formatted workshop messages for today, or empty string if none
        """
        if not self._ensure_calendar_data():
            return ""
            
        try:
            # Get today's date
            today = datetime.now().date()
            print(f"Checking for workshops on: {today}")
            
            workshop_messages = []
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    # Get event details
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date = component.get('dtstart')
                    
                    # Check if it's a workshop event
                    if self._is_workshop_event(summary, description):
                        event_date, event_time_str = self._extract_event_date(start_date)
                        
                        # Check if it's today
                        if event_date and event_date == today:
                            # Extract workshop title from summary
                            workshop_title = summary.strip()
                            
                            # Clean up common workshop prefixes
                            for prefix in ['Workshop ', 'workshop ', 'Atelier ', 'atelier ']:
                                if workshop_title.startswith(prefix):
                                    workshop_title = workshop_title[len(prefix):].strip()
                            
                            # Create workshop message
                            time_part = f" at {event_time_str}" if event_time_str else ""
                            msg = f"🛠️ WORKSHOP TODAY 🛠️\n{workshop_title} is scheduled for today{time_part}!"
                            
                            # Add description if available
                            if description and description.strip() and description.strip() != summary.strip():
                                desc_clean = description.strip()
                                if len(desc_clean) > 80:
                                    desc_clean = desc_clean[:80] + "..."
                                msg += f"\n📝 {desc_clean}"
                            
                            workshop_messages.append(msg)
            
            print(f"Found {len(workshop_messages)} workshop(s) today")
            return "\n\n".join(workshop_messages) if workshop_messages else ""
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return ""

    def get_upcoming_workshops(self, days_ahead=7):
        """
        Check iCal calendar for upcoming workshop events in the next few days.
        
        Args:
            days_ahead (int): Number of days to look ahead (default: 7)
        
        Returns:
            str: Formatted upcoming workshop messages, or empty string if none
        """
        if not self._ensure_calendar_data():
            return ""
            
        try:
            # Get date range
            today = datetime.now().date()
            start_date = today + timedelta(days=1)
            end_date = today + timedelta(days=days_ahead)
            
            print(f"Checking for upcoming workshops from {start_date} to {end_date}")
            
            upcoming_workshops = []
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    # Get event details
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date_prop = component.get('dtstart')
                    
                    # Check if it's a workshop event
                    if self._is_workshop_event(summary, description):
                        event_date, event_time_str = self._extract_event_date(start_date_prop)
                        
                        # Check if it's in the upcoming range
                        if event_date and start_date <= event_date <= end_date:
                            # Extract workshop title from summary
                            workshop_title = summary.strip()
                            
                            # Clean up common workshop prefixes
                            for prefix in ['Workshop ', 'workshop ', 'Atelier ', 'atelier ']:
                                if workshop_title.startswith(prefix):
                                    workshop_title = workshop_title[len(prefix):].strip()
                            
                            # Calculate days until workshop
                            days_until = (event_date - today).days
                            
                            # Create upcoming workshop message
                            if days_until == 1:
                                day_text = "tomorrow"
                            else:
                                day_text = f"in {days_until} days"
                            
                            time_part = f" at {event_time_str}" if event_time_str else ""
                            
                            msg = (
                                f"🛠️ UPCOMING WORKSHOP 🛠️\n"
                                f"{workshop_title} is {day_text} ({event_date.strftime('%B %d')}){time_part}!"
                            )
                            
                            # Add description if available
                            if description and description.strip() and description.strip() != summary.strip():
                                desc_clean = description.strip()
                                if len(desc_clean) > 80:
                                    desc_clean = desc_clean[:80] + "..."
                                msg += f"\n📝 {desc_clean}"
                            
                            upcoming_workshops.append((days_until, msg))
            
            # Sort by days until workshop
            upcoming_workshops.sort(key=lambda x: x[0])
            messages = [msg for _, msg in upcoming_workshops]
            
            print(f"Found {len(messages)} upcoming workshop(s)")
            return "\n\n".join(messages) if messages else ""
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return ""

    def is_on_site_today(self):
        """
        Check iCal calendar to see if today is marked as "On Site".
        
        Returns:
            bool: True if today is marked as "On Site", False otherwise
        """
        if not self._ensure_calendar_data():
            return False
            
        try:
            # Get today's date
            today = datetime.now().date()
            print(f"Checking if today ({today}) is marked as On Site")
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    # Get event details
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date = component.get('dtstart')
                    
                    # Check if it's an "On Site" event
                    if self._is_on_site_event(summary, description):
                        event_date, _ = self._extract_event_date(start_date)
                        
                        # Check if it's today
                        if event_date and event_date == today:
                            print(f"Found 'On Site' event for today: {summary}")
                            return True
            
            print("No 'On Site' event found for today")
            return False
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return False

    def is_at_home_today(self):
        """
        Check iCal calendar to see if today is marked as "At home".
        
        Returns:
            bool: True if today is marked as "At home", False otherwise
        """
        if not self._ensure_calendar_data():
            return False
            
        try:
            # Get today's date
            today = datetime.now().date()
            print(f"Checking if today ({today}) is marked as At home")
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    # Get event details
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date = component.get('dtstart')
                    
                    # Check if it's an "At home" event
                    if self._is_at_home_event(summary, description):
                        event_date, _ = self._extract_event_date(start_date)
                        
                        # Check if it's today
                        if event_date and event_date == today:
                            print(f"Found 'At home' event for today: {summary}")
                            return True
            
            print("No 'At home' event found for today")
            return False
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return False

    def is_class_day_today(self):
        """
        Check iCal calendar to see if today is a class day (either "On Site" or "At home").
        
        Returns:
            bool: True if today has either "On Site" or "At home" event, False otherwise
        """
        return self.is_on_site_today() or self.is_at_home_today()

    def list_calendar_events(self, days_range=30):
        """
        List all events in the calendar for debugging purposes.
        
        Args:
            days_range (int): Number of days to look ahead and behind (default: 30)
        
        Returns:
            list: List of event information dictionaries
        """
        if not self._ensure_calendar_data():
            return []
            
        try:
            # Get date range
            today = datetime.now().date()
            start_date = today - timedelta(days=days_range)
            end_date = today + timedelta(days=days_range)
            
            events = []
            
            for component in self._calendar_data.walk():
                if component.name == "VEVENT":
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    start_date_prop = component.get('dtstart')
                    
                    event_date, event_time_str = self._extract_event_date(start_date_prop)
                    
                    # Only include events in our date range
                    if event_date and start_date <= event_date <= end_date:
                        events.append({
                            'date': event_date,
                            'time': event_time_str,
                            'summary': summary,
                            'description': description,
                            'is_birthday': self._is_birthday_event(summary, description),
                            'is_workshop': self._is_workshop_event(summary, description),
                            'is_on_site': self._is_on_site_event(summary, description),
                            'is_at_home': self._is_at_home_event(summary, description)
                        })
            
            # Sort by date
            events.sort(key=lambda x: x['date'])
            return events
            
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            logging.error(f"An unexpected error occurred: {error}")
            return []