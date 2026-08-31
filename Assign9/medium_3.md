# Medium 3: Prompt Ladder — Vague to Structured, Measured

## Objective

The purpose of this experiment is to understand how **prompt quality affects the quality of an LLM response**.

The same task — **explaining a company leave policy to a new employee** — is tested using three different prompts:

- **V1:** Vague
- **V2:** Improved
- **V3:** Structured

Each prompt is tested in a **fresh conversation** so that previous conversations do not influence the results.

---

## V1 — Vague Prompt

### Prompt

> Tell me about leave policy.

### LLM Response

> Leave policies generally explain the different types of leave employees can take, such as annual leave, sick leave, casual leave, and other approved absences. Employees may need to request leave in advance and obtain approval from their manager or HR. The exact number of leave days and rules depend on the company's policy.

### Observation

V1 is very vague. It does not provide the employee's situation, the actual company policy, specific instructions, or an expected output format.

The response is therefore **generic** and may contain general information that is not necessarily part of the company's actual policy.

---

## V2 — Improved Prompt

### Prompt

> You are an HR assistant helping new employees in their first week at the company.
>
> Explain the company's leave policy to a new employee in a clear and helpful way.

### LLM Response

> As a new employee, understanding the company's leave policy can help you plan your time off properly. The leave policy may include different types of leave, such as annual leave and sick leave. You may need to submit leave requests through the company's HR system and receive approval before taking leave. If you are unsure about a particular type of leave, you should contact HR for clarification.

### Observation

V2 is better because it provides:

- **Role:** HR assistant
- **Audience:** New employees in their first week
- **Task:** Explain the leave policy

However, the actual company policy is still not provided. Therefore, the model may still give generic information instead of the company's real rules.

---

## V3 — Structured Prompt

### Prompt

> You are an HR assistant helping a new employee in their first week.
>
> Explain the following company leave policy using **ONLY** the information provided below.
>
> Use simple language.
>
> Keep the answer under 150 words.
>
> Do not invent company-specific numbers or rules.
>
> **Output format:**
>
> 1. Start with one short introduction sentence.
> 2. Then give exactly 4 bullet points.
> 3. End with one closing line telling the employee where to ask follow-up questions.
>
> **Policy:**
>
> Employees receive 18 days of annual leave per year.  
> Leave must be applied 3 days in advance through the HR portal.  
> A maximum of 5 days can be carried forward to the next year.  
> Sick leave requires a medical certificate after 2 consecutive days.

### LLM Response

> Welcome! Here are the key points you need to know about the company's leave policy:
>
> - Employees receive **18 days of annual leave** each year.
> - Annual leave must be requested **3 days in advance through the HR portal**.
> - A maximum of **5 unused leave days** can be carried forward to the next year.
> - Sick leave requires a **medical certificate after 2 consecutive days**.
>
> For any questions or clarification, please contact HR.

### Observation

V3 is the strongest prompt because it provides:

- **Role:** HR assistant
- **Audience:** New employee
- **Task:** Explain the leave policy
- **Context:** Actual company policy
- **Grounding:** Use only the provided information
- **Constraints:** Simple language and under 150 words
- **Output format:** Introduction + exactly 4 bullet points + closing line

This makes the response more reliable, structured, and useful.

---

## Scorecard

| Criteria | V1 | V2 | V3 |
|---|---:|---:|---:|
| Relevance to a new employee | 2/5 | 4/5 | 5/5 |
| Structure | 1/5 | 3/5 | 5/5 |
| Grounding | 1/5 | 1/5 | 5/5 |
| Usability | 1/5 | 3/5 | 5/5 |

### Score Explanation

| Criteria | Explanation |
|---|---|
| **Relevance** | V1 is generic, V2 targets new employees, and V3 directly explains the provided company policy to a new employee. |
| **Structure** | V1 has no specific structure, V2 has basic instructions, and V3 requires a specific output format. |
| **Grounding** | V1 and V2 do not contain the actual policy, so they cannot be grounded in company-specific information. V3 uses only the provided policy. |
| **Usability** | V1 is too generic for onboarding. V2 is more useful but may contain assumptions. V3 is clear, concise, and suitable for an onboarding message. |

---

## Comparison

### V1

**Vague → Generic response**

The model has very little information and may provide general leave-policy information.

### V2

**Role + Audience + Task → More relevant response**

The model understands that it is acting as an HR assistant and answering a new employee.

### V3

**Role + Audience + Task + Context + Constraints + Format → Reliable and useful response**

The model receives the actual policy and is explicitly instructed not to use information outside it.

---

## Conclusion

This experiment shows that **better prompts produce more relevant, structured, and reliable LLM responses**.

V1 was vague and produced generic information. V2 improved the response by adding a role, audience, and clear task, but it was still not grounded in the company's actual policy. V3 produced the best response because it added **context, grounding, constraints, and a specific output format**.

---

## What I Learned

Through this exercise, I learned that **prompt engineering is more than simply asking a question**. A good prompt should clearly define the role of the AI, the target audience, the task, the information the AI can use, the restrictions it must follow, and the required output format.

I also learned the importance of **grounding**. If we do not provide the actual company policy, the LLM may give generic information or invent plausible details. By providing the policy and saying **"use ONLY the information provided"**, we can make the response more controlled and reliable.

V3 is also a simple preview of **RAG (Retrieval-Augmented Generation)** because relevant information is provided to the model as context before generating the answer.

This learning will be useful in future **real LLM API applications**. Instead of manually writing prompts, a Python application can take a user's question and a relevant document, insert them into a prompt template, send the completed prompt to an LLM API, and return the generated answer.

---

## Key Learning

```text
Vague Prompt
     ↓
Generic Response
     ↓
Better Prompt
     ↓
More Relevant Response
     ↓
Structured + Grounded Prompt
     ↓
More Reliable + Useful Response