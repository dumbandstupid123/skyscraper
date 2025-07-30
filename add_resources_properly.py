import json

def add_resources_to_structured_file():
    # Load existing resources
    with open('structured_resources.json', 'r') as f:
        existing_resources = json.load(f)
    
    print(f"Existing resources: {len(existing_resources)}")
    
    # Load new resources
    with open('new_resources.json', 'r') as f:
        new_resources = json.load(f)
    
    print(f"New resources to add: {len(new_resources)}")
    
    # Convert new resources to match existing format
    converted_resources = []
    for i, resource in enumerate(new_resources):
        converted = {
            'category': resource['category'],
            'organization': resource['name'],
            'program_type': resource['description'][:100] + '...' if len(resource['description']) > 100 else resource['description'],
            'contact': resource['phone'],
            'email': resource['email'],
            'website': resource['website'],
            'target_population': resource.get('target_population', 'General population'),
            'age_group': 'All ages',
            'eligibility': resource['eligibility'],
            'immigration_status': 'Not specified',
            'insurance_required': 'No',
            'accepts_medicaid': 'Not specified',
            'criminal_history': 'Not specified',
            'services': ', '.join(resource['services']) if isinstance(resource['services'], list) else resource['services'],
            'ada_accessible': 'Not specified',
            'escort_allowed': 'Not specified',
            'advance_booking_required': 'Call for details',
            'booking_method': 'Phone or walk-in',
            'documentation_required': 'Call for details',
            'accepts_clients_without_id': 'Call for details',
            'referral_method': 'Self-referral or professional referral',
            'intake_hours': resource['hours'],
            'available_days': resource['hours'],
            'area_of_service': 'Houston area',
            'location': resource['address'],
            'key_features': ', '.join(resource['services'][:3]) if isinstance(resource['services'], list) else resource['services'][:100],
            'id': f"res_{resource['category']}_{i+1000}",
            'resource_name': resource['name'],
            'languages': ', '.join(resource['languages']) if isinstance(resource['languages'], list) else resource['languages'],
            'walk_ins': resource['walk_ins']
        }
        converted_resources.append(converted)
        print(f"Added: {resource['name']} ({resource['category']})")
    
    # Add to existing resources
    all_resources = existing_resources + converted_resources
    
    # Save back to file
    with open('structured_resources.json', 'w') as f:
        json.dump(all_resources, f, indent=2)
    
    print(f"\n✅ Successfully added {len(converted_resources)} new resources!")
    print(f"✅ Total resources now: {len(all_resources)}")
    
    # Show breakdown by category
    categories = {}
    for resource in all_resources:
        cat = resource['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nResources by category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    add_resources_to_structured_file() 