# AI Code Reviewer & Debugger — Design

## Overview

A Python-based code review tool that detects potential bugs using static analysis and, in future versions, LLM-powered reasoning.

## Tech Stack

- **Python** — Core implementation
- **AST** — Source-code parsing and deterministic analysis
- **Pydantic** — Structured data validation
- **pytest** — Automated testing
- **Planned:** Ruff, Bandit, FastAPI, LLM integration, LangGraph

## Architecture

```text
Python Source
     ↓
Input Validation
     ↓
AST Parsing
     ↓
Bug Detection
     ↓
Constant Expression Evaluation
     ↓
Structured Findings
```

## Current Features

- Handles empty input and Python syntax errors.
- Detects division-by-zero expressions, including supported arithmetic and unary expressions.
- Returns structured findings with severity, confidence, line number, explanation, impact, suggested fix, source, and status.
- Uses Pydantic models for validation.
- Includes automated tests for valid inputs, errors, and detection edge cases.
- Analyzes source code without executing it.

## Project Structure

```text
AI-Code-Reviewer-and-Debugger/
├── README.md
├── design.md
├── requirements.txt
├── code_reviewer/
│   ├── __init__.py
│   ├── analyser.py
│   ├── result.py
│   └── schemas.py
└── tests/
    └── test_analyzer.py
```

## Design Principles

- Prefer deterministic analysis before introducing LLMs.
- Keep analysis, schemas, and results modular.
- Evaluate only explicitly supported expressions.
- Validate behavior through automated tests.
- Never execute submitted code to detect bugs.

## Roadmap

1. Improve AST detection and edge-case handling.
2. Integrate Ruff and Bandit.
3. Add LLM-powered code review and structured output validation.
4. Merge duplicate findings while preserving their sources.
5. Expose the reviewer through FastAPI.
6. Introduce LangGraph when workflow orchestration becomes necessary.
7. Add evaluation metrics, logging, and CI/CD.

## Current Status

The deterministic baseline is implemented, with AST-based division-by-zero detection, constant-expression evaluation, structured results, and passing tests. The next priority is improving detection coverage before adding external tools and LLM integration.
