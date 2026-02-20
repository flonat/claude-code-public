# Conference Rankings Reference

> Global reference for targeting conference venues. When choosing a conference, aim for **CORE A* or A** wherever possible.

Last verified: February 2026
CORE Portal: https://portal.core.edu.au/conf-ranks/

## Ranking System

| System | Source | Notes |
|--------|--------|-------|
| **CORE** | Computing Research and Education Association of Australasia | A*, A, B, C scale; most widely used for CS/IS conferences |

Unlike journals (ranked by CABS AJG), conferences are primarily ranked by the **CORE system**. CORE rankings are updated periodically; always check the portal for the latest.

| Tier | CORE | Meaning |
|------|------|---------|
| Tier 1 | A* | Flagship venue — top of field, highly selective (<20% acceptance) |
| Tier 2 | A | Excellent venue — strong reputation, competitive (<25% acceptance) |
| Tier 3 | B | Good venue — solid but less competitive |
| Tier 4 | C | Acceptable venue — regional or niche |

---

## Tier 1 — CORE A*

Top-tier venues with high selectivity. Equivalent stature to CABS 4*/4 journals.

| Conference | Acronym | Field | Typical deadline | Format |
|-----------|---------|-------|-----------------|--------|
| Neural Information Processing Systems | NeurIPS | ML/AI | May | 9 pages + refs |
| International Conference on Machine Learning | ICML | ML | Jan–Feb | 8 pages + refs |
| AAAI Conference on Artificial Intelligence | AAAI | AI | Aug | 7 pages + refs |
| International Joint Conference on AI | IJCAI | AI | Jan | 7 pages + refs |
| Autonomous Agents and Multi-Agent Systems | AAMAS | MAS | Oct | 8 pages + refs |
| ACM Conference on Economics and Computation | ACM EC | Comp Econ | Feb | 15–20 pages |
| Knowledge Discovery and Data Mining | KDD | Data Mining | Feb | 9 pages |
| ACM Conference on Human Factors in Computing | CHI | HCI | Sep | 10 pages + refs |

---

## Tier 2 — CORE A

Excellent venues with strong reputations.

| Conference | Acronym | Field | Typical deadline | Format |
|-----------|---------|-------|-----------------|--------|
| AAAI/ACM Conference on AI, Ethics, and Society | AIES | AI Ethics | Feb | 10 pages + refs |
| ACM Conference on Fairness, Accountability, and Transparency | FAccT | Responsible AI | Jan | 10 pages + refs |
| Genetic and Evolutionary Computation Conference | GECCO | Evolutionary Comp | Feb | 8 pages + refs |
| International Conference on Learning Representations | ICLR | ML | Sep–Oct | 10 pages + refs |
| Computer Supported Cooperative Work | CSCW | Social Computing | Various | 25 pages (journal-style) |
| Workshop on Internet and Network Economics | WINE | Comp Econ | Jun–Jul | 15 pages |

---

## Tier 3 — CORE B

Good venues, often more specialist or regional.

| Conference | Acronym | Field | Typical deadline | Format |
|-----------|---------|-------|-----------------|--------|
| Evolutionary Multi-Criterion Optimization | EMO | MCDM/EMO | Oct | 15 pages |
| International Conference on MCDM | MCDM | MCDM | Varies (biennial) | Extended abstract + paper |
| International Conference on Group Decision and Negotiation | GDN | Group Decision | Feb–Mar | 12 pages |
| International Conference on Human-Agent Interaction | HHAI | Human-AI | Varies | 8 pages |

---

## Relevant Conferences

Conferences from the lists above most relevant to the research programme:

| Conference | CORE | Primary fit |
|-----------|------|-------------|
| AAMAS | A* | Multi-agent systems, mechanism design |
| ACM EC | A* | Computational economics, preference elicitation |
| CHI | A* | Human-AI interaction, decision support interfaces |
| NeurIPS | A* | ML methods, human-AI collaboration |
| ICML | A* | ML methods, learning algorithms |
| AIES | A | AI ethics, societal impact of AI-assisted decisions |
| FAccT | A | Fairness in algorithmic decision-making |
| GECCO | A | Evolutionary multi-objective optimisation |
| ICLR | A | Representation learning, ML methods |
| CSCW | A | Collaborative decision-making, group dynamics |
| EMO | B | Multi-criteria optimisation, Pareto methods |
| MCDM | B | Core MCDM community, preference modelling |
| GDN | B | Group decision processes, negotiation |

**Not CORE-ranked but commonly targeted:**

| Conference | Notes |
|-----------|-------|
| HCOMP (Human Computation) | AAAI symposium; human-AI task design |
| EC Workshop tracks | Mechanism design, market design workshops |
| NeurIPS/ICML Workshop tracks | Lower barrier, good for early-stage ideas |

---

## Conference Metadata Template

When targeting a conference in `/init-project-research`, capture:

```markdown
## Conference Target
- **Conference:** <full name> (<acronym>)
- **CORE ranking:** <A*/A/B/C>
- **Submission deadline:** <date>
- **Notification date:** <date>
- **Camera-ready date:** <date>
- **Conference dates:** <dates>
- **Location:** <city, country>
- **Page limit:** <N pages + refs>
- **Format:** <LaTeX template / style file>
- **Review type:** <double-blind / single-blind / open>
- **Anonymisation required:** <yes/no>
- **CfP link:** <URL>
```
