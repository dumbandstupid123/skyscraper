import re
import json
from typing import List, Dict

def reconstruct_text(content):
    """Reconstruct readable text from word-per-line format"""
    lines = content.strip().split('\n')
    reconstructed = []
    current_sentence = []
    
    for line in lines:
        word = line.strip()
        if not word:
            if current_sentence:
                reconstructed.append(' '.join(current_sentence))
                current_sentence = []
            continue
            
        # Check if this looks like a field header
        if word.endswith(':') or (word in ['Organization', 'Program', 'Phone', 'Email', 'Website', 'Location', 'Address', 'Services', 'Hours', 'Target', 'Eligibility', 'Languages']):
            if current_sentence:
                reconstructed.append(' '.join(current_sentence))
                current_sentence = []
            current_sentence = [word]
        else:
            current_sentence.append(word)
    
    if current_sentence:
        reconstructed.append(' '.join(current_sentence))
    
    return '\n'.join(reconstructed)

def extract_resources_from_reconstructed_text():
    """Extract resources from the reconstructed text"""
    
    with open('post_housing_content.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Reconstructing text from word-per-line format...")
    reconstructed = reconstruct_text(content)
    
    # Save reconstructed text for debugging
    with open('reconstructed_content.txt', 'w', encoding='utf-8') as f:
        f.write(reconstructed)
    
    # Look for resource patterns
    resources = []
    
    # Split on common resource boundaries
    sections = re.split(r'(?=Organization Name:)|(?=Program Name:)', reconstructed)
    
    current_resource = {}
    resource_count = 0
    
    for section in sections:
        if not section.strip():
            continue
            
        lines = section.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Parse different fields
            if line.startswith('Organization Name:'):
                if current_resource and current_resource.get('name'):
                    resources.append(current_resource.copy())
                current_resource = {'name': line.replace('Organization Name:', '').strip()}
                resource_count += 1
                
            elif line.startswith('Program Name:'):
                current_resource['program_name'] = line.replace('Program Name:', '').strip()
                
            elif line.startswith('Phone Number:') or line.startswith('Phone:'):
                phone_text = line.replace('Phone Number:', '').replace('Phone:', '').strip()
                phone_match = re.search(r'(\d{3}[-.]?\d{3}[-.]?\d{4})', phone_text)
                if phone_match:
                    current_resource['phone'] = phone_match.group(1)
                    
            elif line.startswith('Email:'):
                email_text = line.replace('Email:', '').strip()
                email_match = re.search(r'([\w\.-]+@[\w\.-]+\.\w+)', email_text)
                if email_match:
                    current_resource['email'] = email_match.group(1)
                    
            elif line.startswith('Website:'):
                current_resource['website'] = line.replace('Website:', '').strip()
                
            elif line.startswith('Location:') or line.startswith('Address:'):
                current_resource['address'] = line.replace('Location:', '').replace('Address:', '').strip()
                
            elif line.startswith('Services:'):
                current_resource['services'] = line.replace('Services:', '').strip()
                
            elif line.startswith('Hours:'):
                current_resource['hours'] = line.replace('Hours:', '').strip()
                
            elif line.startswith('Target Population:'):
                current_resource['target_population'] = line.replace('Target Population:', '').strip()
                
            elif line.startswith('Eligibility:'):
                current_resource['eligibility'] = line.replace('Eligibility:', '').strip()
                
            elif line.startswith('Languages:'):
                current_resource['languages'] = line.replace('Languages:', '').strip()
    
    # Add the last resource
    if current_resource and current_resource.get('name'):
        resources.append(current_resource)
    
    # Determine categories for all resources
    for resource in resources:
        resource['category'] = determine_category(resource)
        
        # Fill in missing fields
        for field in ['program_name', 'phone', 'email', 'website', 'address', 'services', 'hours', 'target_population', 'eligibility', 'languages']:
            if field not in resource:
                resource[field] = ''
    
    print(f"Found {len(resources)} resources after reconstruction")
    
    # Save resources
    with open('reconstructed_resources.json', 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)
    
    # Category breakdown
    categories = {}
    for resource in resources:
        cat = resource.get('category', 'other')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    # Show first few resources
    print("\nFirst 5 resources:")
    for i, resource in enumerate(resources[:5]):
        print(f"{i+1}. {resource.get('name', 'No name')} ({resource.get('category', 'unknown')})")
    
    return resources

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
    resources = extract_resources_from_reconstructed_text()
    print(f"\n✅ Extracted {len(resources)} resources from PDF!")
    print("Saved to reconstructed_resources.json") 