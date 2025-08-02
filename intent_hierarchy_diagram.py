#!/usr/bin/env python3
"""
Visual Representation of Insurance Intent Hierarchy
"""

def print_intent_hierarchy():
    """Print a visual representation of the intent hierarchy"""
    
    print("=" * 80)
    print("INSURANCE INTENT HIERARCHY")
    print("=" * 80)
    print()
    
    hierarchy = {
        "Premiums": {
            "description": "Payment-related topics",
            "sub_intents": [
                "grace period",
                "premium payment", 
                "additional premium payment",
                "renewal premium discount"
            ],
            "example_keywords": ["grace period", "premium", "payment", "additional premium"]
        },
        "Maternity": {
            "description": "Pregnancy and childbirth coverage",
            "sub_intents": [
                "maternity coverage",
                "pregnancy termination",
                "well mother care",
                "routine preventive care",
                "maternity hospitalization"
            ],
            "example_keywords": ["maternity expenses", "childbirth", "pregnancy", "caesarean"]
        },
        "Coverage": {
            "description": "What's covered by the policy",
            "sub_intents": [
                "inpatient treatment",
                "ambulance services",
                "ayush treatment",
                "trip cancellation coverage",
                "baggage loss coverage",
                "personal accident coverage",
                "air ambulance services",
                "well baby care",
                "new born baby expenses",
                "daily cash benefit",
                "pre/post-hospitalization expenses"
            ],
            "example_keywords": ["inpatient hospitalization", "sum insured", "medical expenses", "ambulance"]
        },
        "Exclusions": {
            "description": "What's not covered",
            "sub_intents": [
                "pre-existing disease",
                "waiting period",
                "cosmetic surgery",
                "substance abuse",
                "war and terrorism",
                "non-medical expenses"
            ],
            "example_keywords": ["pre-existing disease", "waiting period", "exclusion", "cosmetic surgery"]
        },
        "Claims": {
            "description": "How to file and process claims",
            "sub_intents": [
                "claim process",
                "cashless claims",
                "reimbursement process",
                "nominee payment"
            ],
            "example_keywords": ["notification of claim", "cashless facility", "reimbursement", "claim procedure"]
        }
    }
    
    for main_intent, data in hierarchy.items():
        print(f"📋 {main_intent}")
        print(f"   Description: {data['description']}")
        print(f"   Keywords: {', '.join(data['example_keywords'][:3])}...")
        print(f"   Sub-intents:")
        for sub_intent in data['sub_intents']:
            print(f"     • {sub_intent}")
        print()

def print_classification_flow():
    """Print the classification flow"""
    
    print("=" * 80)
    print("CLASSIFICATION FLOW")
    print("=" * 80)
    print()
    
    flow_steps = [
        ("1. Text Input", "Original insurance document text"),
        ("2. Chunking", "Split text into manageable chunks (by sentences/size)"),
        ("3. Keyword Matching", "Find matching keywords in each chunk"),
        ("4. Score Calculation", "Calculate weighted scores for each intent"),
        ("5. Main Intent Selection", "Select intent with highest score"),
        ("6. Sub-Intent Classification", "Determine specific sub-intent within main intent"),
        ("7. Metadata Generation", "Create rich metadata for the chunk")
    ]
    
    for step, description in flow_steps:
        print(f"{step:25} → {description}")
    
    print()

def print_metadata_structure():
    """Print the metadata structure"""
    
    print("=" * 80)
    print("CHUNK METADATA STRUCTURE")
    print("=" * 80)
    print()
    
    metadata_example = {
        "chunk_id": "chunk_1",
        "text": "The policyholder has a 30-day grace period for premium payment",
        "main_intent": "Premiums",
        "sub_intent": "grace period", 
        "confidence_score": 0.85,
        "keywords_found": ["grace period", "premium", "payment"],
        "chunk_type": "text",
        "domain": "insurance"
    }
    
    print("Each chunk gets the following metadata:")
    print()
    for key, value in metadata_example.items():
        if key == "text":
            print(f"  {key:20}: {str(value)[:50]}...")
        else:
            print(f"  {key:20}: {value}")
    
    print()

def print_usage_examples():
    """Print usage examples"""
    
    print("=" * 80)
    print("USAGE EXAMPLES")
    print("=" * 80)
    print()
    
    examples = [
        ("Document Organization", "Group chunks by main intent for better structure"),
        ("Search & Retrieval", "Find specific content by intent or sub-intent"),
        ("Content Analysis", "Understand document focus and coverage gaps"),
        ("Quality Assurance", "Identify low-confidence classifications for review"),
        ("Automated Routing", "Route content to appropriate teams/departments"),
        ("Summary Generation", "Create intent-based summaries of documents")
    ]
    
    for use_case, description in examples:
        print(f"🔍 {use_case}")
        print(f"   {description}")
        print()

if __name__ == "__main__":
    print_intent_hierarchy()
    print_classification_flow()
    print_metadata_structure()
    print_usage_examples()
    
    print("=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print()
    print("1. Main Intents provide broad categorization (5 main categories)")
    print("2. Sub-Intents provide specific topic identification (20+ sub-categories)")
    print("3. Keywords with weights determine classification accuracy")
    print("4. Confidence scores indicate classification certainty")
    print("5. Rich metadata enables powerful search and analysis capabilities")
    print("6. Hierarchical structure allows both broad and specific content organization")