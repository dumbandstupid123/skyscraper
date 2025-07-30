import re
import json

def extract_all_pdf_resources():
    """Extract all resources from the PDF content"""
    
    with open('post_housing_content.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    resources = []
    current_resource = {}
    i = 0
    
    print(f"Processing {len(lines)} lines...")
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for "Organization" followed by "Name:"
        if line == "Organization" and i + 2 < len(lines) and lines[i + 2] == "Name:":
            # Save previous resource if it exists
            if current_resource.get('name'):
                resources.append(current_resource.copy())
                print(f"Added resource: {current_resource['name']}")
            
            # Start new resource
            current_resource = {}
            i += 3  # Skip to the actual name
            
            # Collect organization name (may span multiple lines)
            name_parts = []
            while i < len(lines) and lines[i] and not (lines[i] == "Program" and i + 2 < len(lines) and lines[i + 2] == "Name:"):
                if lines[i] not in ["Organization", "Name:", "Program"]:
                    name_parts.append(lines[i])
                i += 1
            
            current_resource['name'] = ' '.join(name_parts)
            continue
        
        # Look for "Program" followed by "Name:"
        elif line == "Program" and i + 2 < len(lines) and lines[i + 2] == "Name:":
            i += 3  # Skip to the actual program name
            
            # Collect program name
            program_parts = []
            while i < len(lines) and lines[i] and lines[i] not in ["Phone", "Email", "Website", "Location", "Address", "Organization"]:
                if lines[i] not in ["Program", "Name:"]:
                    program_parts.append(lines[i])
                i += 1
            
            current_resource['program_name'] = ' '.join(program_parts)
            continue
        
        # Look for phone patterns
        elif line == "Phone" and i + 2 < len(lines) and lines[i + 2] == "Number:":
            i += 3
            phone_parts = []
            while i < len(lines) and lines[i] and not any(keyword in lines[i] for keyword in ["Email", "Website", "Location", "Organization", "Program"]):
                phone_parts.append(lines[i])
                i += 1
            
            phone_text = ' '.join(phone_parts)
            phone_match = re.search(r'(\d{3}[-.]?\d{3}[-.]?\d{4})', phone_text)
            if phone_match:
                current_resource['phone'] = phone_match.group(1)
            continue
        
        # Look for email
        elif line == "Email:":
            i += 1
            email_parts = []
            while i < len(lines) and lines[i] and not any(keyword in lines[i] for keyword in ["Website", "Location", "Organization", "Program"]):
                email_parts.append(lines[i])
                i += 1
            
            email_text = ' '.join(email_parts)
            email_match = re.search(r'([\w\.-]+@[\w\.-]+\.\w+)', email_text)
            if email_match:
                current_resource['email'] = email_match.group(1)
            continue
        
        # Look for website
        elif line == "Website:":
            i += 1
            website_parts = []
            while i < len(lines) and lines[i] and not any(keyword in lines[i] for keyword in ["Location", "Organization", "Program", "Address"]):
                website_parts.append(lines[i])
                i += 1
            
            current_resource['website'] = ' '.join(website_parts)
            continue
        
        # Look for location/address
        elif line in ["Location:", "Address:"]:
            i += 1
            location_parts = []
            count = 0
            while i < len(lines) and lines[i] and count < 10:  # Limit address to reasonable length
                if not any(keyword in lines[i] for keyword in ["Organization", "Program", "Phone", "Email", "Website"]):
                    location_parts.append(lines[i])
                    count += 1
                else:
                    break
                i += 1
            
            current_resource['address'] = ' '.join(location_parts)
            continue
        
        # Look for other fields
        elif line in ["Services:", "Hours:", "Target", "Eligibility:", "Languages:"]:
            field_name = line.replace(':', '').lower()
            if field_name == "target":
                # Handle "Target Population:"
                if i + 2 < len(lines) and lines[i + 2] == "Population:":
                    field_name = "target_population"
                    i += 3
                else:
                    i += 1
                    continue
            else:
                i += 1
            
            field_parts = []
            count = 0
            while i < len(lines) and lines[i] and count < 15:  # Reasonable field length
                if not any(keyword in lines[i] for keyword in ["Organization", "Program", "Phone", "Email", "Website", "Location", "Address", "Services", "Hours", "Target", "Eligibility", "Languages"]):
                    field_parts.append(lines[i])
                    count += 1
                else:
                    break
                i += 1
            
            current_resource[field_name] = ' '.join(field_parts)
            continue
        
        i += 1
    
    # Add the last resource
    if current_resource.get('name'):
        resources.append(current_resource)
        print(f"Added final resource: {current_resource['name']}")
    
    # Clean up and categorize resources
    cleaned_resources = []
    for resource in resources:
        # Fill in missing fields
        cleaned_resource = {
            'name': resource.get('name', ''),
            'program_name': resource.get('program_name', ''),
            'description': resource.get('program_name', ''),  # Use program name as description if no description
            'phone': resource.get('phone', ''),
            'email': resource.get('email', ''),
            'website': resource.get('website', ''),
            'address': resource.get('address', ''),
            'services': resource.get('services', ''),
            'hours': resource.get('hours', ''),
            'target_population': resource.get('target_population', ''),
            'eligibility': resource.get('eligibility', ''),
            'languages': resource.get('languages', ''),
            'category': determine_category(resource)
        }
        
        # Only include resources with at least a name
        if cleaned_resource['name'] and len(cleaned_resource['name']) > 2:
            cleaned_resources.append(cleaned_resource)
    
    print(f"\nExtracted {len(cleaned_resources)} valid resources")
    
    # Save resources
    with open('final_pdf_resources.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_resources, f, indent=2, ensure_ascii=False)
    
    # Category breakdown
    categories = {}
    for resource in cleaned_resources:
        cat = resource['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    # Show some examples
    print("\nFirst 10 resources:")
    for i, resource in enumerate(cleaned_resources[:10]):
        print(f"{i+1}. {resource['name']} ({resource['category']})")
    
    return cleaned_resources

def determine_category(resource_data):
    """Determine category based on resource content"""
    text = f"{resource_data.get('name', '')} {resource_data.get('program_name', '')} {resource_data.get('services', '')}".lower()
    
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

if __name__ == "__main__":
    resources = extract_all_pdf_resources()
    print(f"\n✅ Successfully extracted {len(resources)} resources from your PDF!")
    print("Saved to final_pdf_resources.json") 