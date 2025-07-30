import json
import re
from typing import List, Dict

def parse_resources_from_text(text: str) -> List[Dict]:
    """Parse resources from the extracted PDF text with improved logic"""
    
    # Split by "Resource" markers
    resource_sections = re.split(r'Resource\s+\d+:', text)
    resources = []
    
    for section in resource_sections[1:]:  # Skip the first empty split
        resource = parse_single_resource(section)
        if resource:
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
        'walk_ins': ''
    }
    
    current_field = None
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Identify field headers
        if line_lower.startswith('organization name:'):
            resource['name'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('program name:'):
            resource['program_name'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('phone number:') or line_lower.startswith('phone:'):
            phone_text = line.split(':', 1)[1].strip()
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
        elif line_lower.startswith('location:') or line_lower.startswith('address:'):
            resource['address'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('program description:') or line_lower.startswith('description:'):
            current_field = 'description'
            desc_text = line.split(':', 1)[1].strip()
            if desc_text:
                resource['description'] = desc_text
        elif line_lower.startswith('eligibility:'):
            current_field = 'eligibility'
            elig_text = line.split(':', 1)[1].strip()
            if elig_text:
                resource['eligibility'] = elig_text
        elif line_lower.startswith('services:'):
            current_field = 'services'
            services_text = line.split(':', 1)[1].strip()
            if services_text:
                resource['services'].append(services_text)
        elif line_lower.startswith('hours:'):
            resource['hours'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('target population:'):
            resource['target_population'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('languages:'):
            lang_text = line.split(':', 1)[1].strip()
            resource['languages'] = [lang.strip() for lang in lang_text.split(',')]
        elif line_lower.startswith('walk-ins:'):
            resource['walk_ins'] = line.split(':', 1)[1].strip()
        elif current_field and line and not ':' in line:
            # Continue previous field
            if current_field == 'description':
                resource['description'] += ' ' + line
            elif current_field == 'eligibility':
                resource['eligibility'] += ' ' + line
            elif current_field == 'services':
                resource['services'].append(line)
        else:
            current_field = None
    
    # Determine category based on content
    resource['category'] = determine_category(resource)
    
    # Clean up
    resource['description'] = resource['description'].strip()
    resource['eligibility'] = resource['eligibility'].strip()
    
    return resource if resource['name'] else None

def determine_category(resource: Dict) -> str:
    """Determine category based on resource content"""
    text = f"{resource['name']} {resource['program_name']} {resource['description']} {' '.join(resource['services'])}".lower()
    
    if any(keyword in text for keyword in ['immigration', 'legal', 'attorney', 'lawyer', 'visa', 'citizenship', 'deportation']):
        return 'immigration_legal'
    elif any(keyword in text for keyword in ['clothing', 'goods', 'furniture', 'appliances', 'donations', 'thrift']):
        return 'goods_clothing'
    elif any(keyword in text for keyword in ['utilities', 'electric', 'gas', 'water', 'internet', 'phone', 'utility']):
        return 'utilities'
    elif any(keyword in text for keyword in ['mental health', 'substance abuse', 'counseling', 'therapy', 'addiction', 'behavioral']):
        return 'mental_health_substance_abuse'
    elif any(keyword in text for keyword in ['housing', 'shelter', 'homeless', 'rent', 'apartment']):
        return 'housing'
    elif any(keyword in text for keyword in ['food', 'pantry', 'meal', 'nutrition']):
        return 'food'
    else:
        return 'other'

def main():
    # Read the raw content
    with open('raw_pdf_content.txt', 'r') as f:
        text = f.read()
    
    print("Parsing resources with improved logic...")
    resources = parse_resources_from_text(text)
    
    print(f"Found {len(resources)} resources")
    
    # Save improved resources
    with open('improved_resources.json', 'w') as f:
        json.dump(resources, f, indent=2)
    
    print("Improved resources saved to improved_resources.json")
    
    # Print category breakdown
    categories = {}
    for resource in resources:
        cat = resource.get('category', 'other')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} resources")
    
    # Print first few resources for verification
    print("\nFirst 3 resources:")
    for i, resource in enumerate(resources[:3]):
        print(f"\n{i+1}. {resource['name']}")
        print(f"   Category: {resource['category']}")
        print(f"   Phone: {resource['phone']}")
        print(f"   Description: {resource['description'][:100]}...")

if __name__ == "__main__":
    main() 