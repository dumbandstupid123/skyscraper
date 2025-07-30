import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
SCRIPT_DIR = Path(__file__).parent.absolute()
CLIENTS_FILE = SCRIPT_DIR / 'clients.json'
# --- End Configuration ---

def load_clients():
    """Loads clients, or returns a new structure if the file doesn't exist or is corrupt."""
    if CLIENTS_FILE.exists():
        with open(CLIENTS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.warning("clients.json is corrupted or empty. Starting fresh.")
                return {'clients': [], 'next_id': 1}
    return {'clients': [], 'next_id': 1}

def save_clients(clients_data):
    """Saves the clients data back to the JSON file."""
    with open(CLIENTS_FILE, 'w') as f:
        json.dump(clients_data, f, indent=2)

def create_detailed_client(profile):
    """Creates a single detailed fake client based on a profile."""
    first_name, last_name = profile['name'].split(' ', 1)
    
    # Generate a detailed, narrative-style note
    notes_narrative = (
        f"Client Name: {profile['name']}. Age: {profile['age']}. Gender: {profile.get('gender', 'N/A')}. "
        f"Family Status: {profile.get('family_status', 'N/A')}. "
        f"Employment: {profile.get('employment_status', 'N/A')}. "
    )
    if 'income_level' in profile:
        notes_narrative += f"Income: Approx. ${profile['income_level']}/year. "
    if profile.get('is_veteran'):
        notes_narrative += "Veteran Status: Yes. "
    if profile.get('has_disability'):
        notes_narrative += "Disability: Yes. "
    
    notes_narrative += f"Key Needs: {', '.join(profile.get('needs', []))}. "
    notes_narrative += f"Summary: {profile.get('summary', '')}"

    return {
        "id": None, # Will be assigned later
        "firstName": first_name,
        "lastName": last_name,
        "dateOfBirth": (datetime.now() - timedelta(days=365 * profile['age'])).strftime('%Y-%m-%d'),
        "gender": profile.get('gender', 'prefer-not-to-say'),
        "family_status": profile.get('family_status', 'Unknown'),
        "employment_status": profile.get('employment_status', 'Unknown'),
        "income_level": profile.get('income_level', 0),
        "is_veteran": profile.get('is_veteran', False),
        "has_disability": profile.get('has_disability', False),
        "needs": profile.get('needs', []),
        "notes": notes_narrative,
        "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
        "phoneNumber": f"832-555-{random.randint(1000, 9999)}",
        "address": f"{random.randint(100, 9999)} Main St, Houston, TX 77005"
    }

def main():
    """Main function to generate and save a diverse set of fake clients."""
    profiles = [
        {'name': 'Maria Garcia', 'age': 28, 'gender': 'Female', 'family_status': 'Single Mother', 'employment_status': 'Unemployed', 'income_level': 8000, 'needs': ['domestic violence support', 'housing assistance', 'childcare'], 'summary': 'Fleeing an abusive partner, needs safe housing for herself and her 2-year-old son.'},
        {'name': 'John "Smitty" Smith', 'age': 55, 'gender': 'Male', 'family_status': 'Single', 'employment_status': 'Employed part-time', 'income_level': 15000, 'is_veteran': True, 'needs': ['veteran services', 'mental health support', 'substance abuse treatment'], 'summary': 'Army veteran struggling with PTSD and alcohol dependency. Works odd jobs but needs stable employment.'},
        {'name': 'Emily White', 'age': 8, 'gender': 'Female', 'family_status': 'In foster care', 'employment_status': 'Not applicable', 'needs': ['child welfare services', 'educational support', 'therapy'], 'summary': 'Recently placed in foster care due to parental neglect. Needs a stable, supportive environment.'},
        {'name': 'David Johnson', 'age': 72, 'gender': 'Male', 'family_status': 'Widowed', 'employment_status': 'Retired', 'income_level': 12000, 'has_disability': True, 'needs': ['senior housing', 'medical care', 'meal delivery'], 'summary': 'Lives alone on a fixed income and has mobility issues after a recent fall.'},
        {'name': 'Jessica Rodriguez', 'age': 22, 'gender': 'Female', 'family_status': 'Single', 'employment_status': 'Student', 'needs': ['lgbtq+ support', 'homeless shelter', 'job training'], 'summary': 'College student who was kicked out after coming out to her family. Currently homeless.'},
        {'name': 'Michael Brown', 'age': 41, 'gender': 'Male', 'family_status': 'Married with children', 'employment_status': 'Unemployed', 'needs': ['legal aid', 'employment services', 'financial assistance'], 'summary': 'Recently laid off from a factory job. Facing eviction and needs legal help to navigate the process.'},
        {'name': 'Sarah Miller', 'age': 34, 'gender': 'Female', 'family_status': 'Married', 'employment_status': 'Employed full-time', 'income_level': 45000, 'needs': ['mental health counseling', 'support group'], 'summary': 'Struggling with severe postpartum depression after the birth of her second child.'},
        {'name': 'Chris Davis', 'age': 19, 'gender': 'Non-binary', 'family_status': 'Single', 'employment_status': 'Unemployed', 'needs': ['transitional housing', 'job placement', 'mental health support'], 'summary': 'Aged out of the foster care system and is unprepared for independent living. Experiences anxiety.'},
        {'name': 'Robert Wilson', 'age': 65, 'gender': 'Male', 'family_status': 'Single', 'employment_status': 'Retired', 'is_veteran': True, 'income_level': 22000, 'needs': ['permanent supportive housing', 'disability benefits assistance'], 'summary': 'Vietnam veteran with chronic health issues looking for stable, long-term housing.'},
        {'name': 'Linda Martinez', 'age': 25, 'gender': 'Female', 'family_status': 'Pregnant', 'employment_status': 'Employed part-time', 'income_level': 18000, 'needs': ['prenatal care', 'housing assistance', 'WIC enrollment'], 'summary': 'First-time mother working a low-wage job. Needs support to ensure a healthy pregnancy and stable housing.'}
    ]

    logging.info("Regenerating all clients with detailed profiles for testing...")
    
    # Start with a fresh list
    clients_data = {'clients': [], 'next_id': 1}
    
    for profile in profiles:
        new_client = create_detailed_client(profile)
        new_client['id'] = clients_data['next_id']
        clients_data['next_id'] += 1
        clients_data['clients'].append(new_client)

    save_clients(clients_data)
    logging.info(f"Successfully generated {len(clients_data['clients'])} detailed client profiles.")
    logging.info(f"Client data saved to {CLIENTS_FILE}")

if __name__ == "__main__":
    main() 