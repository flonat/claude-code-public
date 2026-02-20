---
name: research-ideation
description: "Generate structured research questions, testable hypotheses, and empirical strategies from a topic or dataset. Produces 3–5 ranked questions with identification strategies."
disable-model-invocation: true
argument-hint: "[topic, phenomenon, or dataset description]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
---

# Research Ideation

Generate structured research questions, testable hypotheses, and empirical strategies from a topic, phenomenon, or dataset.

**Input:** `$ARGUMENTS` — a topic (e.g., "AI-assisted decision-making in organisations"), a phenomenon (e.g., "why do managers resist algorithmic recommendations?"), or a dataset description (e.g., "panel of UK firms with AI adoption and productivity, 2018–2024").

---

## Before Starting

1. Read `.context/profile.md` to understand the researcher's areas and strengths.
2. Read `.context/projects/_index.md` to check for overlap with active projects.
3. If the topic relates to a specific project, read its context file.
4. Check existing bibliography files (`.bib`) in active projects for relevant references.

---

## Steps

1. **Understand the input.** Read `$ARGUMENTS` and any referenced files. Identify the domain: human-AI collaboration, MCDM, multi-agent systems, organisational behaviour, or other.

2. **Generate 3–5 research questions** ordered from descriptive to causal:
   - **Descriptive:** What are the patterns? (e.g., "How has X evolved over time?")
   - **Correlational:** What factors are associated? (e.g., "Is X correlated with Y after controlling for Z?")
   - **Causal:** What is the effect? (e.g., "What is the causal effect of X on Y?")
   - **Mechanism:** Why does the effect exist? (e.g., "Through what channel does X affect Y?")
   - **Policy/Design:** What are the implications? (e.g., "How should system X be designed to improve outcome Y?")

3. **For each research question, develop:**
   - **Hypothesis:** A testable prediction with expected sign/magnitude
   - **Identification/analytical strategy:** How to establish causality or build the argument (DiD, experiment, simulation, design science, RDD, IV, etc.)
   - **Data requirements:** What data would be needed? Is it available?
   - **Key assumptions:** What must hold for the strategy to be valid?
   - **Potential pitfalls:** Common threats and mitigations
   - **Related literature:** 2–3 papers using similar approaches (verify these exist)

4. **Rank the questions** by feasibility and contribution.

5. **Present the output** to the user. Save only if requested.

---

## Output Format

```markdown
# Research Ideation: [Topic]

**Date:** [YYYY-MM-DD]
**Input:** [Original input]

## Overview

[1–2 paragraphs situating the topic and why it matters]

## Research Questions

### RQ1: [Question] (Feasibility: High/Medium/Low)

**Type:** Descriptive / Correlational / Causal / Mechanism / Policy

**Hypothesis:** [Testable prediction]

**Identification Strategy:**
- **Method:** [e.g., Difference-in-Differences, online experiment, agent-based simulation]
- **Treatment:** [What varies and when]
- **Control group:** [Comparison units or baseline]
- **Key assumption:** [e.g., parallel trends, SUTVA, rationality]

**Data Requirements:**
- [Dataset 1 — what it provides]
- [Dataset 2 — what it provides]

**Potential Pitfalls:**
1. [Threat 1 and possible mitigation]
2. [Threat 2 and possible mitigation]

**Related Work:** [Author (Year)], [Author (Year)]

---

[Repeat for RQ2–RQ5]

## Ranking

| RQ | Feasibility | Contribution | Priority |
|----|-------------|-------------|----------|
| 1  | High        | Medium      | ...      |
| 2  | Medium      | High        | ...      |

## Suggested Next Steps

1. [Most promising direction and immediate action]
2. [Data to obtain or experiment to design]
3. [Literature to review deeper]
```

---

## Domain Adaptation

Adapt the identification strategies to the research area:

| Domain | Typical strategies |
|--------|-------------------|
| **Human-AI collaboration** | Online experiments, field experiments, survey experiments, computational modelling |
| **MCDM** | Simulation, axiomatic analysis, case studies, experimental validation |
| **Multi-agent systems** | Agent-based models, game-theoretic analysis, computational experiments |
| **Organisational behaviour** | Field experiments, quasi-experiments, longitudinal surveys, qualitative |
| **Environmental/carbon** | DiD, RDD, IV, synthetic control, structural estimation |

---

## Principles

- **Be creative but grounded.** Push beyond obvious questions, but every suggestion must be empirically feasible.
- **Think like a referee.** For each causal question, immediately identify the identification challenge.
- **Consider data availability.** A brilliant question with no available data is not actionable.
- **Suggest specific datasets** where possible (WRDS, UK Data Service, FRED, Prolific, MTurk, OpenAlex, etc.).
- **Use British English** throughout.

---

## Cross-References

| Skill | When to use instead/alongside |
|-------|-------------------------------|
| `/interview-me` | When you have a specific idea and want to develop it through conversation |
| `/devils-advocate` | To stress-test a chosen research question |
| `/literature` | To verify and expand the related work for a chosen RQ |
| `/literature` | To find papers using similar methods or on similar topics (includes OpenAlex API) |
