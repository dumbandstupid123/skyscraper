import PyPDF2
import json
import re
from typing import List, Dict

def extract_pdf_content(pdf_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def parse_resources(text: str) -> List[Dict]:
    """Parse resources from extracted PDF text"""
    resources = []
    
    # Define categories we're looking for
    categories = {
        'immigration': ['immigration', 'legal', 'attorney', 'lawyer', 'visa', 'citizenship'],
        'goods': ['clothing', 'goods', 'furniture', 'appliances', 'donations'],
        'utilities': ['utilities', 'electric', 'gas', 'water', 'internet', 'phone'],
        'mental_health': ['mental health', 'substance abuse', 'counseling', 'therapy', 'addiction']
    }
    
    # Split text into sections
    lines = text.split('\n')
    current_resource = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for resource names (usually in caps or bold)
        if re.match(r'^[A-Z\s&]+$', line) and len(line) > 5:
            if current_resource:
                resources.append(current_resource)
            current_resource = {
                'name': line.title(),
                'description': '',
                'phone': '',
                'email': '',
                'website': '',
                'address': '',
                'category': determine_category(line, categories),
                'eligibility': '',
                'services': []
            }
        
        # Extract contact information
        elif 'phone' in line.lower() or re.search(r'\(\d{3}\)', line):
            phone_match = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4}|\d{3}-\d{3}-\d{4})', line)
            if phone_match and current_resource:
                current_resource['phone'] = phone_match.group(1)
        
        elif '@' in line:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
            if email_match and current_resource:
                current_resource['email'] = email_match.group()
        
        elif 'www.' in line or 'http' in line:
            website_match = re.search(r'(www\.[\w\.-]+|https?://[\w\.-]+)', line)
            if website_match and current_resource:
                current_resource['website'] = website_match.group()
        
        # Address (contains street numbers)
        elif re.search(r'\d+\s+\w+', line) and current_resource:
            current_resource['address'] = line
        
        # Description or services
        elif current_resource and line:
            if not current_resource['description']:
                current_resource['description'] = line
            else:
                current_resource['services'].append(line)
    
    # Add the last resource
    if current_resource:
        resources.append(current_resource)
    
    return resources

def determine_category(resource_name: str, categories: Dict) -> str:
    """Determine resource category based on name and keywords"""
    resource_lower = resource_name.lower()
    
    for category, keywords in categories.items():
        if any(keyword in resource_lower for keyword in keywords):
            return category
    
    return 'other'

def main():
    pdf_path = "/Users/vijayramlochan/Downloads/pumpum.pdf"
    
    print("Extracting content from PDF...")
    text = extract_pdf_content(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    print("Parsing resources...")
    resources = parse_resources(text)
    
    print(f"Found {len(resources)} resources")
    
    # Save extracted resources
    with open('extracted_resources.json', 'w') as f:
        json.dump(resources, f, indent=2)
    
    # Also save raw text for manual review
    with open('raw_pdf_content.txt', 'w') as f:
        f.write(text)
    
    print("Resources saved to extracted_resources.json")
    print("Raw content saved to raw_pdf_content.txt")
    
    # Print summary
    categories = {}
    for resource in resources:
        cat = resource.get('category', 'other')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} resources")

if __name__ == "__main__":
    main() 