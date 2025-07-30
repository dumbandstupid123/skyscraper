import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# --- Configuration ---
load_dotenv()
SCRIPT_DIR = Path(__file__).parent.absolute()
RESOURCES_FILE = SCRIPT_DIR / 'structured_resources.json'
# --- End Configuration ---

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RAGResourceMatcher:
    def __init__(self):
        # 1. Initialize OpenAI and Embedding Models
        openai_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPEN_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY or OPEN_API_KEY environment variable is required.")
        
        # Set the OpenAI API key for the session
        os.environ["OPENAI_API_KEY"] = openai_key
        
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # 2. Load data, create documents, and build the in-memory vector store
        try:
            self._load_resources_and_build_vector_store()
            logging.info("RAG Resource Matcher initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize RAG Resource Matcher: {e}", exc_info=True)
            self.vector_store = None # Ensure it's None if initialization fails

    def _load_resources_and_build_vector_store(self):
        """Loads resource data from JSON and builds an in-memory Chroma vector store."""
        logging.info("Loading resources from JSON and building vector store...")
        
        # Load resources from JSON
        with open(RESOURCES_FILE, 'r') as f:
            resources = json.load(f)
        
        # Create documents from resources
        documents = []
        for resource in resources:
            # Create searchable text content
            content = f"""
            Resource: {resource.get('resource_name', 'Unknown')}
            Organization: {resource.get('organization', 'Unknown')}
            Category: {resource.get('category', 'Unknown')}
            Target Population: {resource.get('target_population', 'Unknown')}
            Services: {resource.get('services', 'Unknown')}
            Eligibility: {resource.get('eligibility', 'Unknown')}
            Location: {resource.get('location', 'Unknown')}
            Hours: {resource.get('hours', 'Unknown')}
            Contact: {resource.get('contact', 'Unknown')}
            Key Features: {resource.get('key_features', 'Unknown')}
            Age Group: {resource.get('age_group', 'Unknown')}
            Immigration Status: {resource.get('immigration_status', 'Unknown')}
            Accepts Clients Without ID: {resource.get('accepts_clients_without_id', 'Unknown')}
            Advance Booking Required: {resource.get('advance_booking_required', 'Unknown')}
            ADA Accessible: {resource.get('ada_accessible', 'Unknown')}
            """.strip()
            
            doc = Document(
                page_content=content,
                metadata=resource
            )
            documents.append(doc)
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Create the in-memory vector store using Chroma
        logging.info(f"Creating Chroma index from {len(split_docs)} document chunks...")
        self.vector_store = Chroma.from_documents(split_docs, self.embeddings)
        logging.info("In-memory vector store created successfully.")

    def get_recommendations(self, client_data: Dict[str, Any], resource_type: str) -> Dict[str, Any]:
        """
        Enhanced RAG workflow with category filtering for housing, food, and transportation:
        1. Build a query from client data.
        2. Retrieve relevant documents using vector similarity search.
        3. Filter results by resource category (housing/food/transportation).
        4. Use the LLM to generate a summary of the filtered documents.
        """
        if not self.vector_store:
            logging.error("RAG Resource Matcher not initialized. Cannot get recommendations.")
            return {
                "llm_summary": "Error: The resource matching system is not available.",
                "retrieved_recommendations": [],
                "client_question": ""
            }
            
        question = self._build_client_question(client_data, resource_type)

        # Retrieve more documents initially to allow for filtering
        retrieved_docs = self.vector_store.similarity_search(question, k=25)
        
        # Filter documents by category
        filtered_docs = self._filter_by_category(retrieved_docs, resource_type)
        
        # Take top 5 after filtering
        final_docs = filtered_docs[:5]
        
        # Prepare recommendations for the final output
        final_recommendations = [doc.metadata for doc in final_docs]

        # Generate the final summary using the LLM
        recommendation_reason = self._generate_llm_summary(question, final_docs, resource_type)
        
        return {
            "recommendation_reason": recommendation_reason,
            "retrieved_recommendations": final_recommendations,
            "client_question": question
        }

    def _filter_by_category(self, documents: List[Document], resource_type: str) -> List[Document]:
        """Filter documents by resource category with enhanced keyword matching."""
        if resource_type not in ['food', 'housing', 'transportation']:
            return documents
            
        filtered = []
        for doc in documents:
            # Primary filter: check if the document has category metadata
            if 'category' in doc.metadata:
                if doc.metadata['category'] == resource_type:
                    filtered.append(doc)
            else:
                # Fallback: check content for category indicators
                content = doc.page_content.lower()
                if resource_type == 'food':
                    food_keywords = ['food', 'meal', 'pantry', 'nutrition', 'grocery', 'hunger', 'feeding', 'csfp', 'snap', 'tefap']
                    if any(keyword in content for keyword in food_keywords):
                        filtered.append(doc)
                elif resource_type == 'housing':
                    housing_keywords = ['housing', 'shelter', 'bed', 'room', 'apartment', 'home', 'residence', 'accommodation', 'lodging']
                    if any(keyword in content for keyword in housing_keywords):
                        filtered.append(doc)
                elif resource_type == 'transportation':
                    transport_keywords = ['transportation', 'transport', 'ride', 'bus', 'taxi', 'medical transport', 'mobility', 'travel', 'transit']
                    if any(keyword in content for keyword in transport_keywords):
                        filtered.append(doc)
        
        return filtered

    def _build_client_question(self, client_data: Dict[str, Any], resource_type: str) -> str:
        """Builds a detailed question string from client data for vector search."""
        parts = [f"Find {resource_type} resources for a client."]
        
        # Extract age from dateOfBirth if available
        age = None
        if 'dateOfBirth' in client_data and client_data['dateOfBirth']:
            try:
                from datetime import datetime
                dob = datetime.strptime(client_data['dateOfBirth'], '%Y-%m-%d')
                age = (datetime.now() - dob).days // 365
            except (ValueError, TypeError):
                pass # Ignore if format is wrong

        if age:
            parts.append(f"The client's age is {age}.")
        if client_data.get('gender'):
            parts.append(f"Gender: {client_data['gender']}.")
        if client_data.get('family_status'):
            parts.append(f"Family status: {client_data['family_status']}.")
        if client_data.get('employment_status'):
            parts.append(f"Employment: {client_data['employment_status']}.")
        if client_data.get('income_level'):
            parts.append(f"Income level: ${client_data['income_level']}.")
        if client_data.get('is_veteran'):
            parts.append(f"Veteran status: {'Yes' if client_data['is_veteran'] else 'No'}.")
        if client_data.get('has_disability'):
            parts.append(f"Has disability: {'Yes' if client_data['has_disability'] else 'No'}.")
        
        # Add specific needs based on resource type
        if resource_type == 'food':
            parts.append("Looking for food assistance, meals, pantries, or nutrition programs.")
        elif resource_type == 'housing':
            parts.append("Looking for housing assistance, shelter, or accommodation.")
        elif resource_type == 'transportation':
            parts.append("Looking for transportation assistance, rides, or mobility services.")
        
        # Use the detailed notes for context
        if client_data.get('notes'):
            parts.append(f"Client background and needs: {client_data['notes']}")
        
        # Add needs array if available
        if client_data.get('needs') and isinstance(client_data['needs'], list):
            parts.append(f"Specific needs: {', '.join(client_data['needs'])}")
            
        return " ".join(parts)

    def _generate_llm_summary(self, question: str, documents: List[Document], resource_type: str) -> str:
        """Uses the LLM to generate a helpful summary of the top recommended resources."""
        if not documents:
            return f"No matching {resource_type} resources were found for this client."

        # Extract metadata and page content for the prompt
        context = "\n\n---\n\n".join([
            f"Resource: {doc.metadata.get('resource_name', 'N/A')}\n"
            f"Organization: {doc.metadata.get('organization', 'N/A')}\n"
            f"Contact: {doc.metadata.get('contact', 'N/A')}\n"
            f"Target Population: {doc.metadata.get('target_population', 'N/A')}\n"
            f"Details: {doc.page_content}"
            for doc in documents
        ])

        resource_type_context = {
            'food': "food assistance, meals, pantries, or nutrition programs",
            'housing': "housing assistance, shelter, or accommodation services",
            'transportation': "transportation assistance, rides, or mobility services"
        }

        prompt = PromptTemplate.from_template(
            "You are a helpful case manager assistant. Based on the client's need for {resource_type_desc} "
            "and the provided resources, write a single, personalized sentence explaining why these resources "
            "are being recommended for this client. Address the social worker/case manager, not the client directly. "
            "Focus on how these resources match the client's specific situation and needs.\n\n"
            "Client's Need: {question}\n\n"
            "Available {resource_type} Resources:\n{context}\n\n"
            "Recommendation for Social Worker:"
        )
        
        chain = prompt | self.llm
        response = chain.invoke({
            "question": question, 
            "context": context,
            "resource_type": resource_type,
            "resource_type_desc": resource_type_context.get(resource_type, f"{resource_type} services")
        })
        return response.content if hasattr(response, 'content') else str(response)

# Helper to calculate age, in case it's needed elsewhere
from datetime import datetime

def _calculate_age(birth_date_str: str) -> int:
    """Calculates age from a 'YYYY-MM-DD' string."""
    if not birth_date_str:
        return 0
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        return (datetime.now() - birth_date).days // 365
    except (ValueError, TypeError):
        return 0 