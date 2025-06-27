"""
Test script for calendar_utils_ical.py
Run this to test the iCal calendar birthday functionality
"""

from calendar_utils import get_birthday_message_if_today, get_upcoming_birthdays, list_calendar_events

def test_calendar_utils():
    ical_url = "https://calendar.google.com/calendar/ical/c_702b545902f6d85b61594f7a0105d1de9cd94496bd643c6449641761047313bc%40group.calendar.google.com/public/basic.ics"
    
    print("🗓️ TESTING iCAL CALENDAR BIRTHDAY CHECKER 🗓️\n")
    
    # First, list available events
    print("Step 1: Listing calendar events...")
    events = list_calendar_events(ical_url, days_range=30)
    
    if not events:
        print("❌ No events found. Please check the calendar URL.")
        return
    
    print(f"✅ Found {len(events)} event(s)\n")
    
    # Test today's birthdays
    print("Step 2: Checking for today's birthdays...")
    today_birthdays = get_birthday_message_if_today(ical_url)
    
    if today_birthdays:
        print("🎂 BIRTHDAYS TODAY:")
        print(today_birthdays)
    else:
        print("📅 No birthdays today")
    
    print("\n" + "="*50 + "\n")
    
    # Test upcoming birthdays
    print("Step 3: Checking for upcoming birthdays (next 7 days)...")
    upcoming_birthdays = get_upcoming_birthdays(ical_url, days_ahead=7)
    
    if upcoming_birthdays:
        print("📅 UPCOMING BIRTHDAYS:")
        print(upcoming_birthdays)
    else:
        print("📅 No upcoming birthdays in the next 7 days")
    
    print("\n" + "="*50 + "\n")
    print("✅ Test completed!")

if __name__ == "__main__":
    test_calendar_utils()
