#!/usr/bin/env python3
"""
Script to parse the new PDF content and add/update resources in structured_resources.json
"""

import json
import re
from pathlib import Path
import hashlib

def clean_text(text):
    """Clean up text by removing extra spaces and normalizing"""
    if not text:
        return ""
    # Remove extra spaces and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def generate_resource_id(organization, program_type):
    """Generate a unique resource ID based on organization and program type"""
    combined = f"{organization}_{program_type}".lower()
    return f"res_{hash(combined) % 10**16}"

def extract_field_value(content, field_name, start_pos):
    """Extract field value from content starting at a position"""
    pattern = rf'{field_name}:\s*([^A-Z][^:]*?)(?=\s*[A-Z][^:]*:|$)'
    match = re.search(pattern, content[start_pos:], re.IGNORECASE | re.DOTALL)
    if match:
        return clean_text(match.group(1))
    return ""

def parse_resource_block(content, start_pos, end_pos):
    """Parse a single resource block from the content"""
    block = content[start_pos:end_pos]
    
    # Extract organization name (usually the first line after the header)
    org_match = re.search(r'Organization:\s*([^\n]+)', block, re.IGNORECASE)
    if not org_match:
        return None
    
    organization = clean_text(org_match.group(1))
    
    # Extract other fields
    program_type = extract_field_value(block, "Program Type", 0)
    contact = extract_field_value(block, "Contact", 0)
    target_population = extract_field_value(block, "Target Population", 0)
    eligibility = extract_field_value(block, "Eligibility", 0)
    services = extract_field_value(block, "Services", 0)
    hours = extract_field_value(block, "Hours", 0)
    location = extract_field_value(block, "Location", 0)
    key_features = extract_field_value(block, "Key Features", 0)
    
    # Additional fields that might be present
    documentation = extract_field_value(block, "Documentation", 0)
    amenities = extract_field_value(block, "Amenities", 0)
    cost = extract_field_value(block, "Cost", 0)
    availability = extract_field_value(block, "Availability", 0)
    process = extract_field_value(block, "Process", 0)
    
    # Combine additional info into services if services is empty
    if not services:
        additional_info = []
        if amenities:
            additional_info.append(f"Amenities: {amenities}")
        if cost:
            additional_info.append(f"Cost: {cost}")
        if availability:
            additional_info.append(f"Availability: {availability}")
        if process:
            additional_info.append(f"Process: {process}")
        services = "; ".join(additional_info)
    
    # Determine category based on content
    block_lower = block.lower()
    if any(word in block_lower for word in ['food', 'meal', 'pantry', 'nutrition', 'feeding']):
        category = "food"
    elif any(word in block_lower for word in ['transport', 'ride', 'medical transport', 'mobility']):
        category = "transportation"
    else:
        category = "housing"  # Default to housing
    
    resource = {
        "category": category,
        "organization": organization,
        "program_type": program_type or "Housing Program",
        "contact": contact,
        "target_population": target_population,
        "age_group": "Not specified",
        "eligibility": eligibility,
        "immigration_status": "Not specified",
        "insurance_required": "No",
        "accepts_medicaid": "Not specified",
        "criminal_history": "Not specified",
        "ada_accessible": "Not specified",
        "advance_booking_required": "Not specified",
        "accepts_clients_without_id": "Not specified",
        "referral_method": "Not specified",
        "intake_hours": hours,
        "available_days": "Not specified",
        "area_of_service": "Houston area",
        "email": "Not listed",
        "website": "Not listed",
        "services": services,
        "key_features": key_features,
        "id": generate_resource_id(organization, program_type),
        "resource_name": organization
    }
    
    # Add documentation field if present
    if documentation:
        resource["documentation"] = documentation
    
    return resource

def parse_pdf_content(content):
    """Parse the entire PDF content and extract resources"""
    resources = []
    
    # Find all organization markers
    org_positions = []
    for match in re.finditer(r'Organization:\s*([^\n]+)', content, re.IGNORECASE):
        org_positions.append(match.start())
    
    # Parse each resource block
    for i, start_pos in enumerate(org_positions):
        end_pos = org_positions[i + 1] if i + 1 < len(org_positions) else len(content)
        
        resource = parse_resource_block(content, start_pos, end_pos)
        if resource:
            resources.append(resource)
    
    return resources

def main():
    # Read the new PDF content
    content_file = Path(__file__).parent / "new_pdf_content.txt"
    if not content_file.exists():
        print(f"Content file not found: {content_file}")
        return
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse resources from the content
    new_resources = parse_pdf_content(content)
    print(f"Parsed {len(new_resources)} resources from new PDF")
    
    # Load existing structured resources
    resources_file = Path(__file__).parent / "structured_resources.json"
    if resources_file.exists():
        with open(resources_file, 'r', encoding='utf-8') as f:
            existing_resources = json.load(f)
    else:
        existing_resources = []
    
    # Create a backup
    backup_file = Path(__file__).parent / "structured_resources_backup_before_new_pdf.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(existing_resources, f, indent=2)
    print(f"Backup created: {backup_file}")
    
    # Create a map of existing resources by organization + program_type
    existing_map = {}
    for resource in existing_resources:
        key = f"{resource.get('organization', '')}_{resource.get('program_type', '')}".lower()
        existing_map[key] = resource
    
    # Add or update resources
    updated_count = 0
    added_count = 0
    
    for new_resource in new_resources:
        key = f"{new_resource['organization']}_{new_resource['program_type']}".lower()
        
        if key in existing_map:
            # Update existing resource
            existing_resource = existing_map[key]
            for field, value in new_resource.items():
                if value and value != "Not specified" and value != "Not listed":
                    existing_resource[field] = value
            updated_count += 1
        else:
            # Add new resource
            existing_resources.append(new_resource)
            added_count += 1
    
    # Save updated resources
    with open(resources_file, 'w', encoding='utf-8') as f:
        json.dump(existing_resources, f, indent=2)
    
    print(f"Updated {updated_count} existing resources")
    print(f"Added {added_count} new resources")
    print(f"Total resources: {len(existing_resources)}")
    print(f"Resources saved to: {resources_file}")

if __name__ == "__main__":
    main() 