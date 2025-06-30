#!/usr/bin/env python3
"""
Test script to verify the calendar utility functions work correctly.
"""

from calendar_utils import is_on_site_today, is_at_home_today, is_class_day_today

# iCal URL from your main.py
ical_url = "https://calendar.google.com/calendar/ical/c_702b545902f6d85b61594f7a0105d1de9cd94496bd643c6449641761047313bc%40group.calendar.google.com/public/basic.ics"

def test_calendar_functions():
    """Test all calendar functions"""
    print("=== TESTING CALENDAR FUNCTIONS ===\n")
    
    # Test is_on_site_today
    print("1. Testing is_on_site_today():")
    try:
        result = is_on_site_today(ical_url)
        print(f"   Result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test is_at_home_today
    print("2. Testing is_at_home_today():")
    try:
        result = is_at_home_today(ical_url)
        print(f"   Result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test is_class_day_today
    print("3. Testing is_class_day_today():")
    try:
        result = is_class_day_today(ical_url)
        print(f"   Result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Logic verification
    print("4. Logic verification:")
    try:
        on_site = is_on_site_today(ical_url)
        at_home = is_at_home_today(ical_url)
        class_day = is_class_day_today(ical_url)
        
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

if __name__ == "__main__":
    test_calendar_functions()
