#!/usr/bin/env python3
"""
Simple Example: How Intents and Sub-Intents Work in Chunks
"""

from insurance_intent_classifier import InsuranceIntentClassifier, INSURANCE_DOMAIN_CONFIG

def simple_example():
    """Simple example showing chunking and classification"""
    
    print("=== SIMPLE CHUNKING EXAMPLE ===\n")
    
    # Initialize classifier
    classifier = InsuranceIntentClassifier(INSURANCE_DOMAIN_CONFIG)
    
    # Simple text about premiums
    text = "The policyholder has a 30-day grace period for premium payment. Additional premium may be charged for high-risk activities."
    
    print("Original Text:")
    print(f'"{text}"\n')
    
    # Step 1: Chunk the text
    chunks = classifier.chunk_text(text, max_chunk_size=200)
    print(f"Step 1: Text chunked into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: {chunk}")
    print()
    
    # Step 2: Classify each chunk
    print("Step 2: Classifying each chunk:")
    for i, chunk in enumerate(chunks, 1):
        metadata = classifier.classify_chunk(chunk, f"chunk_{i}")
        
        print(f"\nChunk {i} Classification:")
        print(f"  Text: {metadata.text}")
        print(f"  Main Intent: {metadata.main_intent}")
        print(f"  Sub Intent: {metadata.sub_intent}")
        print(f"  Confidence: {metadata.confidence_score:.2f}")
        print(f"  Keywords Found: {metadata.keywords_found}")
    
    print("\n" + "="*60)
    
    # Example with multiple intents
    print("\n=== MULTIPLE INTENT EXAMPLE ===\n")
    
    mixed_text = """
    Premium Payment: The policyholder has a 30-day grace period for premium payment.
    Maternity Coverage: The policy covers maternity expenses including childbirth and caesarean delivery.
    Claims Process: Cashless facility is available at network hospitals for reimbursement claims.
    """
    
    print("Mixed Intent Text:")
    print(mixed_text)
    
    # Process the mixed text
    mixed_chunks = classifier.chunk_text(mixed_text, max_chunk_size=150)
    print(f"Chunked into {len(mixed_chunks)} chunks:\n")
    
    for i, chunk in enumerate(mixed_chunks, 1):
        metadata = classifier.classify_chunk(chunk, f"mixed_chunk_{i}")
        
        print(f"Chunk {i}:")
        print(f"  Text: {metadata.text.strip()}")
        print(f"  Main Intent: {metadata.main_intent}")
        print(f"  Sub Intent: {metadata.sub_intent}")
        print(f"  Confidence: {metadata.confidence_score:.2f}")
        print()

def explain_keyword_matching():
    """Explain how keyword matching works"""
    
    print("=== KEYWORD MATCHING EXPLANATION ===\n")
    
    classifier = InsuranceIntentClassifier(INSURANCE_DOMAIN_CONFIG)
    
    # Example text
    text = "The policyholder has a 30-day grace period for premium payment"
    
    print(f"Analyzing text: '{text}'\n")
    
    # Show keyword matching process
    text_lower = text.lower()
    
    print("Step 1: Looking for keywords in the text:")
    found_keywords = []
    
    for intent_name, intent_data in classifier.intents.items():
        print(f"\nChecking {intent_name} intent keywords:")
        intent_score = 0
        
        for keyword_info in intent_data["keywords"]:
            keyword = keyword_info["text"].lower()
            weight = keyword_info["weight"]
            
            if keyword in text_lower:
                print(f"  ✓ Found '{keyword}' (weight: {weight})")
                intent_score += weight
                found_keywords.append(keyword)
            else:
                print(f"  ✗ '{keyword}' not found")
        
        if intent_score > 0:
            print(f"  Total score for {intent_name}: {intent_score}")
    
    print(f"\nStep 2: Keywords found: {found_keywords}")
    
    # Classify the text
    metadata = classifier.classify_chunk(text)
    print(f"\nStep 3: Final classification:")
    print(f"  Main Intent: {metadata.main_intent}")
    print(f"  Sub Intent: {metadata.sub_intent}")
    print(f"  Confidence: {metadata.confidence_score:.2f}")

if __name__ == "__main__":
    simple_example()
    print("\n" + "="*80 + "\n")
    explain_keyword_matching()