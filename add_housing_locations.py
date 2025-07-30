#!/usr/bin/env python3
"""
Add location data to housing resources to enable map functionality.
"""

import json
import re
from pathlib import Path

def extract_address_from_text(text):
    """Extract address from text using common address patterns."""
    if not text:
        return None
    
    # Common Houston address patterns
    address_patterns = [
        # Full address with street number, name, city, state, zip
        r'(\d+\s+[A-Za-z0-9\s\.\-]+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ln|Lane|Way|Pkwy|Parkway),?\s*Houston,?\s*TX\s*\d{5})',
        # Address with just street and Houston TX
        r'(\d+\s+[A-Za-z0-9\s\.\-]+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ln|Lane|Way|Pkwy|Parkway),?\s*Houston,?\s*TX)',
        # Just street address (we'll add Houston, TX)
        r'(\d+\s+[A-Za-z0-9\s\.\-]+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ln|Lane|Way|Pkwy|Parkway))'
    ]
    
    for pattern in address_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            address = match.group(1).strip()
            # Clean up the address
            address = re.sub(r'\s+', ' ', address)  # Remove extra spaces
            address = address.replace(',', ', ')  # Ensure proper comma spacing
            
            # Add Houston, TX if not present
            if 'houston' not in address.lower():
                address += ', Houston, TX'
            
            return address
    
    return None

def get_known_housing_addresses():
    """Return a dictionary of known addresses for major housing organizations."""
    return {
        'open door mission': '3312 Milam St, Houston, TX 77002',
        'magnificat houses': '2402 Rosewood St, Houston, TX 77004',
        'txbunkhouse': '2020 N Main St, Houston, TX 77009',
        'united states veterans initiative': '2000 Crawford St, Houston, TX 77002',
        'wellsprings village': '1823 Rusk St, Houston, TX 77002',
        'salvation army': '1603 McGowen St, Houston, TX 77004',
        'star of hope': '419 Dowling St, Houston, TX 77003',
        'covenant house': '1111 Lovett Blvd, Houston, TX 77006',
        'houston recovery center': '315 W 3rd St, Houston, TX 77007',
        'bridge over troubled waters': '1818 Chenevert St, Houston, TX 77003',
        'family promise': '4410 Almeda Rd, Houston, TX 77004',
        'avenue 360': '2900 Weslayan St, Houston, TX 77027',
        'interfaith ministries': '3303 Main St, Houston, TX 77002',
        'harris center': '9401 Southwest Fwy, Houston, TX 77074',
        'mental health america': '2211 Norfolk St, Houston, TX 77098'
    }

def add_housing_locations():
    """Add location data to housing resources."""
    script_dir = Path(__file__).parent
    resources_file = script_dir / 'structured_resources.json'
    backup_file = script_dir / 'structured_resources_backup_before_location_fix.json'
    
    if not resources_file.exists():
        print(f"Error: {resources_file} not found")
        return
    
    # Load the current resources
    with open(resources_file, 'r') as f:
        resources = json.load(f)
    
    # Create backup
    with open(backup_file, 'w') as f:
        json.dump(resources, f, indent=2)
    print(f"Backup created: {backup_file}")
    
    known_addresses = get_known_housing_addresses()
    fixed_count = 0
    
    for resource in resources:
        if resource.get('category') != 'housing':
            continue
        
        # Skip if already has a valid location
        if resource.get('location') and resource['location'] not in ['Not specified', 'Not listed', 'N/A']:
            continue
        
        organization = resource.get('organization', '').lower()
        contact = resource.get('contact', '')
        services = resource.get('services', '')
        key_features = resource.get('key_features', '')
        
        location = None
        
        # Try to find address in known addresses
        for org_key, address in known_addresses.items():
            if org_key in organization:
                location = address
                break
        
        # If not found in known addresses, try to extract from contact info
        if not location:
            location = extract_address_from_text(contact)
        
        # Try to extract from services field
        if not location:
            location = extract_address_from_text(services)
        
        # Try to extract from key_features field
        if not location:
            location = extract_address_from_text(key_features)
        
        # If still no location, set a default based on organization type
        if not location:
            if 'downtown' in organization or 'central' in organization:
                location = 'Downtown Houston, TX'
            elif 'north' in organization or 'heights' in organization:
                location = 'North Houston, TX'
            elif 'south' in organization:
                location = 'South Houston, TX'
            elif 'west' in organization or 'katy' in organization:
                location = 'West Houston, TX'
            elif 'east' in organization:
                location = 'East Houston, TX'
            else:
                location = 'Houston, TX'
        
        # Update the resource
        resource['location'] = location
        
        print(f"Added location to: {resource.get('organization', 'Unknown')} - {resource.get('program_type', 'Unknown')}")
        print(f"  Location: {location}")
        print()
        
        fixed_count += 1
    
    # Save the updated resources
    with open(resources_file, 'w') as f:
        json.dump(resources, f, indent=2)
    
    print(f"Added location data to {fixed_count} housing resources")
    print(f"Updated file: {resources_file}")

if __name__ == "__main__":
    add_housing_locations() 