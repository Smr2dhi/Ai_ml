# LLM Hallucination Test

## Run 1

- **Invented details:** No
- **Sounded confident:** No, it was cautious
- **Warned about uncertainty:** Yes

## Run 2

- The constraint made the model more cautious.
- It avoided inventing leave-policy details.

## Observations

1. Run 1 did not hallucinate and clearly stated its limitation.
2. Run 2 further reduced the chance of hallucination.
3. Constraints can reduce hallucinations but cannot completely eliminate them.

## Why did hallucination happen?

An LLM predicts likely text from learned patterns rather than automatically looking up and verifying facts.