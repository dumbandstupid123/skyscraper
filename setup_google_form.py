"""
NextStep Client Needs Assessment - Google Form Setup Guide

This script provides the template and instructions for setting up your Google Form
for client needs assessment.

SETUP INSTRUCTIONS:
1. Go to forms.google.com
2. Create a new form
3. Title: "NextStep Client Needs Assessment"
4. Add the questions below in order
5. Set up the Google Sheet connection
6. Configure the environment variables

GOOGLE FORM QUESTIONS TO ADD:
"""

form_questions = [
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
        "description": "Your primary phone number",
        "required": False,
        "field_name": "Phone Number"
    },
    {
        "type": "Multiple choice",
        "question": "Do you currently need housing assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Housing Needs"
    },
    {
        "type": "Multiple choice",
        "question": "What type of housing would be most helpful?",
        "options": [
            "Emergency shelter", 
            "Transitional housing", 
            "Permanent housing", 
            "Senior housing",
            "Family housing",
            "Other"
        ],
        "required": False,
        "field_name": "Housing Type Preference"
    },
    {
        "type": "Multiple choice",
        "question": "How urgent is your housing need?",
        "options": ["Immediate (within 1 week)", "Soon (within 1 month)", "Within 3 months", "Within 6 months", "Planning ahead"],
        "required": False,
        "field_name": "Housing Timeline"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need food assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Food Assistance Needed"
    },
    {
        "type": "Paragraph",
        "question": "Any dietary restrictions or food preferences?",
        "description": "Please describe any allergies, dietary restrictions, or specific food needs",
        "required": False,
        "field_name": "Food Preferences"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need healthcare services?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Healthcare Needs"
    },
    {
        "type": "Multiple choice",
        "question": "How urgent is your healthcare need?",
        "options": ["Emergency", "Urgent", "Routine", "Preventive"],
        "required": False,
        "field_name": "Healthcare Priority"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need transportation assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Transportation Needs"
    },
    {
        "type": "Multiple choice",
        "question": "What type of transportation help do you need?",
        "options": ["Public transit passes", "Ride vouchers", "Gas cards", "Vehicle repair", "Other"],
        "required": False,
        "field_name": "Transportation Type"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need employment support?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Employment Support"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need educational support?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Education Support"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need child care assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Child Care Needs"
    },
    {
        "type": "Multiple choice",
        "question": "Do you need elder care assistance?",
        "options": ["Yes", "No"],
        "required": True,
        "field_name": "Elder Care Needs"
    },
    {
        "type": "Paragraph",
        "question": "Emergency Contact Information",
        "description": "Please provide name and phone number of someone we can contact in case of emergency",
        "required": False,
        "field_name": "Emergency Contacts"
    },
    {
        "type": "Paragraph",
        "question": "Additional Notes",
        "description": "Is there anything else you'd like us to know about your situation or needs?",
        "required": False,
        "field_name": "Additional Notes"
    },
    {
        "type": "Multiple choice",
        "question": "Please rank your most urgent need:",
        "options": ["Housing", "Food", "Healthcare", "Transportation", "Employment", "Education", "Child Care", "Elder Care", "Other"],
        "required": True,
        "field_name": "Priority Ranking"
    }
]

def print_form_setup_instructions():
    """Print detailed instructions for setting up the Google Form."""
    
    print("=" * 80)
    print("NEXTSTEP CLIENT NEEDS ASSESSMENT - GOOGLE FORM SETUP")
    print("=" * 80)
    
    print("\n1. CREATE THE GOOGLE FORM:")
    print("   - Go to forms.google.com")
    print("   - Click 'Blank form'")
    print("   - Title: 'NextStep Client Needs Assessment'")
    print("   - Description: 'Help us understand your current needs so we can provide the best support'")
    
    print("\n2. ADD THESE QUESTIONS IN ORDER:")
    print("-" * 50)
    
    for i, q in enumerate(form_questions, 1):
        print(f"\nQUESTION {i}:")
        print(f"   Type: {q['type']}")
        print(f"   Question: {q['question']}")
        if q.get('description'):
            print(f"   Description: {q['description']}")
        print(f"   Required: {q['required']}")
        if q.get('options'):
            print(f"   Options: {', '.join(q['options'])}")
        print(f"   Field Name (for mapping): {q['field_name']}")
    
    print("\n3. CONNECT TO GOOGLE SHEETS:")
    print("   - In your form, click 'Responses' tab")
    print("   - Click the green Sheets icon")
    print("   - Create a new spreadsheet or select existing")
    print("   - Name it: 'NextStep Needs Assessment Responses'")
    
    print("\n4. GET THE FORM AND SHEET IDs:")
    print("   - Form URL: https://forms.gle/FORM_ID")
    print("   - Sheet URL: https://docs.google.com/spreadsheets/d/SHEET_ID/")
    print("   - Copy these IDs for your environment variables")
    
    print("\n5. SET UP GOOGLE API CREDENTIALS:")
    print("   - Go to console.developers.google.com")
    print("   - Create a new project or select existing")
    print("   - Enable Google Sheets API")
    print("   - Create service account credentials")
    print("   - Download the JSON key file")
    
    print("\n6. ENVIRONMENT VARIABLES TO SET:")
    print("   GOOGLE_SHEETS_ID=your_spreadsheet_id")
    print("   GOOGLE_SERVICE_ACCOUNT_JSON='{\"type\":\"service_account\",...}'")
    print("   SENDGRID_API_KEY=your_sendgrid_key")
    print("   FROM_EMAIL=nextstep@yourdomain.com")
    print("   STAFF_NOTIFICATION_EMAIL=staff@yourdomain.com")
    
    print("\n7. UPDATE THE FORM URL IN server.py:")
    print("   - Replace 'YOUR_FORM_ID' with your actual form ID")
    print("   - Update the entry field IDs if needed")
    
    print("\n8. TEST THE INTEGRATION:")
    print("   - Fill out the form as a test client")
    print("   - Check that responses appear in the Google Sheet")
    print("   - Run the /api/process-form-responses endpoint")
    print("   - Verify client profiles are updated")
    
    print("\n" + "=" * 80)
    print("SETUP COMPLETE! Your two-way communication system is ready.")
    print("=" * 80)

if __name__ == "__main__":
    print_form_setup_instructions() 