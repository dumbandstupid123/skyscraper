"""
NextStep Client Needs Assessment - SIMPLIFIED Google Form Setup Guide

This script provides a simplified template with only the most essential needs:
- Housing
- Food  
- Transportation

SETUP INSTRUCTIONS:
1. Go to forms.google.com
2. Create a new form
3. Title: "NextStep Client Needs Assessment - Quick Check"
4. Add the questions below in order
5. Set up the Google Sheet connection
6. Configure the environment variables
"""

simple_form_questions = [
    {
        "type": "Short answer",
        "question": "Email Address",
        "description": "Please enter your email address (this helps us match your response to your profile)",
        "required": True,
        "field_name": "Client Email"
    },
    {
        "type": "Short answer", 
        "question": "Full Name",
        "description": "Please enter your first and last name",
        "required": True,
        "field_name": "Client Name"
    },
    {
        "type": "Short answer",
        "question": "Phone Number",
        "description": "Your primary phone number (optional)",
        "required": False,
        "field_name": "Phone Number"
    },
    # HOUSING SECTION
    {
        "type": "Multiple choice",
        "question": "Do you currently need housing assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Housing Needs"
    },
    {
        "type": "Multiple choice",
        "question": "If yes, how urgent is your housing need?",
        "options": ["Emergency (within 1 week)", "Urgent (within 1 month)", "Soon (within 3 months)", "Planning ahead", "Not applicable"],
        "required": False,
        "field_name": "Housing Priority"
    },
    # FOOD SECTION
    {
        "type": "Multiple choice",
        "question": "Do you need food assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Food Needs"
    },
    {
        "type": "Multiple choice",
        "question": "If yes, how urgent is your food need?",
        "options": ["Emergency (today)", "Urgent (this week)", "Soon (this month)", "Ongoing support", "Not applicable"],
        "required": False,
        "field_name": "Food Priority"
    },
    # TRANSPORTATION SECTION
    {
        "type": "Multiple choice",
        "question": "Do you need transportation assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Transportation Needs"
    },
    {
        "type": "Multiple choice",
        "question": "If yes, what type of transportation help do you need?",
        "options": ["Public transit passes", "Ride vouchers/Uber credits", "Gas cards", "Vehicle repair help", "Other", "Not applicable"],
        "required": False,
        "field_name": "Transportation Type"
    },
    # PRIORITY AND NOTES
    {
        "type": "Multiple choice",
        "question": "What is your most urgent need right now?",
        "options": ["Housing", "Food", "Transportation", "Other"],
        "required": True,
        "field_name": "Top Priority"
    },
    {
        "type": "Paragraph",
        "question": "Additional Notes",
        "description": "Is there anything else you'd like us to know about your current situation?",
        "required": False,
        "field_name": "Additional Notes"
    }
]

def print_simple_form_setup():
    """Print instructions for the simplified Google Form."""
    
    print("=" * 80)
    print("NEXTSTEP CLIENT NEEDS ASSESSMENT - SIMPLIFIED SETUP")
    print("Focus: Housing, Food, Transportation")
    print("=" * 80)
    
    print("\n1. CREATE THE GOOGLE FORM:")
    print("   - Go to forms.google.com")
    print("   - Click 'Blank form'")
    print("   - Title: 'NextStep Client Needs Assessment - Quick Check'")
    print("   - Description: 'Quick assessment to understand your current housing, food, and transportation needs'")
    
    print("\n2. ADD THESE QUESTIONS IN ORDER:")
    print("-" * 50)
    
    for i, q in enumerate(simple_form_questions, 1):
        print(f"\nQUESTION {i}:")
        print(f"   Type: {q['type']}")
        print(f"   Question: {q['question']}")
        if q.get('description'):
            print(f"   Description: {q['description']}")
        print(f"   Required: {q['required']}")
        if q.get('options'):
            print(f"   Options: {', '.join(q['options'])}")
        print(f"   📊 Column Name in Sheets: '{q['field_name']}'")
    
    print("\n3. CONNECT TO GOOGLE SHEETS:")
    print("   - In your form, click 'Responses' tab")
    print("   - Click the green Sheets icon")
    print("   - Create a new spreadsheet")
    print("   - Name it: 'NextStep Simple Needs Assessment'")
    
    print("\n4. VERIFY COLUMN NAMES:")
    print("   Make sure your Google Sheet has these EXACT column names:")
    for q in simple_form_questions:
        print(f"   - '{q['field_name']}'")
    
    print("\n5. GET YOUR IDs:")
    print("   - Form URL: https://forms.gle/YOUR_FORM_ID")
    print("   - Sheet URL: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/")
    
    print("\n6. ENVIRONMENT VARIABLES:")
    print("   Add to your .env file:")
    print("   GOOGLE_SHEETS_ID=your_sheet_id_here")
    print("   GOOGLE_SERVICE_ACCOUNT_JSON='{\"type\":\"service_account\",...}'")
    print("   SENDGRID_API_KEY=your_sendgrid_key (optional)")
    print("   FROM_EMAIL=nextstep@yourdomain.com")
    
    print("\n7. TEST THE FORM:")
    print("   - Fill out your form as a test")
    print("   - Check responses appear in Google Sheets")
    print("   - Run: curl http://localhost:5001/api/process-form-responses")
    
    print("\n" + "=" * 80)
    print("SIMPLIFIED SETUP COMPLETE!")
    print("Your clients can now update their housing, food, and transportation needs")
    print("=" * 80)

def get_google_sheets_headers():
    """Return the expected column headers for easy copy-paste."""
    headers = [q['field_name'] for q in simple_form_questions]
    return headers

if __name__ == "__main__":
    print_simple_form_setup()
    
    print("\n\n🔄 QUICK COPY-PASTE HEADERS:")
    print("If you need to manually set column names in Google Sheets:")
    headers = get_google_sheets_headers()
    print("Timestamp\t" + "\t".join(headers))
    print("\n(Copy the line above and paste as your first row in Google Sheets)") 