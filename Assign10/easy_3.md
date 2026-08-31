# AI Hallucination, Confidence vs Accuracy

## Objective

The objective of this assignment is to understand that a confident-sounding AI answer is not always a correct answer.

The experiment tests the AI using common factual questions and trap questions designed to trigger hallucinations.

## Five Test Questions

| # | Question | Answer (Short Summary) | Confidence | Correctness |
|---|---|---|---|---|
| 1 | What is the capital of France? | The capital of France is Paris. | High | Correct |
| 2 | How many days are there in a leap year? | A leap year has 366 days. | High | Correct |
| 3 | Who won the 2035 Cricket World Cup? | The AI provided a specific team as the winner and described the final match. | High | Wrong |
| 4 | Who wrote the book The Midnight Algorithm of Jaipur? | The AI provided a specific author and additional details about the book. | High | Wrong |
| 5 | What is our company's Article 7 leave policy? | The AI gave a detailed description of an Article 7 leave policy even though no such company document was provided. | High | Wrong |

## Observations

The future-event trap produced a hallucination because the event has not happened yet, but the model still generated a confident-sounding answer.

The invented book question also produced a hallucination because the model generated a likely-sounding author and additional details for something that was not established as real.

The fake internal company policy produced another hallucination because the model had no company document containing Article 7, but it still attempted to provide an answer.

These examples show that an LLM predicts likely text based on patterns it has learned; it does not automatically verify whether every fact it produces is true.

## Confidence vs Accuracy

Confidence refers to how certain the answer sounds.

Accuracy refers to whether the information in the answer is actually correct.

An answer can sound very confident while still being completely wrong.

For example, an answer about a future event may sound very confident and contain specific details, but those details cannot be treated as verified facts.

## Extension: Mitigation

One trap question can be re-asked with an additional instruction:

> If you do not know the answer or the event has not happened, say "I don't know". Do not guess or invent information.

For example:

**Question:** Who won the 2035 Cricket World Cup?

**Improved response:** I don't know. The 2035 Cricket World Cup has not happened yet, so there is no verified winner.

This instruction encourages the model to avoid guessing when information is unknown or cannot be verified.

## Conclusion

The experiment demonstrates that confidence in an AI's tone does not guarantee accuracy of its facts.

## Impact on AI Knowledge Assistant

The AI Knowledge Assistant must ground its answers in company documents and use validation rather than blindly trusting confident-sounding LLM responses.