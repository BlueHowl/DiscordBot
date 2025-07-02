import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.calendar_service import CalendarService

def test_calendar_service():
    ical_url = "https://calendar.google.com/calendar/ical/c_702b545902f6d85b61594f7a0105d1de9cd94496bd643c6449641761047313bc%40group.calendar.google.com/public/basic.ics"
    
    print("🗓️ TESTING CALENDAR SERVICE 🗓️\n")
    
    # Create CalendarService instance
    calendar_service = CalendarService(ical_url)
    
    # Test refresh
    print("Step 1: Testing calendar refresh...")
    refresh_result = calendar_service.refresh()
    if refresh_result:
        print("✅ Calendar refreshed successfully")
    else:
        print("❌ Failed to refresh calendar")
        return
    
    # First, list available events
    print("\nStep 2: Listing calendar events...")
    events = calendar_service.list_calendar_events(days_range=30)
    
    if not events:
        print("❌ No events found. Please check the calendar URL.")
        return
    
    print(f"✅ Found {len(events)} event(s)\n")
    
    # Test today's birthdays
    print("Step 3: Checking for today's birthdays...")
    today_birthdays = calendar_service.get_birthday_message_if_today()
    
    if today_birthdays:
        print("🎂 BIRTHDAYS TODAY:")
        print(today_birthdays)
    else:
        print("📅 No birthdays today")
    
    print("\n" + "="*50 + "\n")
    
    # Test upcoming birthdays
    print("Step 4: Checking for upcoming birthdays (next 7 days)...")
    upcoming_birthdays = calendar_service.get_upcoming_birthdays(days_ahead=7)
    
    if upcoming_birthdays:
        print("📅 UPCOMING BIRTHDAYS:")
        print(upcoming_birthdays)
    else:
        print("📅 No upcoming birthdays in the next 7 days")
    
    print("\n" + "="*50 + "\n")
    print("✅ Birthday test completed!")

def test_calendar_functions():
    """Test all calendar functions"""
    ical_url = "https://calendar.google.com/calendar/ical/c_702b545902f6d85b61594f7a0105d1de9cd94496bd643c6449641761047313bc%40group.calendar.google.com/public/basic.ics"
    
    print("=== TESTING CALENDAR FUNCTIONS ===\n")
    
    # Create CalendarService instance
    calendar_service = CalendarService(ical_url)
    
    # Test is_on_site_today
    print("1. Testing is_on_site_today():")
    try:
        result = calendar_service.is_on_site_today()
        print(f"   Result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test is_at_home_today
    print("2. Testing is_at_home_today():")
    try:
        result = calendar_service.is_at_home_today()
        print(f"   Result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test is_class_day_today
    print("3. Testing is_class_day_today():")
    try:
        result = calendar_service.is_class_day_today()
        print(f"   Result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Logic verification
    print("4. Logic verification:")
    try:
        on_site = calendar_service.is_on_site_today()
        at_home = calendar_service.is_at_home_today()
        class_day = calendar_service.is_class_day_today()
        
        print(f"   On Site: {on_site}")
        print(f"   At Home: {at_home}")
        print(f"   Class Day: {class_day}")
        
        # Verify logic
        expected_class_day = on_site or at_home
        if class_day == expected_class_day:
            print("   ✅ Logic is correct!")
        else:
            print(f"   ❌ Logic error: expected {expected_class_day}, got {class_day}")
            
    except Exception as e:
        print(f"   Error in logic verification: {e}")

def test_workshop_functions():
    """Test workshop-related functions"""
    ical_url = "https://calendar.google.com/calendar/ical/c_702b545902f6d85b61594f7a0105d1de9cd94496bd643c6449641761047313bc%40group.calendar.google.com/public/basic.ics"
    
    print("=== TESTING WORKSHOP FUNCTIONS ===\n")
    
    # Create CalendarService instance
    calendar_service = CalendarService(ical_url)
    
    # Test workshop today
    print("1. Testing get_workshop_message_if_today():")
    try:
        result = calendar_service.get_workshop_message_if_today()
        if result:
            print("🛠️ WORKSHOPS TODAY:")
            print(result)
        else:
            print("   No workshops today")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test upcoming workshops
    print("2. Testing get_upcoming_workshops():")
    try:
        result = calendar_service.get_upcoming_workshops(days_ahead=7)
        if result:
            print("🛠️ UPCOMING WORKSHOPS:")
            print(result)
        else:
            print("   No upcoming workshops in the next 7 days")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()

if __name__ == "__main__":
    # Run birthday tests
    test_calendar_service()
    
    print("\n" + "="*70 + "\n")
    
    # Run calendar function tests
    test_calendar_functions()
    
    print("\n" + "="*70 + "\n")
    
    # Run workshop function tests
    test_workshop_functions()
