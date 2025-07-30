#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
import os

def test_imports():
    """Test all required imports"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import fastapi
        print("✅ fastapi imported successfully")
        
        import uvicorn
        print("✅ uvicorn imported successfully")
        
        # Test langchain imports
        import langchain
        print("✅ langchain imported successfully")
        
        import langchain_openai
        print("✅ langchain_openai imported successfully")
        
        # Test the problematic import
        from langchain_community.vectorstores import FAISS
        print("✅ langchain_community.vectorstores.FAISS imported successfully")
        
        # Test other imports
        import chromadb
        print("✅ chromadb imported successfully")
        
        import numpy
        print("✅ numpy imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 