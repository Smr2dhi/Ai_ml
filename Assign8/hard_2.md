# Hard 2 — AI Use Case Report

## 1) Industry & Use Case

**Industry:** Banking  
**Use Case:** AI-Powered Fraud Detection

## 2) User Persona

**Role:** Bank Fraud Analyst

**Example Queries / Needs:**

- “Show me transactions that appear unusual so I can investigate them.”
- “Help me identify high-risk transactions before they result in financial losses.”

## 3) Business Problem

Bank fraud analysts review a large volume of transactions every day to identify potentially fraudulent activity. Manual investigation is time-consuming and can result in both false positives and missed fraudulent transactions. Delays in identifying suspicious activity can increase financial losses, investigation costs, and customer complaints.

## 4) Current Process

1. Transaction data is collected from customer accounts and payment systems.
2. Transactions are screened using predefined rules and thresholds.
3. Potentially suspicious transactions are flagged for manual investigation.
4. Analysts review customer transaction history and relevant transaction details.
5. Confirmed fraud cases are escalated for appropriate action or customer verification.

## 5) Proposed AI Solution

The proposed solution uses an AI-based fraud detection model to analyze transaction patterns and generate a fraud-risk score for each transaction. The model identifies unusual transaction behavior and prioritizes high-risk transactions for review.

This allows fraud analysts to focus on the transactions that require immediate attention while reducing unnecessary manual review.

**Category:** Predictive AI  
**Type:** AI Feature
## 6) Solution Architecture

The proposed fraud detection system collects transaction data, processes it, analyzes transaction patterns using an AI model, and provides a fraud-risk score to the bank's fraud analyst.

```text
+-----------------------+
|   Banking Systems     |
|-----------------------|
| Cards | ATM | Online  |
| Mobile | Payments     |
+-----------+-----------+
            |
            v
+-----------------------+
|   Transaction Data    |
|-----------------------|
| Amount | Time         |
| Location | Merchant   |
| Account History      |
+-----------+-----------+
            |
            v
+-----------------------+
| Data Processing       |
| & Feature Engineering |
+-----------+-----------+
            |
            v
+-----------------------+
|  AI Fraud Detection   |
|        Model          |
+-----------+-----------+
            |
            v
+-----------------------+
|   Fraud Risk Score    |
|-----------------------|
| Low | Medium | High   |
+-----------+-----------+
            |
            v
+-----------------------+
|    Fraud Analyst      |
|-----------------------|
| Review & Investigation|
+-----------+-----------+
            |
            v
+-----------------------+
|   Final Decision      |
|-----------------------|
| Genuine | Fraud       |
| Verification Required|
+-----------------------+
```


**Build vs. Buy:** The bank should initially **integrate an existing AI fraud-detection service** rather than build the entire system from scratch. This approach allows the bank to deploy fraud detection faster and reduce initial development effort and cost. Following Session 16's point that most companies **build AI features** rather than entire AI systems, the bank can later develop a custom fraud-detection feature on top of existing AI capabilities to better match its own transaction patterns and business requirements.