#!/usr/bin/env python3
"""
Fix corrupted resource data where schedule information got mixed into website and other fields.
"""

import json
import re
from pathlib import Path

def clean_website_field(website_value):
    """Clean the website field by extracting only the URL part."""
    if not website_value or website_value in ["Not listed", "N/A", "Not specified"]:
        return "Not listed"
    
    # Extract just the URL part (everything before the first space or schedule info)
    # Look for patterns like "Schedule Information" or "Intake Hours" 
    url_match = re.match(r'(https?://[^\s]+)', website_value)
    if url_match:
        return url_match.group(1)
    
    # If no URL found, return "Not listed"
    return "Not listed"

def extract_schedule_from_corrupted_field(corrupted_value):
    """Extract schedule information from corrupted fields."""
    if not corrupted_value:
        return None
    
    # Look for schedule information patterns
    schedule_patterns = [
        r'Schedule Information.*?(?=Distribution Days:|$)',
        r'Intake Hours:.*?(?=Distribution Days:|$)', 
        r'Distribution Days:.*?(?=Location|$)',
        r'Check-in begins.*?(?=Distribution Days:|$)'
    ]
    
    extracted_info = []
    for pattern in schedule_patterns:
        matches = re.findall(pattern, corrupted_value, re.DOTALL | re.IGNORECASE)
        extracted_info.extend(matches)
    
    return ' '.join(extracted_info).strip() if extracted_info else None

def fix_resource_data():
    """Fix the corrupted resource data."""
    script_dir = Path(__file__).parent
    resources_file = script_dir / 'structured_resources.json'
    backup_file = script_dir / 'structured_resources_backup_before_fix.json'
    
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
    
    fixed_count = 0
    
    for resource in resources:
        original_website = resource.get('website', '')
        
        # Check if website field is corrupted (contains schedule info)
        if original_website and any(keyword in original_website.lower() for keyword in 
                                  ['schedule information', 'intake hours', 'distribution days', 'check-in begins']):
            
            # Clean the website field
            clean_website = clean_website_field(original_website)
            resource['website'] = clean_website
            
            # Extract schedule information and update appropriate fields
            schedule_info = extract_schedule_from_corrupted_field(original_website)
            if schedule_info:
                # Update intake_hours if it's generic or missing
                if not resource.get('intake_hours') or resource.get('intake_hours') in ['Not specified', 'Not listed']:
                    if 'intake hours:' in schedule_info.lower() or 'check-in begins' in schedule_info.lower():
                        resource['intake_hours'] = schedule_info
                
                # Update available_days if it's generic or missing  
                if not resource.get('available_days') or resource.get('available_days') in ['Not specified', 'Not listed']:
                    if 'distribution days:' in schedule_info.lower():
                        resource['available_days'] = schedule_info
            
            print(f"Fixed resource: {resource.get('organization', 'Unknown')} - {resource.get('program_type', 'Unknown')}")
            print(f"  Original website: {original_website[:100]}...")
            print(f"  Clean website: {clean_website}")
            print(f"  Extracted schedule: {schedule_info[:100] if schedule_info else 'None'}...")
            print()
            
            fixed_count += 1
    
    # Save the fixed resources
    with open(resources_file, 'w') as f:
        json.dump(resources, f, indent=2)
    
    print(f"Fixed {fixed_count} corrupted resources")
    print(f"Updated file: {resources_file}")

if __name__ == "__main__":
    fix_resource_data() 