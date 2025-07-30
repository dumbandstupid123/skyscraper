import json
import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AssistantFnc:
    def __init__(self):
        self.conversation_history = []
        self.current_client = None
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def lookup_client(self, client_id: str) -> dict:
        """Look up a client by their ID number."""
        clients_data = self.load_clients()
        for client in clients_data.get('clients', []):
            if str(client.get('id', '')) == client_id:
                self.current_client = client
                return client
        return {"error": "Client not found"}

    async def get_case_history(self) -> dict:
        """Get the case history for the current client."""
        if not self.current_client:
            return {"error": "No client selected"}
        return {
            "client": self.current_client,
            "history": self.conversation_history
        }

    async def get_available_resources(self) -> dict:
        """Get information about available resources and programs in Houston."""
        return self.load_resources()
    
    async def translate_text(self, text: str, target_language: str) -> dict:
        """Translate text to the specified language using OpenAI."""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are a professional translator. Translate the following text to {target_language}. Maintain the original meaning and tone. Only return the translated text, nothing else."
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            
            translated_text = response.choices[0].message.content.strip()
            return {
                "original": text,
                "translated": translated_text,
                "target_language": target_language,
                "success": True
            }
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return {
                "original": text,
                "translated": text,  # Return original if translation fails
                "target_language": target_language,
                "success": False,
                "error": str(e)
            }
    
    async def get_platform_features(self) -> dict:
        """Get comprehensive information about NextStep platform features."""
        return {
            "platform_name": "NextStep",
            "description": "AI-powered resource management system for social workers and case managers",
            "main_features": [
                "Resource Matcher - AI-powered tool that matches clients with appropriate resources",
                "Resource Center - Browse resources by category (Housing, Food, Transportation)", 
                "Client Management - Add, view, and manage client profiles",
                "Dashboard - Overview of activities and quick actions",
                "Voice Assistant - LiveKit-powered voice interactions",
                "Live Translation - Real-time translation support for multiple languages"
            ],
            "resource_categories": {
                "housing": "Emergency shelters, transitional housing, permanent supportive housing",
                "food": "Food pantries, meal programs, nutrition assistance, SNAP benefits", 
                "transportation": "Free rides, public transit, medical transportation, ADA services"
            },
            "workflow": [
                "1. Add clients with their basic information and needs",
                "2. Use Resource Matcher to find appropriate resources for specific clients",
                "3. Browse resources by category in the Resource Center", 
                "4. Track client progress and resource assignments"
            ],
            "total_resources": len(self.load_resources().get('resources', [])),
            "total_clients": len(self.load_clients().get('clients', []))
        }
    
    async def search_resources_by_category(self, category: str) -> dict:
        """Search resources by specific category."""
        resources_data = self.load_resources()
        filtered_resources = [
            resource for resource in resources_data.get('resources', [])
            if resource.get('category', '').lower() == category.lower()
        ]
        
        return {
            "category": category,
            "count": len(filtered_resources),
            "resources": filtered_resources[:10]  # Return first 10 for brevity
        }
    
    async def get_client_statistics(self) -> dict:
        """Get statistics about clients in the system."""
        clients_data = self.load_clients()
        clients = clients_data.get('clients', [])
        
        stats = {
            "total_clients": len(clients),
            "demographics": {},
            "needs_summary": {},
            "recent_additions": 0
        }
        
        # Analyze demographics and needs
        for client in clients:
            # Gender stats
            gender = client.get('gender', 'Unknown')
            stats["demographics"][gender] = stats["demographics"].get(gender, 0) + 1
            
            # Needs analysis
            needs = client.get('needs', [])
            for need in needs:
                stats["needs_summary"][need] = stats["needs_summary"].get(need, 0) + 1
        
        return stats

    def load_clients(self):
        """Load clients from JSON file."""
        try:
            if os.path.exists('clients.json'):
                with open('clients.json', 'r') as f:
                    return json.load(f)
            return {'clients': []}
        except Exception as e:
            logger.error(f"Error loading clients: {e}")
            return {'clients': []}

    def load_resources(self):
        """Load resources from JSON file."""
        try:
            if os.path.exists('structured_resources.json'):
                with open('structured_resources.json', 'r') as f:
                    resources_data = json.load(f)
                    # structured_resources.json is an array, not an object with "resources" key
                    if isinstance(resources_data, list):
                        return {"resources": resources_data}
                    return resources_data
            return {'resources': []}
        except Exception as e:
            logger.error(f"Error loading resources: {e}")
            return {'resources': []} 