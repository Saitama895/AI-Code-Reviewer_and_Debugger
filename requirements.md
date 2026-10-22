# AI Code Reviewer — Requirements Draft

## 1. Objective

Build an AI-powered Python code reviewer that identifies potential bugs, explains their impact, and suggests fixes.

## 2. Input

- Accept one Python source file as text.
- Reject empty or invalid input.
- Do not execute submitted code in the initial version.

## 3. Finding Schema

Each finding must contain:

- `title`: Short description of the issue.
- `severity`: Low, medium, high, or critical.
- `confidence`: Low, medium, or high.
- `line_number`: Relevant source line, when identifiable.
- `explanation`: Why the issue occurs.
- `impact`: What could break.
- `suggested_fix`: A proposed correction.
- `source`: Static analyzer or LLM.
- `status`: Initial assessment of the finding.

## 4. Expected Behavior

### Case 1: Obvious bug

Input contains a clear programming error.

Expected behavior:

- Identify the issue if detectable.
- Explain its impact and suggest a fix.
- Include the relevant line number when available.

### Case 2: Clean code

Input contains no known bugs.

Expected behavior:

- Return an empty findings list if no issues are identified.
- Do not invent bugs to produce a non-empty response.

### Case 3: LLM identifies a bug missed by static analysis

Expected behavior:

- Preserve the LLM finding for review.
- Record its source and supporting reasoning.
- Do not mark it confirmed without sufficient evidence.

### Case 4: Malformed LLM output

Expected behavior:

- Attempt a bounded recovery or retry when appropriate.
- Validate the output before accepting it.
- Return a clear failure status if recovery fails.

### Case 5: Invalid Python syntax

Expected behavior:

- Report a syntax error with its location when available.
- Do not continue normal semantic review if parsing fails.
- Return an actionable error message.

## 5. Non-Functional Requirements

- Validate all inputs and model outputs.
- Handle model timeouts and API failures.
- Keep logs useful for debugging without exposing secrets.
- Ensure the same input can be tested reproducibly.

## 6. Out of Scope for MVP

- GitHub integration.
- Multi-file repository analysis.
- Automatic application of fixes.
- Execution of untrusted source code.

## 7. Open Questions

- How should duplicate findings from different sources be combined?
- What evidence is sufficient to classify a finding as likely or confirmed?
- How should the application behave when the LLM is unavailable?
