import json
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict

# Your insurance domain configuration
INSURANCE_DOMAIN_CONFIG = {
  "domain": "insurance",
  "intents": {
    "Premiums": {
      "keywords": [
        {"text": "grace period", "weight": 2.0},
        {"text": "premium", "weight": 1.5},
        {"text": "payment", "weight": 1.0},
        {"text": "additional premium", "weight": 1.5},
        {"text": "renewal premium", "weight": 1.8},
        {"text": "installment premium", "weight": 1.5},
        {"text": "risk loading", "weight": 1.5}
      ],
      "sub_intents": [
        "grace period",
        "premium payment",
        "additional premium payment",
        "renewal premium discount"
      ],
      "weight": 1.0
    },
    "Maternity": {
      "keywords": [
        {"text": "maternity expenses", "weight": 2.0},
        {"text": "childbirth", "weight": 2.0},
        {"text": "pregnancy", "weight": 2.0},
        {"text": "caesarean", "weight": 1.5},
        {"text": "well mother care", "weight": 2.0},
        {"text": "routine preventive care", "weight": 1.5},
        {"text": "immunizations", "weight": 1.5},
        {"text": "maternity hospitalization", "weight": 2.0},
        {"text": "ectopic pregnancy", "weight": 1.5},
        {"text": "miscarriage", "weight": 1.5}
      ],
      "sub_intents": [
        "maternity coverage",
        "pregnancy termination",
        "well mother care",
        "routine preventive care",
        "maternity hospitalization"
      ],
      "weight": 1.0
    },
    "Coverage": {
      "keywords": [
        {"text": "inpatient hospitalization", "weight": 2.5},
        {"text": "sum insured", "weight": 2.0},
        {"text": "medical expenses", "weight": 1.5},
        {"text": "room rent", "weight": 1.0},
        {"text": "ambulance", "weight": 1.2},
        {"text": "air ambulance", "weight": 2.0},
        {"text": "ayurvedic", "weight": 1.5},
        {"text": "homeopathic", "weight": 1.5},
        {"text": "trip cancellation", "weight": 2.0},
        {"text": "baggage loss", "weight": 1.5},
        {"text": "personal accident", "weight": 1.5},
        {"text": "well baby care", "weight": 2.0},
        {"text": "new born baby expenses", "weight": 2.0},
        {"text": "routine medical care", "weight": 1.5},
        {"text": "daily cash", "weight": 1.2},
        {"text": "pre-hospitalization", "weight": 2.0},
        {"text": "post-hospitalization", "weight": 2.0},
        {"text": "home treatment", "weight": 1.5}
      ],
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
      "weight": 1.0
    },
    "Exclusions": {
      "keywords": [
        {"text": "pre-existing disease", "weight": 2.0},
        {"text": "waiting period", "weight": 2.0},
        {"text": "exclusion", "weight": 2.0},
        {"text": "cosmetic surgery", "weight": 1.5},
        {"text": "obesity", "weight": 1.5},
        {"text": "alcoholism", "weight": 1.5},
        {"text": "drug dependency", "weight": 1.5},
        {"text": "war", "weight": 2.0},
        {"text": "terrorism", "weight": 2.0},
        {"text": "sterility", "weight": 1.5},
        {"text": "infertility", "weight": 1.5},
        {"text": "dental treatment", "weight": 1.5},
        {"text": "non-medical expenses", "weight": 1.5}
      ],
      "sub_intents": [
        "pre-existing disease",
        "waiting period",
        "cosmetic surgery",
        "substance abuse",
        "war and terrorism",
        "non-medical expenses"
      ],
      "weight": 1.0
    },
    "Claims": {
      "keywords": [
        {"text": "notification of claim", "weight": 2.0},
        {"text": "cashless facility", "weight": 2.0},
        {"text": "reimbursement", "weight": 1.5},
        {"text": "claim procedure", "weight": 1.5},
        {"text": "assistance service provider", "weight": 1.5},
        {"text": "claim documentation", "weight": 1.5},
        {"text": "nominee", "weight": 1.5}
      ],
      "sub_intents": [
        "claim process",
        "cashless claims",
        "reimbursement process",
        "nominee payment"
      ],
      "weight": 1.0
    }
  }
}

@dataclass
class ChunkMetadata:
    """Represents metadata for a text chunk"""
    chunk_id: str
    text: str
    main_intent: str
    sub_intent: str
    confidence_score: float
    keywords_found: List[str]
    chunk_type: str = "text"
    domain: str = "insurance"

class InsuranceIntentClassifier:
    """Classifies insurance-related text chunks into intents and sub-intents"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.intents = config["intents"]
        self.domain = config["domain"]
        
        # Build keyword mappings for faster lookup
        self.keyword_to_intent = {}
        self.sub_intent_keywords = {}
        
        for intent_name, intent_data in self.intents.items():
            # Map keywords to main intent
            for keyword_info in intent_data["keywords"]:
                keyword = keyword_info["text"].lower()
                self.keyword_to_intent[keyword] = {
                    "intent": intent_name,
                    "weight": keyword_info["weight"]
                }
            
            # Map sub-intents to their parent intent
            for sub_intent in intent_data["sub_intents"]:
                self.sub_intent_keywords[sub_intent.lower()] = intent_name
    
    def classify_chunk(self, text: str, chunk_id: str = None) -> ChunkMetadata:
        """
        Classify a text chunk into main intent and sub-intent
        
        Args:
            text: The text to classify
            chunk_id: Unique identifier for the chunk
            
        Returns:
            ChunkMetadata object with classification results
        """
        text_lower = text.lower()
        
        # Find matching keywords and calculate scores
        intent_scores = defaultdict(float)
        keywords_found = []
        
        for keyword, intent_info in self.keyword_to_intent.items():
            if keyword in text_lower:
                intent_name = intent_info["intent"]
                weight = intent_info["weight"]
                intent_scores[intent_name] += weight
                keywords_found.append(keyword)
        
        # Determine main intent
        if intent_scores:
            main_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
            confidence_score = intent_scores[main_intent] / sum(intent_scores.values())
        else:
            main_intent = "Unknown"
            confidence_score = 0.0
        
        # Determine sub-intent
        sub_intent = self._determine_sub_intent(text_lower, main_intent)
        
        return ChunkMetadata(
            chunk_id=chunk_id or f"chunk_{hash(text) % 10000}",
            text=text,
            main_intent=main_intent,
            sub_intent=sub_intent,
            confidence_score=confidence_score,
            keywords_found=keywords_found
        )
    
    def _determine_sub_intent(self, text: str, main_intent: str) -> str:
        """Determine the specific sub-intent based on text content"""
        if main_intent not in self.intents:
            return "unknown"
        
        intent_data = self.intents[main_intent]
        sub_intent_scores = {}
        
        # Score each sub-intent based on keyword presence
        for sub_intent in intent_data["sub_intents"]:
            score = 0
            sub_intent_words = sub_intent.lower().split()
            
            # Check if sub-intent words appear in text
            for word in sub_intent_words:
                if word in text:
                    score += 1
            
            # Normalize score by sub-intent length
            if len(sub_intent_words) > 0:
                sub_intent_scores[sub_intent] = score / len(sub_intent_words)
        
        # Return the highest scoring sub-intent
        if sub_intent_scores:
            return max(sub_intent_scores.items(), key=lambda x: x[1])[0]
        else:
            return "general"
    
    def chunk_text(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks based on sentences and size limits
        
        Args:
            text: The text to chunk
            max_chunk_size: Maximum size of each chunk
            
        Returns:
            List of text chunks
        """
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # If adding this sentence would exceed chunk size, start new chunk
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_document(self, document_text: str) -> List[ChunkMetadata]:
        """
        Process a complete document by chunking and classifying each chunk
        
        Args:
            document_text: The complete document text
            
        Returns:
            List of ChunkMetadata objects for each chunk
        """
        chunks = self.chunk_text(document_text)
        metadata_list = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"chunk_{i+1}"
            metadata = self.classify_chunk(chunk, chunk_id)
            metadata_list.append(metadata)
        
        return metadata_list

# Example usage and demonstration
def demonstrate_intent_classification():
    """Demonstrate how intents and sub-intents work in practice"""
    
    # Initialize the classifier
    classifier = InsuranceIntentClassifier(INSURANCE_DOMAIN_CONFIG)
    
    # Sample insurance document text
    sample_text = """
    Premium Payment and Grace Period: The policyholder has a 30-day grace period for premium payment. 
    Additional premium may be charged for high-risk activities. Renewal premium discounts are available 
    for claim-free years.
    
    Maternity Coverage: The policy covers maternity expenses including childbirth, caesarean delivery, 
    and well mother care. Routine preventive care and immunizations are also covered. Maternity 
    hospitalization expenses up to the sum insured are reimbursed.
    
    Coverage Details: Inpatient hospitalization expenses are covered up to the specified sum insured. 
    The policy includes ambulance services, air ambulance coverage, and AYUSH treatment options. 
    Pre-hospitalization and post-hospitalization expenses are covered for 30 days before and 60 days 
    after admission.
    
    Exclusions: Pre-existing diseases are excluded for the first 48 months. Cosmetic surgery, 
    obesity treatment, and dental procedures are not covered. War and terrorism-related claims 
    are excluded from coverage.
    
    Claims Process: Cashless facility is available at network hospitals. For reimbursement claims, 
    proper documentation must be submitted within 30 days. The assistance service provider will 
    guide through the claim procedure.
    """
    
    print("=== INSURANCE INTENT CLASSIFICATION DEMONSTRATION ===\n")
    
    # Process the document
    metadata_list = classifier.process_document(sample_text)
    
    print("Document Chunks and Their Classifications:\n")
    for metadata in metadata_list:
        print(f"Chunk ID: {metadata.chunk_id}")
        print(f"Text: {metadata.text[:100]}...")
        print(f"Main Intent: {metadata.main_intent}")
        print(f"Sub Intent: {metadata.sub_intent}")
        print(f"Confidence Score: {metadata.confidence_score:.2f}")
        print(f"Keywords Found: {metadata.keywords_found}")
        print("-" * 80)
    
    # Show how metadata can be used for different purposes
    print("\n=== METADATA USAGE EXAMPLES ===\n")
    
    # Group by main intent
    intent_groups = defaultdict(list)
    for metadata in metadata_list:
        intent_groups[metadata.main_intent].append(metadata)
    
    print("Chunks Grouped by Main Intent:")
    for intent, chunks in intent_groups.items():
        print(f"\n{intent} ({len(chunks)} chunks):")
        for chunk in chunks:
            print(f"  - {chunk.sub_intent}: {chunk.text[:50]}...")
    
    # Find chunks with high confidence
    high_confidence_chunks = [m for m in metadata_list if m.confidence_score > 0.5]
    print(f"\nHigh Confidence Chunks (>0.5): {len(high_confidence_chunks)}")
    
    # Show keyword distribution
    all_keywords = []
    for metadata in metadata_list:
        all_keywords.extend(metadata.keywords_found)
    
    keyword_counts = defaultdict(int)
    for keyword in all_keywords:
        keyword_counts[keyword] += 1
    
    print(f"\nMost Common Keywords:")
    for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {keyword}: {count} occurrences")

if __name__ == "__main__":
    demonstrate_intent_classification()