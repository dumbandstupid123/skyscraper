#!/usr/bin/env python3
"""
Script to extract content from the new PDF file
"""

import PyPDF2
import sys
from pathlib import Path

def extract_pdf_content(pdf_path):
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def main():
    pdf_path = "/Users/vijayramlochan/Downloads/rasika_dindin.pdf"
    
    if not Path(pdf_path).exists():
        print(f"PDF file not found: {pdf_path}")
        return
    
    content = extract_pdf_content(pdf_path)
    
    if content:
        # Save to text file for easier processing
        output_file = Path(__file__).parent / "new_pdf_content.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"New PDF content extracted and saved to: {output_file}")
        print(f"Content length: {len(content)} characters")
        
        # Show first 2000 characters
        print("\nFirst 2000 characters:")
        print(content[:2000])
    else:
        print("Failed to extract PDF content")

if __name__ == "__main__":
    main() 