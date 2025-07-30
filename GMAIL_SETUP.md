# Gmail App Password Setup Guide

## Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the steps to enable 2-Step Verification if not already enabled

## Step 2: Generate App Password
1. Go back to Security settings
2. Under "Signing in to Google", click "App passwords"
3. Select "Mail" as the app
4. Select "Other (custom name)" as the device
5. Enter "NextStep Social Worker" as the name
6. Click "Generate"
7. **Copy the 16-character app password** (it will look like: abcd efgh ijkl mnop)

## Step 3: Update Server Configuration
Edit `clean-repo/backend/server.py` lines 32-36:

```python
# Set up SMTP email configuration
os.environ['SMTP_SERVER'] = 'smtp.gmail.com'
os.environ['SMTP_PORT'] = '587'
os.environ['SMTP_USERNAME'] = 'your-actual-gmail@gmail.com'  # Your Gmail address
os.environ['SMTP_PASSWORD'] = 'abcd efgh ijkl mnop'  # Your App Password (spaces removed)
os.environ['FROM_EMAIL'] = 'your-actual-gmail@gmail.com'  # Your Gmail address
os.environ['FROM_NAME'] = 'NextStep Social Worker'
```

## Step 4: Test Email Sending
After updating the configuration, restart the server and test the contact functionality.

## Current Configuration
- **All client emails updated to:** `hk80@rice.edu`
- **All messages will be sent to:** `hk80@rice.edu` 
- **Emails will appear to come from:** Your Gmail address
- **From name will be:** "NextStep Social Worker"

## Security Notes
- **Never commit app passwords to version control**
- **App passwords bypass 2FA, so keep them secure**
- **You can revoke app passwords anytime from Google Account settings**
- **Use environment variables for production deployments** 