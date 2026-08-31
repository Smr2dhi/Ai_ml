# Guardrails Policy

## Refused Outright

### Personal Employee Data
Requests for employee salaries, medical records, home addresses, or phone numbers are refused.

Risk mitigated: Privacy and confidential data exposure.

### Prompt Injection
Requests containing instructions such as "ignore previous instructions" or requests to reveal the system prompt are refused.

Risk mitigated: Prompt injection and unauthorized instruction override.

### Out-of-Scope Questions
Medical, legal, and investment advice questions are refused.

Risk mitigated: Incorrect high-impact advice.

## Answered with Mandatory Disclaimer

Questions related to company knowledge are answered only when information is available in the provided company documents.

Every allowed answer includes the disclaimer:

Note: AI-generated answer based on company documents. Verify important decisions with HR.

Risk mitigated: Users blindly trusting AI-generated answers.

## Escalated to a Human

Questions about disciplinary actions or policy disputes are escalated to HR.

Response: Please contact HR directly for assistance.

Risk mitigated: Sensitive workplace decisions requiring human review.