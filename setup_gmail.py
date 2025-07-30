#!/usr/bin/env python3
"""
Script to easily update Gmail configuration in server.py
Run this after getting your Gmail App Password
"""

import re

def update_gmail_config():
    print("🔧 Gmail Configuration Setup")
    print("=" * 50)
    
    # Get user input
    gmail_address = input("Enter your Gmail address (e.g., yourname@gmail.com): ").strip()
    app_password = input("Enter your 16-character App Password (spaces will be removed): ").strip()
    
    # Remove spaces from app password
    app_password = app_password.replace(' ', '')
    
    # Validate inputs
    if not gmail_address or '@gmail.com' not in gmail_address:
        print("❌ Invalid Gmail address. Please include @gmail.com")
        return
    
    if len(app_password) != 16:
        print(f"❌ App password should be 16 characters. You entered {len(app_password)} characters.")
        return
    
    # Read server.py file
    try:
        with open('server.py', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ server.py not found. Make sure you're in the backend directory.")
        return
    
    # Replace placeholders
    content = re.sub(
        r"os\.environ\['SMTP_USERNAME'\] = 'PUT_YOUR_GMAIL_HERE@gmail\.com'",
        f"os.environ['SMTP_USERNAME'] = '{gmail_address}'",
        content
    )
    
    content = re.sub(
        r"os\.environ\['SMTP_PASSWORD'\] = 'PUT_YOUR_16_CHAR_APP_PASSWORD_HERE'",
        f"os.environ['SMTP_PASSWORD'] = '{app_password}'",
        content
    )
    
    content = re.sub(
        r"os\.environ\['FROM_EMAIL'\] = 'PUT_YOUR_GMAIL_HERE@gmail\.com'",
        f"os.environ['FROM_EMAIL'] = '{gmail_address}'",
        content
    )
    
    # Write back to file
    with open('server.py', 'w') as f:
        f.write(content)
    
    print("✅ Gmail configuration updated successfully!")
    print(f"📧 Gmail: {gmail_address}")
    print(f"🔑 App Password: {app_password[:4]}{'*' * 8}{app_password[-4:]}")
    print("\n🔄 Please restart the server for changes to take effect:")
    print("   pkill -f 'python server.py' && python server.py")

if __name__ == "__main__":
    update_gmail_config() 