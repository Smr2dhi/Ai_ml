# Support Ticket Classifier — Zero to Few-Shot

## 1. Zero-Shot

Classify the support ticket as Complaint, Feedback, or Inquiry.

Reply with the category name only.

Classify this ticket:

"My package arrived with a broken seal and no invoice."

### Results

| Prompt Version | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Zero-Shot | Complaint | Complaint | Complaint |

---

## 2. One-Shot

Classify the support ticket as Complaint, Feedback, or Inquiry.

Email: Refund not received  
Category: Complaint

Reply with the category name only.

Classify this ticket:

"My package arrived with a broken seal and no invoice."

### Results

| Prompt Version | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| One-Shot | Complaint | Complaint | Complaint |

---

## 3. Few-Shot

Classify the support ticket as Complaint, Feedback, or Inquiry.

Email: Refund not received  
Category: Complaint

Email: Your service was very helpful  
Category: Feedback

Email: What documents are required to open an account?  
Category: Inquiry

Reply with the category name only.

Classify this ticket:

"My package arrived with a broken seal and no invoice."

### Results

| Prompt Version | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Few-Shot | Complaint | Complaint | Complaint |

---

## 4. Comparison

| Prompt Version | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Zero-Shot | Complaint | Complaint | Complaint |
| One-Shot | Complaint | Complaint | Complaint |
| Few-Shot | Complaint | Complaint | Complaint |

## 5. Observation

Few-Shot was the most consistent because it provided examples for all three categories. The examples gave the model a clear pattern to follow.

# Extension — Urgent Escalation

## Few-Shot Prompt

Classify the support ticket as Complaint, Feedback, Inquiry, or Urgent Escalation.

Email: Refund not received  
Category: Complaint

Email: Your service was very helpful  
Category: Feedback

Email: What documents are required to open an account?  
Category: Inquiry

Email: This is the third time I am writing — I will contact my lawyer.  
Category: Urgent Escalation

Reply with the category name only.

Classify this ticket:

"This is the third time I am writing — I will contact my lawyer."

### Result

Urgent Escalation