import firebase_admin
from firebase_admin import credentials, auth
import os
from pathlib import Path

# Initialize Firebase Admin SDK
def initialize_firebase_admin():
    if not firebase_admin._apps:
        # For development, you can use a service account key file
        # For production, use environment variables or service account
        
        # Path to service account key (you'll need to download this from Firebase Console)
        service_account_path = Path(__file__).parent / "firebase-service-account.json"
        
        if service_account_path.exists():
            # Use service account key file
            cred = credentials.Certificate(str(service_account_path))
            firebase_admin.initialize_app(cred)
        else:
            # Use default credentials (works in production environments)
            try:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Warning: Could not initialize Firebase Admin SDK: {e}")
                print("Please download the service account key from Firebase Console")
                print("and save it as 'firebase-service-account.json' in the backend directory")
                return None
    
    return firebase_admin.get_app()

def verify_firebase_token(id_token):
    """Verify Firebase ID token and return user information"""
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        # Extract user information
        user_info = {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'name': decoded_token.get('name'),
            'email_verified': decoded_token.get('email_verified', False),
            'firebase_claims': decoded_token
        }
        
        return user_info
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

def get_user_by_uid(uid):
    """Get user information by UID"""
    try:
        user = auth.get_user(uid)
        return {
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
            'email_verified': user.email_verified,
            'created_at': user.user_metadata.creation_timestamp,
            'last_sign_in': user.user_metadata.last_sign_in_timestamp
        }
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

# Initialize Firebase Admin on import
initialize_firebase_admin() 