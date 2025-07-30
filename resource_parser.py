import json
import re
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / 'resources.txt'
OUTPUT_FILE = SCRIPT_DIR / 'structured_resources.json'
# --- End Configuration ---

def parse_resource_block(block):
    """Parses a single block of text into a structured resource dictionary."""
    resource = {}
    current_key = None
    
    # Fields that should NOT have multi-line content appended
    single_line_fields = {'website', 'email', 'phone', 'contact', 'organization', 'program_type'}
    
    for line in block.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for key-value pairs (e.g., "Organization: Magnificat Houses Inc")
        match = re.match(r'([^:]+):\s*(.*)', line)
        if match:
            key, value = match.groups()
            # Convert key to camelCase for consistency (e.g., "Program Type" -> "programType")
            key_formatted = key.strip().replace(' ', '_').lower()
            current_key = key_formatted
            resource[current_key] = value.strip()
        elif current_key and current_key not in single_line_fields:
            # Only append multi-line content to fields that should support it
            # Skip if the line looks like it starts a new section or contains schedule info
            if not re.match(r'(Schedule Information|Intake Hours|Distribution Days)', line, re.IGNORECASE):
                resource[current_key] += ' ' + line
        elif current_key in single_line_fields:
            # For single-line fields, don't append additional content
            # This prevents schedule info from being added to website/email fields
            continue
            
    # Generate a unique ID based on the resource name
    if 'name' in resource:
        name_slug = re.sub(r'\s+', '-', resource['name'].lower().strip())
        resource['id'] = f"res_{name_slug}"
    else:
        # Fallback ID if name is missing
        resource['id'] = f"res_{hash(block)}"

    return resource

def main():
    """Main function to parse the text file and save as JSON."""
    logging.info(f"Starting resource parsing from: {INPUT_FILE}")
    
    if not INPUT_FILE.exists():
        logging.error(f"Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r') as f:
        content = f.read()

    # Split the content into blocks based on double newlines
    blocks = content.strip().split('\n\n')
    
    structured_resources = []
    for i, block in enumerate(blocks):
        if block.strip():
            logging.info(f"Parsing resource block {i+1}...")
            parsed = parse_resource_block(block)
            structured_resources.append(parsed)

    # Save the structured data to a JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(structured_resources, f, indent=2)
        
    logging.info(f"Successfully parsed {len(structured_resources)} resources.")
    logging.info(f"Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main() 