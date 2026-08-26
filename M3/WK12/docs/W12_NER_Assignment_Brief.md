# Assignment: End-to-End Named Entity Recognition (NER) for Customer Support Ticket Analysis

**Course:** Fusemachines AI Fellowship 2026 · **Points:** 100 · **Instructor:** Nirajan Bekoju

## Overview

Companies receive thousands of customer support tickets every day. Automatically identifying key entities such as customer names, organizations, products, locations, dates, and monetary values helps route tickets faster, automate CRM updates, and improve response times.

In this assignment, you will build an end-to-end Named Entity Recognition (NER) pipeline, starting from text preprocessing and exploratory analysis to training and evaluating an NER model.

## Dataset

- **Primary:** CoNLL-2003 Named Entity Recognition Dataset
- **Optional:** WNUT-17 Emerging Entities Dataset

## Core Tasks

### Task 1: Text Preprocessing
Prepare the dataset for NER.
- Tokenize the text.
- Inspect entity labels.
- Analyze sentence length and entity distribution.

**Deliverable:** Report the number of sentences, vocabulary size, and frequency of each entity type.

### Task 2: Feature Engineering
Generate features for sequence labeling.
- Create word-level features (lowercase, prefixes/suffixes, capitalization).
- Optionally include POS tags or word embeddings.

**Deliverable:** Briefly explain the selected features and why they are useful for NER.

### Task 3: Named Entity Recognition
Train an NER model — implement either:
- Conditional Random Field (CRF), or
- BiLSTM

**Deliverable:** Precision, Recall, F1-score, entity-wise performance. Discuss which entity types are most difficult to recognize and why.

### Task 4: Error Analysis
Evaluate model predictions.
- Display sample predictions.
- Compare predicted vs. true entities.
- Identify common error patterns.

**Deliverable:** Summarize the three most frequent types of errors.

### Task 5: Business Impact
Assume the model will be deployed in a customer support system. Discuss:
- How NER can automate ticket routing.
- How extracted entities improve customer service.
- Limitations of the current system and possible improvements.

**Deliverable:** A short business recommendation (150–200 words).

### Task 6: Optional Dataset
Perform similar analysis and modelling using the optional dataset: WNUT-17 Emerging Entities Dataset.

## Submission Requirements

Submit one Jupyter Notebook (`.ipynb`) containing:
- Well-structured Markdown explanations
- Clearly commented code
- Visualizations where appropriate
- Results and discussion for each task
