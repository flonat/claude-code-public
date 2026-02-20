---
name: devils-advocate
description: "Challenge research assumptions and identify weaknesses in arguments. Stress-test papers before submission or revision."
argument-hint: [paper-or-argument-description]
---

# Devil's Advocate Skill

> Challenge research assumptions and identify weaknesses in your arguments.

## Purpose

Based on Scott Cunningham's Part 3: "Creating Devil's Advocate Agents for Tough Problems" - addressing the "LLM thing of over-confidence in diagnosing a problem."

**For formal code audits with replication scripts and referee reports, use the Referee 2 agent instead (`.claude/agents/referee2-reviewer.md`).** This skill is for quick adversarial feedback on arguments, not systematic audits.

## When to Use

- Before submitting a paper
- When stuck on a research problem
- When you want to stress-test an argument
- During paper revision planning

## When NOT to Use

- **Code audits** — use the Referee 2 agent instead
- **Replication verification** — use the Referee 2 agent instead
- **Quick proofreading** — just ask for a read-through
- **When you want validation** — this skill is designed to challenge, not affirm

## Workflow

1. **Understand the claim** - Read the paper/argument being evaluated
2. **Adopt adversarial stance** - Actively look for weaknesses
3. **Challenge on multiple dimensions**:
   - Theoretical assumptions
   - Methodological choices
   - Data limitations
   - Alternative explanations
   - Generalizability
4. **Provide constructive criticism** - Not just problems but potential solutions

## Prompt Template

```
I want you to act as a devil's advocate for my research. Your job is to find weaknesses, challenge assumptions, and identify what a hostile reviewer might say.

The paper/argument is: [DESCRIPTION]

Please critique it on:
1. **Theoretical foundations** - Are the assumptions justified?
2. **Methodology** - What are the limitations? Alternative approaches?
3. **Data** - Selection bias? Measurement issues? External validity?
4. **Causal claims** - Alternative explanations? Confounders?
5. **Contribution** - Is it novel enough? Does it matter?

Be harsh but constructive. For each criticism, suggest how it might be addressed.
```

## Example Use

"Play devil's advocate on my MCDM paper about preference drift - specifically challenge my identification strategy and the assumptions about utility functions."

---

## Cross-References

| Skill | When to use instead/alongside |
|-------|-------------------------------|
| `/interview-me` | To develop the idea further through structured interview |
| `/research-ideation` | To generate alternative research questions on the same topic |
| `/proofread` | For language/formatting review rather than argument critique |
