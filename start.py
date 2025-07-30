#!/usr/bin/env python3
"""
Railway startup script for NextStep backend
"""
import os
import sys
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if critical dependencies are importable"""
    try:
        import fastapi
        import uvicorn
        import langchain
        import langchain_core
        import langchain_openai
        import langchain_chroma
        import langchain_text_splitters
        import openai
        import chromadb
        import dotenv
        logger.info("All critical dependencies found")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return False

def check_environment():
    """Check if required environment variables are set"""
    # Load .env from the script's directory if it exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(script_dir, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        logger.info(f"Loaded environment variables from {dotenv_path}")

    # Check for OpenAI API key (either name)
    openai_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPEN_API_KEY")
    if not openai_key:
        logger.error("Missing OpenAI API key. Please set OPENAI_API_KEY or OPEN_API_KEY environment variable")
        return False
    
    # Set the standard name for consistency
    os.environ["OPENAI_API_KEY"] = openai_key
    
    logger.info("All required environment variables are set")
    return True

def main():
    """Main startup function"""
    logger.info("Starting NextStep backend...")
    
    # Check dependencies first
    if not check_dependencies():
        logger.error("Dependency check failed")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed")
        sys.exit(1)
    
    # Set port
    port = int(os.environ.get("PORT", 5001))
    logger.info(f"Starting server on port {port}")
    
    # Import and run the server
    try:
        from server import app
        import uvicorn
        
        # Start the server
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 