# Summarize-then-Extract — Two-Step Prompt Chain

## Objective

To understand prompt chaining by breaking a complex task into two steps:

**Document → Summary → Structured JSON**

## Input Document

<<<

On 14 July, the payroll system was unavailable for 6 hours because a disk filled up on the database server. Salary processing for 230 employees was delayed by one day. The IT team added disk monitoring alerts and a weekly cleanup job. Total estimated cost of the outage is 40000. The incident is now closed.

>>>

---

## Step 1: Summarization Prompt

### Prompt

You are a business analyst.

Think step by step:
1. Identify the issue.
2. Identify the cause.
3. Identify the resolution.

Return a summary of at most 60 words under exactly these headings: **Issue, Cause, Resolution**.

Document:

<<<

On 14 July, the payroll system was unavailable for 6 hours because a disk filled up on the database server. Salary processing for 230 employees was delayed by one day. The IT team added disk monitoring alerts and a weekly cleanup job. Total estimated cost of the outage is 40000. The incident is now closed.

>>>

### Output

**Issue:** Payroll system was unavailable, delaying salary processing.

**Cause:** A disk filled up on the database server.

**Resolution:** IT added disk monitoring alerts and a weekly cleanup job, and the incident was closed.

---

## Step 2: Extraction Prompt

The summary from Step 1 is used as the input. The original document is not used.

### Prompt

Extract the following fields from the summary:

- incident_date
- system
- downtime_hours
- employees_affected
- estimated_cost
- status

If information is missing, use `null`.

Return JSON only. Do not add any other text.

Use exactly these keys:

{
  "incident_date": null,
  "system": "",
  "downtime_hours": null,
  "employees_affected": null,
  "estimated_cost": null,
  "status": ""
}

Summary:

<<<

Issue: Payroll system was unavailable, delaying salary processing.

Cause: A disk filled up on the database server.

Resolution: IT added disk monitoring alerts and a weekly cleanup job, and the incident was closed.

>>>

### Output

{
  "incident_date": null,
  "system": "payroll system",
  "downtime_hours": null,
  "employees_affected": null,
  "estimated_cost": null,
  "status": "closed"
}

---

## Lost Field

The field `downtime_hours` was lost because the first summary did not include the number **6**.

### Fix Added to Prompt 1

**"Always keep all numbers and dates in the summary, including downtime hours, employees affected, estimated cost, and incident date. Also preserve the incident status."**

---

## Step 1 After Fix

**Issue:** Payroll system was unavailable for 6 hours on 14 July, delaying salary processing for 230 employees.

**Cause:** A disk filled up on the database server.

**Resolution:** IT added disk monitoring alerts and a weekly cleanup job. Estimated cost was 40000 and the incident is now closed.

---

## Final JSON After Fix

{
  "incident_date": "14 July",
  "system": "payroll system",
  "downtime_hours": 6,
  "employees_affected": 230,
  "estimated_cost": 40000,
  "status": "closed"
}

## Conclusion

This assignment showed me that prompt chaining makes complex tasks easier, but important information can be lost between steps. Preserving numbers and dates in the summary ensures that the final extraction contains all required information.