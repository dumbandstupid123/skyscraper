import re
import json
from typing import List, Dict

def clean_and_join_text(text_lines):
    """Clean and join text that's split across multiple lines"""
    return ' '.join(line.strip() for line in text_lines if line.strip())

def extract_field_value(text, field_name):
    """Extract value for a specific field"""
    pattern = rf'{field_name}:\s*(.+?)(?=\n[A-Z][a-z]*:|$)'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return clean_and_join_text(match.group(1).split('\n'))
    return ''

def determine_category(resource_data):
    """Determine category based on resource content"""
    text = f"{resource_data.get('name', '')} {resource_data.get('description', '')} {resource_data.get('services', '')}".lower()
    
    if any(keyword in text for keyword in ['food', 'pantry', 'meal', 'nutrition', 'kitchen', 'hunger', 'grocery']):
        return 'food'
    elif any(keyword in text for keyword in ['housing', 'shelter', 'homeless', 'rent', 'apartment', 'transitional']):
        return 'housing'
    elif any(keyword in text for keyword in ['immigration', 'legal', 'attorney', 'lawyer', 'visa', 'citizenship', 'deportation', 'asylum']):
        return 'immigration_legal'
    elif any(keyword in text for keyword in ['clothing', 'goods', 'furniture', 'appliances', 'donations', 'thrift', 'clothes']):
        return 'goods_clothing'
    elif any(keyword in text for keyword in ['utilities', 'electric', 'gas', 'water', 'internet', 'phone', 'utility', 'bill assistance']):
        return 'utilities'
    elif any(keyword in text for keyword in ['mental health', 'substance abuse', 'counseling', 'therapy', 'addiction', 'behavioral', 'psychiatric']):
        return 'mental_health_substance_abuse'
    elif any(keyword in text for keyword in ['transportation', 'transport', 'bus', 'ride', 'metro']):
        return 'transportation'
    elif any(keyword in text for keyword in ['health', 'medical', 'clinic', 'hospital', 'healthcare']):
        return 'healthcare'
    elif any(keyword in text for keyword in ['education', 'school', 'training', 'job', 'employment']):
        return 'education_employment'
    else:
        return 'other'

def parse_single_resource(resource_text):
    """Parse a single resource from text block"""
    lines = [line.strip() for line in resource_text.split('\n') if line.strip()]
    
    resource = {
        'name': '',
        'program_name': '',
        'description': '',
        'phone': '',
        'email': '',
        'website': '',
        'address': '',
        'category': '',
        'eligibility': '',
        'services': '',
        'hours': '',
        'target_population': '',
        'languages': '',
        'walk_ins': '',
        'intake_hours': '',
        'location': ''
    }
    
    # Extract basic info
    resource['name'] = extract_field_value(resource_text, 'Organization Name')
    resource['program_name'] = extract_field_value(resource_text, 'Program Name')
    resource['description'] = extract_field_value(resource_text, 'Program Description') or extract_field_value(resource_text, 'Description')
    resource['eligibility'] = extract_field_value(resource_text, 'Eligibility')
    resource['services'] = extract_field_value(resource_text, 'Services')
    resource['target_population'] = extract_field_value(resource_text, 'Target Population')
    resource['hours'] = extract_field_value(resource_text, 'Hours') or extract_field_value(resource_text, 'Intake Hours')
    resource['languages'] = extract_field_value(resource_text, 'Languages')
    resource['walk_ins'] = extract_field_value(resource_text, 'Walk-ins')
    
    # Extract contact info
    phone_match = re.search(r'Phone.*?:?\s*(\d{3}[-.]?\d{3}[-.]?\d{4})', resource_text, re.IGNORECASE)
    if phone_match:
        resource['phone'] = phone_match.group(1)
    
    email_match = re.search(r'Email.*?:?\s*([\w\.-]+@[\w\.-]+\.\w+)', resource_text, re.IGNORECASE)
    if email_match:
        resource['email'] = email_match.group(1)
    
    website_match = re.search(r'Website.*?:?\s*(https?://[\w\.-]+|www\.[\w\.-]+)', resource_text, re.IGNORECASE)
    if website_match:
        resource['website'] = website_match.group(1)
    
    # Extract address/location
    location_match = re.search(r'(?:Location|Address).*?:?\s*(.+?)(?=\n|$)', resource_text, re.IGNORECASE)
    if location_match:
        resource['address'] = clean_and_join_text(location_match.group(1).split('\n')[:3])
    
    # Determine category
    resource['category'] = determine_category(resource)
    
    # Clean up empty values
    for key, value in resource.items():
        if isinstance(value, str):
            resource[key] = value.strip()
    
    return resource if resource['name'] else None

def parse_all_resources():
    """Parse all resources from the post-housing content"""
    
    with open('post_housing_content.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by resource markers
    resource_sections = re.split(r'Resource\s+\d+:', content, flags=re.IGNORECASE)
    
    resources = []
    skipped = 0
    
    print(f"Found {len(resource_sections)} sections to process...")
    
    for i, section in enumerate(resource_sections[1:], 1):  # Skip first empty section
        if len(section.strip()) < 50:  # Skip very short sections
            skipped += 1
            continue
            
        resource = parse_single_resource(section)
        if resource and resource['name']:
            resources.append(resource)
            print(f"Parsed {i}: {resource['name']} ({resource['category']})")
        else:
            skipped += 1
            print(f"Skipped section {i} (no name found)")
    
    print(f"\nParsed {len(resources)} resources, skipped {skipped}")
    
    # Save all resources
    with open('all_pdf_resources.json', 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)
    
    # Category breakdown
    categories = {}
    for resource in resources:
        cat = resource['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    return resources

if __name__ == "__main__":
    resources = parse_all_resources()
    print(f"\n✅ Extracted {len(resources)} resources from PDF!")
    print("Saved to all_pdf_resources.json") 