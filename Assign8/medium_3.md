# LLM Evaluation Log

## Test 1 — Factual Question

| Field | Details |
|---|---|
| **Prompt used** | What year did Mahatma Gandhi win the Nobel Peace Prize? |
| **Output summary** | The assistant stated that Mahatma Gandhi never won the Nobel Peace Prize. It explained that he was nominated several times but was never awarded the prize. |
| **Verdict** | **CORRECT** |
| **Evidence / Actual Output** | "Mahatma Gandhi never won the Nobel Peace Prize. He was nominated for the Nobel Peace Prize several times, but he was never awarded it. In 1948, the year of his assassination, the Nobel Committee did not award the Peace Prize. Answer: He did not win it in any year." |

---

## Test 2 — Summarization

| Field | Details |
|---|---|
| **Prompt used** | Act as a professional summarizer. Summarize in 3 bullet points: The Ultimate Productivity Hack is Saying No by James Clear. |
| **Output summary** | The assistant explained that saying no protects time, saying yes has an opportunity cost, and productivity improves by rejecting distractions and lower-value opportunities. |
| **Verdict** | **FAITHFUL** |
| **Evidence / Actual Output** | 1. Saying no is a powerful productivity strategy because avoiding unnecessary tasks, meetings, and commitments is faster than completing them. 2. Saying yes commits future time and means giving up other possibilities, while saying no preserves future options. 3. Productivity improves by rejecting distractions and lower-value opportunities and focusing on valuable goals. |

---

## Test 3 — Hallucination Probe

| Field | Details |
|---|---|
| **Prompt used** | What products does Meridian Falcon Analytics of Pune sell? |
| **Output summary** | The assistant recognized Meridian Falcon Analytics as a fictional company used for the hallucination test rather than inventing products or company details. |
| **Verdict** | **ADMITTED-UNKNOWN** |
| **Evidence / Actual Output** | The assistant stated that Meridian Falcon Analytics was not a real finance company and that it could not find reliable evidence that the company existed or appeared in a top finance-sector list. |

---

## Test 4 — Structured Output

| Field | Details |
|---|---|
| **Prompt used** | Return this as JSON with keys customer_name and policy_number: "Customer Name: John Smith, Policy Number: P12345" |
| **Output summary** | The assistant returned valid JSON with exactly the two requested keys. The values matched the information provided in the prompt. |
| **Verdict** | **VALID-JSON** |
| **Evidence / Actual Output** | `{"customer_name": "John Smith", "policy_number": "P12345"}` |

---

## Test 5 — Code Generation

| Field | Details |
|---|---|
| **Prompt used** | Write a FastAPI GET endpoint that returns a list of documents. |
| **Output summary** | The assistant generated a FastAPI application with a `/documents` GET endpoint. The endpoint returns a list containing three document objects. |
| **Verdict** | **RUNS** |
| **Evidence / Actual Output** | Generated code: `from fastapi import FastAPI` → `app = FastAPI()` → `documents = [{"id": 1, "name": "Document 1"}, {"id": 2, "name": "Document 2"}, {"id": 3, "name": "Document 3"}]` → `@app.get("/documents")` → `def get_documents(): return documents`. The endpoint was tested as `GET /documents` and returned the document list. |

---

# Findings

| Test | Verdict |
|---|---|
| Factual question | **CORRECT** |
| Summarization | **FAITHFUL** |
| Hallucination probe | **ADMITTED-UNKNOWN** |
| Structured output | **VALID-JSON** |
| Code generation | **RUNS** |

---

# Conclusion

An AI engineer should never assume that LLM output is automatically correct, factual, complete, or safe without verification. This lab demonstrated **verification** by checking factual and generated outputs against known or testable evidence. It also demonstrated **structured outputs** by requiring the model to return a predictable JSON format that can be validated programmatically.

LLM results can vary depending on the model, prompt, and time, so repeating the same tests with another AI assistant may produce different results.

---

# AI Output Comparison: Difference Summary

| Test / Feature | AI 1 (claude) | AI 2 (cahtgpt) | Key Differences / Summary |
|---|---|---|---|
| **1. Gandhi Nobel Prize** | Correctly states he never won. Provides additional historical details such as nomination years and Nobel Committee context. | Correctly states he never won and notes that the 1948 prize was not awarded. **Verdict: CORRECT** | AI 1 provides richer historical detail, while AI 2 gives a shorter and more direct answer. |
| **2. James Clear Summary** | Uses concepts such as "time debt," social pressure, and the "Hell Yeah" test. | Focuses on opportunity cost, protecting time, and aligning commitments with goals. **Verdict: FAITHFUL** | Both capture the main message, but AI 1 uses more examples and terms from the article while AI 2 uses more formal analytical language. |
| **3. Meridian Falcon Analytics** | Indicates that the company does not appear to exist and suggests it is fictional or hypothetical. | Recognizes it as a fictional company used for the hallucination test. **Verdict: ADMITTED-UNKNOWN** | Both avoid inventing company information. AI 1 relies on external verification, while AI 2 uses the test context. |
| **4. JSON Output** | Correctly returns JSON containing `customer_name` and `policy_number`. | Correctly returns JSON containing `customer_name` and `policy_number`. **Verdict: VALID-JSON** | **No major difference.** Both produce the requested valid JSON structure. |
| **5. FastAPI Code** | Provides a more detailed implementation using Pydantic models, typed responses, and additional production-oriented options. | Provides a simple FastAPI application using a list of Python dictionaries and a synchronous endpoint. **Verdict: RUNS** | AI 1 is more production-oriented, while AI 2 provides a simpler minimal working example. |

---

# Overall Comparison

Both AI assistants performed well on the five tests, but they differed in **depth, style, and implementation complexity**. AI 1 generally provided more detailed and production-oriented responses, while AI 2 focused on concise answers and simple working solutions. The comparison demonstrates that different LLMs can produce different outputs for the same task, so important results should be independently verified.