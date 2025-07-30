import json

def create_immigration_legal_resources():
    """Create immigration/legal resources based on the PDF content"""
    return [
        {
            "id": "immigration_1",
            "name": "KIND (Kids in Need of Defense)",
            "description": "Legal services for unaccompanied immigrant children",
            "phone": "713-574-9800",
            "email": "infohouston@supportkind.org",
            "website": "https://supportkind.org",
            "address": "Houston, TX",
            "category": "immigration_legal",
            "eligibility": "Unaccompanied immigrant children",
            "services": ["Legal representation", "Immigration assistance", "Child advocacy"],
            "hours": "Monday-Friday 9AM-5PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "By appointment only"
        },
        {
            "id": "immigration_2", 
            "name": "Catholic Charities Immigration Services",
            "description": "Comprehensive immigration legal services including asylum, family reunification, and citizenship",
            "phone": "713-874-6624",
            "email": "immigration@ccschouston.org",
            "website": "https://ccschouston.org/services/immigration/",
            "address": "2900 Louisiana St, Houston, TX 77006",
            "category": "immigration_legal",
            "eligibility": "Low-income immigrants",
            "services": ["Asylum cases", "Family reunification", "Citizenship applications", "DACA renewals"],
            "hours": "Monday-Friday 8:30AM-4:30PM",
            "languages": ["English", "Spanish", "Vietnamese"],
            "walk_ins": "Yes, limited hours"
        },
        {
            "id": "immigration_3",
            "name": "Houston Immigration Legal Services Collaborative",
            "description": "Pro bono legal services for immigrants",
            "phone": "713-782-3100",
            "email": "info@hilsc.org",
            "website": "https://hilsc.org",
            "address": "1900 Kane St, Houston, TX 77007",
            "category": "immigration_legal",
            "eligibility": "Low-income immigrants in removal proceedings",
            "services": ["Deportation defense", "Asylum representation", "Legal clinics"],
            "hours": "Monday-Friday 9AM-5PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Legal clinics on Saturdays"
        }
    ]

def create_goods_clothing_resources():
    """Create goods/clothing resources"""
    return [
        {
            "id": "goods_1",
            "name": "Good Shepherd Mission",
            "description": "Free clothing, household items, and emergency assistance",
            "phone": "713-691-0371",
            "email": "info@goodshepherdmission.org",
            "website": "https://www.goodshepherdmission.org/food-clothing.html",
            "address": "308 Hutchins St, Houston, TX 77003",
            "category": "goods_clothing",
            "eligibility": "Low-income individuals and families",
            "services": ["Free clothing", "Household items", "Emergency assistance"],
            "hours": "Monday-Friday 8AM-4PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Yes"
        },
        {
            "id": "goods_2",
            "name": "Catholic Charities Clothing Pantry",
            "description": "Free clothing for adults and children",
            "phone": "713-874-6664",
            "email": "clothing@ccschouston.org", 
            "website": "https://ccschouston.org/services/food-pantry-clothing/",
            "address": "2900 Louisiana St, Houston, TX 77006",
            "category": "goods_clothing",
            "eligibility": "Low-income families",
            "services": ["Adult clothing", "Children's clothing", "Shoes", "Accessories"],
            "hours": "Tuesday & Thursday 9AM-12PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Yes"
        },
        {
            "id": "goods_3",
            "name": "Salvation Army Family Store",
            "description": "Thrift store with low-cost clothing and household items",
            "phone": "713-752-0677",
            "email": "info@salvationarmyhouston.org",
            "website": "https://salvationarmyhouston.org",
            "address": "Multiple locations in Houston",
            "category": "goods_clothing",
            "eligibility": "Open to everyone",
            "services": ["Discounted clothing", "Furniture", "Appliances", "Household goods"],
            "hours": "Monday-Saturday 9AM-7PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Yes"
        }
    ]

def create_utilities_resources():
    """Create utilities assistance resources"""
    return [
        {
            "id": "utilities_1",
            "name": "CenterPoint Energy Customer Assistance Program",
            "description": "Utility bill assistance for low-income households",
            "phone": "713-659-2111",
            "email": "customercare@centerpointenergy.com",
            "website": "https://www.centerpointenergy.com/en-us/residential/customer-service/financial-assistance",
            "address": "Houston, TX",
            "category": "utilities",
            "eligibility": "Low-income households at risk of disconnection",
            "services": ["Gas bill assistance", "Payment plans", "Weatherization"],
            "hours": "Monday-Friday 7AM-7PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "No, call first"
        },
        {
            "id": "utilities_2",
            "name": "Reliant Energy LITE-UP Program",
            "description": "Electric bill assistance and energy efficiency programs",
            "phone": "1-866-222-7100",
            "email": "customercare@reliant.com",
            "website": "https://www.reliant.com/en/public-power/lite-up-texas.jsp",
            "address": "Houston, TX",
            "category": "utilities",
            "eligibility": "Income-qualified households",
            "services": ["Electric bill assistance", "Free energy-efficient appliances", "Weatherization"],
            "hours": "24/7 phone support",
            "languages": ["English", "Spanish"],
            "walk_ins": "Online applications available"
        },
        {
            "id": "utilities_3",
            "name": "Harris County Community Services",
            "description": "Comprehensive utility assistance programs",
            "phone": "713-274-3100",
            "email": "communityservices@hctx.net",
            "website": "https://csd.harriscountytx.gov/Pages/Utility-Assistance.aspx",
            "address": "8410 Lantern Point Dr, Houston, TX 77054",
            "category": "utilities",
            "eligibility": "Harris County residents with income below 150% FPL",
            "services": ["Electric bill assistance", "Gas bill assistance", "Water bill assistance"],
            "hours": "Monday-Friday 8AM-5PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "By appointment"
        }
    ]

def create_mental_health_resources():
    """Create mental health/substance abuse resources"""
    return [
        {
            "id": "mental_health_1",
            "name": "Harris Center for Mental Health",
            "description": "Comprehensive mental health and substance abuse services",
            "phone": "713-970-7000",
            "email": "info@harriscenter.org",
            "website": "https://www.harriscenter.org",
            "address": "2525 Holly Hall St, Houston, TX 77054",
            "category": "mental_health_substance_abuse",
            "eligibility": "Harris County residents, sliding fee scale available",
            "services": ["Mental health counseling", "Substance abuse treatment", "Crisis intervention", "Psychiatric services"],
            "hours": "24/7 crisis line, regular hours Monday-Friday 8AM-5PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Crisis services available 24/7"
        },
        {
            "id": "mental_health_2",
            "name": "Memorial Hermann Prevention & Recovery Center",
            "description": "Addiction treatment and mental health services",
            "phone": "713-242-3200",
            "email": "parc@memorialhermann.org",
            "website": "https://www.memorialhermann.org/services/specialties/behavioral-health/addiction-treatment",
            "address": "3043 Gessner Rd, Houston, TX 77080",
            "category": "mental_health_substance_abuse",
            "eligibility": "All ages, insurance and self-pay accepted",
            "services": ["Inpatient detox", "Outpatient counseling", "Group therapy", "Family counseling"],
            "hours": "24/7 admissions, outpatient Monday-Friday 8AM-8PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Emergency admissions 24/7"
        },
        {
            "id": "mental_health_3",
            "name": "Coalition for the Homeless - Mental Health Services",
            "description": "Mental health services for homeless individuals",
            "phone": "713-739-7514",
            "email": "info@cfth.org",
            "website": "https://www.cfth.org/services/mental-health",
            "address": "2000 Crawford St, Houston, TX 77002",
            "category": "mental_health_substance_abuse",
            "eligibility": "Homeless individuals and those at risk of homelessness",
            "services": ["Case management", "Mental health counseling", "Substance abuse counseling", "Housing assistance"],
            "hours": "Monday-Friday 8AM-5PM",
            "languages": ["English", "Spanish"],
            "walk_ins": "Yes, during business hours"
        }
    ]

def main():
    """Combine all resources and save to JSON"""
    
    all_resources = []
    
    # Add all category resources
    all_resources.extend(create_immigration_legal_resources())
    all_resources.extend(create_goods_clothing_resources())
    all_resources.extend(create_utilities_resources())
    all_resources.extend(create_mental_health_resources())
    
    # Save to JSON file
    with open('new_resources.json', 'w') as f:
        json.dump(all_resources, f, indent=2)
    
    print(f"Created {len(all_resources)} new resources")
    
    # Print category breakdown
    categories = {}
    for resource in all_resources:
        cat = resource['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} resources")
    
    print("\nResources saved to new_resources.json")
    print("Ready to add to database!")

if __name__ == "__main__":
    main() 