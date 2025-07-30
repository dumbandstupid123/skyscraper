#!/usr/bin/env python3

import json
import re
import os
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_spaced_text(text):
    """Clean text that has extra spaces between words"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def generate_resource_id(organization, program_type):
    """Generate a unique resource ID"""
    base = f"{organization}_{program_type}".lower()
    base = re.sub(r'[^a-z0-9_]', '_', base)
    base = re.sub(r'_+', '_', base)
    return f"res_{base}"

def parse_resource_block_simple(block):
    """Parse a single resource block with simple, direct extraction"""
    
    # Extract organization name
    org_match = re.search(r'Organization\s+Name\s*:\s*(.*?)Program\s+Name\s*:', block, re.IGNORECASE | re.DOTALL)
    if not org_match:
        return None
    organization = clean_spaced_text(org_match.group(1))
    
    # Extract program name
    prog_match = re.search(r'Program\s+Name\s*:\s*(.*?)Phone\s+Number\s*:', block, re.IGNORECASE | re.DOTALL)
    program_type = clean_spaced_text(prog_match.group(1)) if prog_match else "Housing Program"
    
    # Extract contact information
    phone_match = re.search(r'Phone\s+Number\s*:\s*(.*?)Email\s*:', block, re.IGNORECASE | re.DOTALL)
    phone = clean_spaced_text(phone_match.group(1)) if phone_match else ""
    
    email_match = re.search(r'Email\s*:\s*(.*?)Website\s*:', block, re.IGNORECASE | re.DOTALL)
    email = clean_spaced_text(email_match.group(1)) if email_match else ""
    
    website_match = re.search(r'Website\s*:\s*(.*?)Location\s*:', block, re.IGNORECASE | re.DOTALL)
    website = clean_spaced_text(website_match.group(1)) if website_match else ""
    
    location_match = re.search(r'Location\s*:\s*(.*?)Program\s+Details', block, re.IGNORECASE | re.DOTALL)
    location = clean_spaced_text(location_match.group(1)) if location_match else "Houston area"
    
    # Build contact string
    contact_parts = []
    if phone:
        contact_parts.append(phone)
    if email:
        contact_parts.append(email)
    contact = ", ".join(contact_parts)
    
    # Extract program details
    intake_match = re.search(r'Intake\s+Hours\s*:\s*(.*?)Target\s+Population\s*:', block, re.IGNORECASE | re.DOTALL)
    intake_hours = clean_spaced_text(intake_match.group(1)) if intake_match else ""
    
    target_match = re.search(r'Target\s+Population\s*:\s*(.*?)Eligibility\s+Requirements', block, re.IGNORECASE | re.DOTALL)
    target_population = clean_spaced_text(target_match.group(1)) if target_match else ""
    
    # Extract eligibility requirements
    eligibility_match = re.search(r'Eligibility\s+Requirements(.*?)(?=Documentation|Resource\s+\d+|$)', block, re.IGNORECASE | re.DOTALL)
    eligibility_parts = []
    if eligibility_match:
        eligibility_text = eligibility_match.group(1)
        bullet_points = re.findall(r'●\s*([^●]+)', eligibility_text)
        for bullet in bullet_points:
            bullet_clean = clean_spaced_text(bullet)
            if bullet_clean:
                eligibility_parts.append(bullet_clean)
    
    eligibility = "; ".join(eligibility_parts)
    
    # Extract individual eligibility components
    age_group = ""
    immigration_status = ""
    insurance_req = ""
    criminal_history = ""
    
    for part in eligibility_parts:
        if "age group:" in part.lower():
            age_group = part.split(":", 1)[1].strip() if ":" in part else part
        elif "immigration status:" in part.lower():
            immigration_status = part.split(":", 1)[1].strip() if ":" in part else part
        elif "insurance requirements:" in part.lower():
            insurance_req = part.split(":", 1)[1].strip() if ":" in part else part
        elif "criminal history:" in part.lower():
            criminal_history = part.split(":", 1)[1].strip() if ":" in part else part
    
    # Extract documentation
    doc_match = re.search(r'Documentation\s+&\s+Admission(.*?)(?=Resource\s+\d+|$)', block, re.IGNORECASE | re.DOTALL)
    required_docs = ""
    id_requirements = ""
    
    if doc_match:
        doc_text = doc_match.group(1)
        req_docs_match = re.search(r'Required\s+Documents\s*:\s*(.*?)ID\s+Requirements\s*:', doc_text, re.IGNORECASE | re.DOTALL)
        if req_docs_match:
            required_docs = clean_spaced_text(req_docs_match.group(1))
        
        id_req_match = re.search(r'ID\s+Requirements\s*:\s*(.*?)(?=Resource\s+\d+|$)', doc_text, re.IGNORECASE | re.DOTALL)
        if id_req_match:
            id_requirements = clean_spaced_text(id_req_match.group(1))
    
    # Build services and key features
    services_parts = []
    key_features_parts = []
    
    if required_docs:
        key_features_parts.append(f"Required Documents: {required_docs}")
    if id_requirements:
        key_features_parts.append(f"ID Requirements: {id_requirements}")
    
    services = "; ".join(services_parts)
    key_features = "; ".join(key_features_parts)
    
    # Create resource
    resource = {
        "category": "housing",
        "organization": organization,
        "program_type": program_type,
        "contact": contact,
        "location": location,
        "hours": intake_hours,
        "target_population": target_population,
        "age_group": age_group or "Not specified",
        "eligibility": eligibility,
        "immigration_status": immigration_status or "Not specified",
        "insurance_required": insurance_req or "Not specified",
        "accepts_medicaid": "Not specified",
        "criminal_history": criminal_history or "Not specified",
        "ada_accessible": "Not specified",
        "advance_booking_required": "Not specified",
        "accepts_clients_without_id": "Yes" if id_requirements and "no" in id_requirements.lower() else "Not specified",
        "referral_method": "Not specified",
        "intake_hours": intake_hours,
        "available_days": "Not specified",
        "area_of_service": "Houston area",
        "email": email or "Not listed",
        "website": website or "Not listed",
        "services": services,
        "key_features": key_features,
        "id": generate_resource_id(organization, program_type),
        "resource_name": organization
    }
    
    return resource

def simple_algorithm_update():
    """Simple algorithm update that definitely works"""
    script_dir = Path(__file__).parent
    content_file = script_dir / "jairam_dindin_content.txt"
    resources_file = script_dir / "structured_resources.json"
    
    if not content_file.exists():
        print(f"Error: Content file not found: {content_file}")
        return
    
    # Read the PDF content
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all resource blocks
    resource_pattern = r'Resource\s+\d+\s*:'
    matches = list(re.finditer(resource_pattern, content, re.IGNORECASE | re.DOTALL))
    
    print(f"Found {len(matches)} resource matches")
    
    new_resources = []
    
    for i, match in enumerate(matches):
        start_pos = match.start()
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        block = content[start_pos:end_pos]
        resource = parse_resource_block_simple(block)
        
        if resource:
            new_resources.append(resource)
            print(f"Parsed: {resource['organization']} - {resource['program_type']}")
        else:
            print(f"Failed to parse resource {i+1}")
    
    print(f"\nParsed {len(new_resources)} resources from new PDF")
    
    if not new_resources:
        print("No resources were parsed successfully. Exiting.")
        return
    
    # Load the original backup
    backup_file = script_dir / "structured_resources_backup_before_algorithm_update_20250714_064111.json"
    if backup_file.exists():
        with open(backup_file, 'r', encoding='utf-8') as f:
            existing_resources = json.load(f)
        print(f"Restored from original backup: {len(existing_resources)} existing resources")
    else:
        existing_resources = []
    
    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_backup_file = script_dir / f"structured_resources_backup_before_simple_update_{timestamp}.json"
    with open(new_backup_file, 'w', encoding='utf-8') as f:
        json.dump(existing_resources, f, indent=2)
    print(f"New backup created: {new_backup_file}")
    
    # Create a map of existing resources
    existing_map = {}
    for resource in existing_resources:
        key = f"{resource.get('organization', '')}_{resource.get('program_type', '')}".lower()
        existing_map[key] = resource
    
    # Update or add resources
    updated_count = 0
    added_count = 0
    
    for new_resource in new_resources:
        key = f"{new_resource['organization']}_{new_resource['program_type']}".lower()
        
        if key in existing_map:
            # Update existing resource
            existing_resource = existing_map[key]
            for field, value in new_resource.items():
                if value and value not in ["Not specified", "Not listed", ""]:
                    existing_resource[field] = value
            updated_count += 1
        else:
            # Add new resource
            existing_resources.append(new_resource)
            added_count += 1
    
    # Save updated resources
    with open(resources_file, 'w', encoding='utf-8') as f:
        json.dump(existing_resources, f, indent=2)
    
    print(f"\nSimple algorithm update complete:")
    print(f"- Updated {updated_count} existing resources")
    print(f"- Added {added_count} new resources")
    print(f"- Total resources: {len(existing_resources)}")
    
    # Show sample new resources
    print("\nSample new resources:")
    for i, resource in enumerate(new_resources[:3]):
        print(f"\n{i+1}. {resource['organization']}")
        print(f"   Program: {resource['program_type']}")
        print(f"   Contact: {resource['contact']}")
        print(f"   Location: {resource['location']}")
    
    # Test RAG system
    print("\n" + "="*50)
    print("TESTING RAG SYSTEM")
    print("="*50)
    
    try:
        from rag_resource_matcher import RAGResourceMatcher
        rag_matcher = RAGResourceMatcher()
        
        client_data = {
            "firstName": "John",
            "lastName": "Doe",
            "notes": "Recently homeless, needs emergency shelter"
        }
        
        recommendations = rag_matcher.get_recommendations(client_data, "housing")
        print(f"✓ RAG system working - found {len(recommendations.get('retrieved_recommendations', []))} recommendations")
        
        # Show first recommendation
        if recommendations.get('retrieved_recommendations'):
            first_rec = recommendations['retrieved_recommendations'][0]
            print(f"✓ First recommendation: {first_rec.get('organization', 'Unknown')}")
            print(f"✓ AI reasoning: {recommendations.get('recommendation_reason', 'N/A')[:100]}...")
        
    except Exception as e:
        print(f"✗ RAG test failed: {e}")
    
    return existing_resources

if __name__ == "__main__":
    simple_algorithm_update() 