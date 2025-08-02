# Insurance Intent Classification: How Intents and Sub-Intents Work

## Overview

Your insurance domain configuration uses a hierarchical classification system with **Main Intents** and **Sub-Intents** to categorize text chunks. This system helps organize and understand insurance-related content at different levels of specificity.

## Structure Breakdown

### 1. Main Intents (Top Level)
Your configuration has 5 main intents:
- **Premiums** - Payment-related topics
- **Maternity** - Pregnancy and childbirth coverage
- **Coverage** - What's covered by the policy
- **Exclusions** - What's not covered
- **Claims** - How to file and process claims

### 2. Sub-Intents (Specific Categories)
Each main intent has specific sub-intents that provide more granular classification:

#### Premiums Sub-Intents:
- `grace period` - Time allowed for late payments
- `premium payment` - General payment processes
- `additional premium payment` - Extra charges
- `renewal premium discount` - Discounts for renewals

#### Maternity Sub-Intents:
- `maternity coverage` - General maternity benefits
- `pregnancy termination` - Abortion coverage
- `well mother care` - Preventive care for mothers
- `routine preventive care` - Regular checkups
- `maternity hospitalization` - Hospital stays for childbirth

## How It Works in Practice

### Step 1: Text Chunking
```
Original Document → Split into chunks → Each chunk gets metadata
```

**Example:**
```
Input: "Premium Payment and Grace Period: The policyholder has a 30-day grace period for premium payment."

Chunk: "Premium Payment and Grace Period: The policyholder has a 30-day grace period for premium payment."
```

### Step 2: Keyword Matching
The system looks for keywords in each chunk:

```python
# Keywords found in the chunk:
- "grace period" (weight: 2.0)
- "premium" (weight: 1.5)
- "payment" (weight: 1.0)

# Total score for "Premiums" intent: 4.5
```

### Step 3: Main Intent Classification
The system calculates scores for each main intent and selects the highest:

```python
Intent Scores:
- Premiums: 4.5 (grace period + premium + payment)
- Maternity: 0.0 (no keywords found)
- Coverage: 0.0 (no keywords found)
- Exclusions: 0.0 (no keywords found)
- Claims: 0.0 (no keywords found)

Result: Main Intent = "Premiums"
```

### Step 4: Sub-Intent Classification
Within the "Premiums" intent, the system determines the specific sub-intent:

```python
Sub-intent scores within "Premiums":
- "grace period": 1.0 (both words found)
- "premium payment": 1.0 (both words found)
- "additional premium payment": 0.67 (2/3 words found)
- "renewal premium discount": 0.25 (1/4 words found)

Result: Sub Intent = "grace period" (highest score)
```

## Metadata Structure

Each chunk gets rich metadata:

```python
ChunkMetadata(
    chunk_id="chunk_1",
    text="Premium Payment and Grace Period: The policyholder has a 30-day grace period for premium payment.",
    main_intent="Premiums",
    sub_intent="grace period",
    confidence_score=0.85,
    keywords_found=["grace period", "premium", "payment"],
    chunk_type="text",
    domain="insurance"
)
```

## Real-World Usage Examples

### 1. Document Organization
```python
# Group chunks by main intent
premium_chunks = [chunk for chunk in all_chunks if chunk.main_intent == "Premiums"]
maternity_chunks = [chunk for chunk in all_chunks if chunk.main_intent == "Maternity"]

# Find specific sub-intent chunks
grace_period_chunks = [chunk for chunk in all_chunks if chunk.sub_intent == "grace period"]
```

### 2. Search and Retrieval
```python
# Find all chunks about claims processing
claims_chunks = [chunk for chunk in all_chunks 
                 if chunk.main_intent == "Claims" and chunk.confidence_score > 0.7]

# Find chunks about specific coverage types
ambulance_chunks = [chunk for chunk in all_chunks 
                   if "ambulance" in chunk.keywords_found]
```

### 3. Content Analysis
```python
# Analyze document structure
intent_distribution = {}
for chunk in all_chunks:
    intent = chunk.main_intent
    intent_distribution[intent] = intent_distribution.get(intent, 0) + 1

# Result: {"Premiums": 3, "Coverage": 5, "Claims": 2, ...}
```

### 4. Quality Assurance
```python
# Find low-confidence classifications
uncertain_chunks = [chunk for chunk in all_chunks if chunk.confidence_score < 0.3]

# Find chunks that might need manual review
mixed_intent_chunks = [chunk for chunk in all_chunks 
                      if len(chunk.keywords_found) > 5]  # Too many keywords might indicate confusion
```

## Benefits of This Approach

### 1. **Hierarchical Organization**
- Main intents provide broad categorization
- Sub-intents provide specific topic identification
- Easy to navigate from general to specific

### 2. **Flexible Search**
- Search by main intent: "Show me all premium-related content"
- Search by sub-intent: "Show me grace period information"
- Search by keywords: "Find content mentioning 'cashless facility'"

### 3. **Content Analysis**
- Understand document structure and focus areas
- Identify gaps in coverage (missing intents)
- Measure content quality and confidence

### 4. **Automated Processing**
- Route content to appropriate teams/departments
- Generate automatic summaries by intent
- Create topic-based indexes

## Example Output

When you run the demonstration, you'll see output like this:

```
=== INSURANCE INTENT CLASSIFICATION DEMONSTRATION ===

Document Chunks and Their Classifications:

Chunk ID: chunk_1
Text: Premium Payment and Grace Period: The policyholder has a 30-day grace period for premium payment...
Main Intent: Premiums
Sub Intent: grace period
Confidence Score: 0.85
Keywords Found: ['grace period', 'premium', 'payment']
--------------------------------------------------------------------------------

Chunk ID: chunk_2
Text: Maternity Coverage: The policy covers maternity expenses including childbirth, caesarean delivery...
Main Intent: Maternity
Sub Intent: maternity coverage
Confidence Score: 0.92
Keywords Found: ['maternity expenses', 'childbirth', 'caesarean', 'well mother care']
--------------------------------------------------------------------------------

=== METADATA USAGE EXAMPLES ===

Chunks Grouped by Main Intent:

Premiums (1 chunks):
  - grace period: Premium Payment and Grace Period: The policyholder has a 30-day...

Maternity (1 chunks):
  - maternity coverage: Maternity Coverage: The policy covers maternity expenses...

Coverage (1 chunks):
  - inpatient treatment: Coverage Details: Inpatient hospitalization expenses are covered...

Exclusions (1 chunks):
  - pre-existing disease: Exclusions: Pre-existing diseases are excluded for the first...

Claims (1 chunks):
  - claim process: Claims Process: Cashless facility is available at network hospitals...

High Confidence Chunks (>0.5): 5

Most Common Keywords:
  - premium: 2 occurrences
  - maternity: 2 occurrences
  - coverage: 2 occurrences
  - grace period: 1 occurrences
  - childbirth: 1 occurrences
```

## Key Takeaways

1. **Main Intents** provide broad categorization (Premiums, Maternity, Coverage, etc.)
2. **Sub-Intents** provide specific topic identification within each main intent
3. **Keywords** with weights determine the classification
4. **Confidence Scores** indicate how certain the classification is
5. **Metadata** enables powerful search, filtering, and analysis capabilities

This system allows you to automatically organize insurance documents, route queries to the right experts, and build intelligent search systems that understand the context and specificity of insurance-related content.