import json
import sqlite3
from datetime import datetime

def create_resources_table_if_not_exists(cursor):
    """Create resources table if it doesn't exist"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            phone TEXT,
            email TEXT,
            website TEXT,
            address TEXT,
            category TEXT,
            eligibility TEXT,
            services TEXT,
            hours TEXT,
            languages TEXT,
            walk_ins TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def add_resources_to_database():
    """Add new resources to the SQLite database"""
    
    # Read the new resources
    with open('new_resources.json', 'r') as f:
        resources = json.load(f)
    
    # Connect to database
    conn = sqlite3.connect('social_worker_app.db')
    cursor = conn.cursor()
    
    # Create table if needed
    create_resources_table_if_not_exists(cursor)
    
    # Add each resource
    added_count = 0
    for resource in resources:
        try:
            cursor.execute('''
                INSERT INTO resources 
                (name, description, phone, email, website, address, category, 
                 eligibility, services, hours, languages, walk_ins)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                resource['name'],
                resource['description'],
                resource['phone'],
                resource['email'],
                resource['website'],
                resource['address'],
                resource['category'],
                resource['eligibility'],
                ', '.join(resource['services']) if isinstance(resource['services'], list) else resource['services'],
                resource['hours'],
                ', '.join(resource['languages']) if isinstance(resource['languages'], list) else resource['languages'],
                resource['walk_ins']
            ))
            added_count += 1
            print(f"Added: {resource['name']} ({resource['category']})")
        except Exception as e:
            print(f"Error adding {resource['name']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\nSuccessfully added {added_count} resources to the database!")
    return added_count

def update_resource_categories():
    """Update the resource categories in the frontend"""
    
    # Categories for the frontend
    categories = {
        'immigration_legal': {
            'name': 'Immigration & Legal',
            'description': 'Legal services, immigration assistance, and advocacy',
            'icon': 'fas fa-balance-scale'
        },
        'goods_clothing': {
            'name': 'Goods & Clothing',
            'description': 'Free clothing, household items, and material assistance',
            'icon': 'fas fa-tshirt'
        },
        'utilities': {
            'name': 'Utilities',
            'description': 'Assistance with electric, gas, water, and internet bills',
            'icon': 'fas fa-bolt'
        },
        'mental_health_substance_abuse': {
            'name': 'Mental Health & Substance Abuse',
            'description': 'Counseling, therapy, addiction treatment, and mental health services',
            'icon': 'fas fa-brain'
        },
        'housing': {
            'name': 'Housing',
            'description': 'Emergency shelter, transitional housing, and permanent housing assistance',
            'icon': 'fas fa-home'
        },
        'food': {
            'name': 'Food',
            'description': 'Food pantries, meal programs, and nutrition assistance',
            'icon': 'fas fa-utensils'
        }
    }
    
    # Save categories for frontend use
    with open('resource_categories.json', 'w') as f:
        json.dump(categories, f, indent=2)
    
    print("Updated resource categories for frontend")

def main():
    print("Adding new resources from PDF document...")
    print("Categories: Immigration/Legal, Goods/Clothing, Utilities, Mental Health/Substance Abuse")
    print("-" * 80)
    
    # Add resources to database
    added_count = add_resources_to_database()
    
    # Update categories
    update_resource_categories()
    
    print("-" * 80)
    print(f"✅ Successfully added {added_count} new resources!")
    print("✅ Updated resource categories")
    print("\nNew resources are now available in:")
    print("  - Resource Center (Browse Resources)")
    print("  - Resource Matcher")
    print("  - All resource-related features")
    
    print("\nNext steps:")
    print("  1. Restart your backend server")
    print("  2. New categories will appear in the resource browser")
    print("  3. Resource matcher will include new resources in matching")

if __name__ == "__main__":
    main() 