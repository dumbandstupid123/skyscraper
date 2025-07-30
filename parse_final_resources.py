import json
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean text by joining words that are split across lines"""
    lines = text.split('\n')
    cleaned_lines = []
    current_line = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_line:
                cleaned_lines.append(current_line.strip())
                current_line = ""
            continue
        
        # If line ends with common punctuation or is a complete field, start new line
        if (line.endswith((':', '.', ',')) or 
            line.lower().startswith(('organization name:', 'program name:', 'phone number:', 
                                   'email:', 'website:', 'location:', 'program description:', 
                                   'target population:', 'services:', 'hours:', 'eligibility:',
                                   'languages:', 'walk-ins:', 'resource '))):
            if current_line:
                cleaned_lines.append(current_line.strip())
            current_line = line
        else:
            current_line += " " + line
    
    if current_line:
        cleaned_lines.append(current_line.strip())
    
    return '\n'.join(cleaned_lines)

def parse_resources_from_cleaned_text(text: str) -> List[Dict]:
    """Parse resources from cleaned text"""
    
    # Split by "Resource X:" patterns
    resource_sections = re.split(r'Resource\s+\d+:', text, flags=re.IGNORECASE)
    resources = []
    
    for section in resource_sections[1:]:  # Skip the header
        resource = parse_single_resource(section.strip())
        if resource and resource.get('name'):
            resources.append(resource)
    
    return resources

def parse_single_resource(section: str) -> Dict:
    """Parse a single resource section"""
    lines = [line.strip() for line in section.split('\n') if line.strip()]
    
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
        'services': [],
        'hours': '',
        'target_population': '',
        'languages': [],
        'walk_ins': '',
        'intake_hours': ''
    }
    
    for line in lines:
        line_lower = line.lower()
        
        # Extract information based on patterns
        if line_lower.startswith('organization name:'):
            resource['name'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('program name:'):
            resource['program_name'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('phone number:'):
            phone_text = line.split(':', 1)[1].strip()
            # Extract phone number
            phone_match = re.search(r'(\d{3}[-.]?\d{3}[-.]?\d{4})', phone_text)
            if phone_match:
                resource['phone'] = phone_match.group(1)
        elif line_lower.startswith('email:'):
            email_text = line.split(':', 1)[1].strip()
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', email_text)
            if email_match:
                resource['email'] = email_match.group()
        elif line_lower.startswith('website:'):
            resource['website'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('location:'):
            resource['address'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('program description:'):
            resource['description'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('target population:'):
            resource['target_population'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('services:'):
            services_text = line.split(':', 1)[1].strip()
            if services_text:
                resource['services'] = [s.strip() for s in services_text.split(',')]
        elif line_lower.startswith('hours:'):
            resource['hours'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('intake hours:'):
            resource['intake_hours'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('eligibility:'):
            resource['eligibility'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('languages:'):
            lang_text = line.split(':', 1)[1].strip()
            resource['languages'] = [lang.strip() for lang in lang_text.split(',')]
        elif line_lower.startswith('walk-ins:'):
            resource['walk_ins'] = line.split(':', 1)[1].strip()
    
    # Determine category
    resource['category'] = determine_category(resource)
    
    return resource

def determine_category(resource: Dict) -> str:
    """Determine category based on resource content"""
    text = f"{resource['name']} {resource['program_name']} {resource['description']} {' '.join(resource['services'])} {resource['target_population']}".lower()
    
    if any(keyword in text for keyword in ['immigration', 'legal', 'attorney', 'lawyer', 'visa', 'citizenship', 'deportation', 'asylum']):
        return 'immigration_legal'
    elif any(keyword in text for keyword in ['clothing', 'goods', 'furniture', 'appliances', 'donations', 'thrift', 'clothes']):
        return 'goods_clothing'
    elif any(keyword in text for keyword in ['utilities', 'electric', 'gas', 'water', 'internet', 'phone', 'utility', 'bill assistance']):
        return 'utilities'
    elif any(keyword in text for keyword in ['mental health', 'substance abuse', 'counseling', 'therapy', 'addiction', 'behavioral', 'psychiatric']):
        return 'mental_health_substance_abuse'
    elif any(keyword in text for keyword in ['housing', 'shelter', 'homeless', 'rent', 'apartment', 'transitional']):
        return 'housing'
    elif any(keyword in text for keyword in ['food', 'pantry', 'meal', 'nutrition', 'kitchen', 'hunger']):
        return 'food'
    else:
        return 'other'

def main():
    # Read the raw content
    with open('raw_pdf_content.txt', 'r') as f:
        text = f.read()
    
    print("Cleaning text format...")
    cleaned_text = clean_text(text)
    
    # Save cleaned text for review
    with open('cleaned_content.txt', 'w') as f:
        f.write(cleaned_text)
    
    print("Parsing resources...")
    resources = parse_resources_from_cleaned_text(cleaned_text)
    
    print(f"Found {len(resources)} resources")
    
    # Save final resources
    with open('final_resources.json', 'w') as f:
        json.dump(resources, f, indent=2)
    
    print("Final resources saved to final_resources.json")
    
    # Print category breakdown
    categories = {}
    for resource in resources:
        cat = resource.get('category', 'other')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} resources")
    
    # Print first few resources for verification
    print("\nFirst 5 resources:")
    for i, resource in enumerate(resources[:5]):
        print(f"\n{i+1}. {resource['name']}")
        print(f"   Program: {resource['program_name']}")
        print(f"   Category: {resource['category']}")
        print(f"   Phone: {resource['phone']}")
        print(f"   Email: {resource['email']}")

if __name__ == "__main__":
    main() 