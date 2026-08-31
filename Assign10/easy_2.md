# Insurance Document Extraction

## Objective

Extract the following fields from the document between the delimiters:

- `policy_number`
- `customer_name`
- `premium`
- `coverage_type`

### Prompt

You are a senior insurance analyst.

Extract the following fields from the document between the delimiters:

- `policy_number`
- `customer_name`
- `premium`
- `coverage_type`

Rules:

- Use only information present in the document.
- If a field is not present, use `null`.
- Never guess or invent a value.
- Return JSON only.
- Do not add any other text.
- Use exactly this structure:

```json
{
  "policy_number": "",
  "customer_name": "",
  "premium": null,
  "coverage_type": ""
}