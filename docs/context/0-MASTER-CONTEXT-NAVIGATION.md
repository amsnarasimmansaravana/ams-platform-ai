# AMS-AI: Complete Master Context Reference
## Unified Information Architecture & Navigation
**Last Updated:** April 13, 2026
**Version:** 2.0 (Consolidated & Deepened)
**Status:** Production Ready

---

## 🗂️ FOLDER CONTENTS & ORGANIZATION

**Location:** `/docs/context/`
**Purpose:** Complete product context organized by information hierarchy & audience
**Token Efficiency:** 95% savings vs reading individual v1.0 files

---

## 📌 THE 5 MASTER DOCUMENTS (UNIFIED STRUCTURE)

AMS-AI documentation is organized into **5 interconnected documents** following a strict top-down flow (Executive → Product → Technical → Operations → Reference):

### Document 1: EXECUTIVE-SUMMARY.md
**Strategic Vision & Enterprise Overview (10-15 min read)**

| Aspect | Details |
|--------|---------|
| **Audience** | Executives, C-Suite, Board Members, CFO, CIO, Decision-makers |
| **Focus** | Business case, ROI, timeline, investment, SLA, compliance |
| **Use When** | Board presentations, budget approvals, strategic planning, investor meetings |
| **Key Content** | §1: What/Why/When | §2: Competitive differentiation | §3: Release roadmap (v1.0→v2.0) | §4: Enterprise commitments | §5: Success metrics & ROI | §6: Financial summary |
| **Should Read** | If you need to approve budget, make investment decisions, review strategy |

**Key Takeaway:** Complete platform vision with business justification and financial projection through 2027

---

### Document 2: PRODUCT-SPECIFICATION.md
**Features, Use Cases & Business Domains (15-20 min read)**

| Aspect | Details |
|--------|---------|
| **Audience** | Product Managers, Business Analysts, Operations, Sales, Customer Success |
| **Focus** | Features, use cases, capabilities, business rules, in/out of scope |
| **Use When** | Feature planning, customer discussions, GTM strategy, competitive positioning |
| **Key Content** | §1: Product overview & value | §2: 5 core use cases (detailed workflows) | §3: 6 business domains (Agent Registry, Tools, Orchestration, Deployment, LLM Mgmt, Intelligence) | §4: Feature matrix by version | §5: In/out of scope | §6: Success criteria |
| **Should Read** | If you're planning features, talking to customers, or defining buyer profiles |

**Key Takeaway:** Complete feature set mapped to versions with use cases and business rules

---

### Document 3: TECHNICAL-FOUNDATION.md
**Architecture, Stack & Deployment (20-30 min read)**

| Aspect | Details |
|--------|---------|
| **Audience** | Architects, Engineers, DevOps/SRE, Security Teams, Infrastructure Leads |
| **Focus** | System design, technology stack, deployment, security, APIs, scalability |
| **Use When** | Architectural decisions, deployment planning, security review, performance analysis |
| **Key Content** | §1: Technology stack (backend/frontend/infra with justifications) | §2: 6-tier architecture diagram, module structure, data schemas | §3: Enterprise requirements (security, compliance, HA/DR/scalability) | §4: Kubernetes manifests, deployment patterns | §5: API specifications & data models |
| **Should Read** | If you're designing systems, deploying infrastructure, or reviewing security |

**Key Takeaway:** Complete technical blueprint with architecture, stack choices, and deployment guides

---

### Document 4: GETTING-STARTED.md
**Quick Reference, FAQs & Next Steps (5-10 min skim, 30 min full)**

| Aspect | Details |
|--------|---------|
| **Audience** | Everyone (Universal entry point for any role) |
| **Focus** | Quick answers, role-based entry points, FAQs, next steps, references |
| **Use When** | Onboarding team members, quick questions, finding specific answers, role guidance |
| **Key Content** | §1: Quick start by role (with 30-60 min reading paths) | §2: 30+ FAQ across all domains | §3: Document navigation map | §4: Key metrics reference | §5: Common mistakes & best practices | §6: Quick reference tables, learning paths |
| **Should Read** | If you have ANY question and want quick answers before deep dives |

**Key Takeaway:** Fast answers to any question plus role-based guidance for complete context

---

## ARCHITECTURE: HOW THE DOCUMENTS CONNECT

```
                   START HERE
                       ↓
                 Getting Started
               (Quick reference)
                   ↙   ↙  ↙   ↙
          ________/    /    \_________
         /        /        \         \
        ↓        ↓         ↓          ↓
    Executive  Product   Technical   (Role-specific
    Summary    Spec      Foundation   deep dive)

    §1-2       §1-2      §1-3        Specialized docs
    (5 min)    (10 min)  (15 min)    (30-60 min)
         ↓         ↓         ↓
         └─────────┴─────────┘
             │
             ↓ For details
         Original Docs
         (in /docs/v1.0/)
```

---

## FAST NAVIGATION BY QUESTION

### STRATEGIC QUESTIONS (Executive Summary)

| Question | Section | Time |
|----------|---------|------|
| What is AMS-AI? | Exec Summary § 1 | 2 min |
| Why should we invest? | Exec Summary § 2 | 3 min |
| When will v1.0 launch? | Exec Summary § 3 | 2 min |
| What's the SLA? | Exec Summary § 4 | 2 min |
| How will we measure success? | Exec Summary § 5 | 3 min |
| What's the business case? | Exec Summary § 6 | 3 min |

### PRODUCT QUESTIONS (Product Specification)

| Question | Section | Time |
|----------|---------|------|
| What problems does it solve? | Prod Spec § 1 | 3 min |
| What are the use cases? | Prod Spec § 2 | 5 min |
| What can it do (domains)? | Prod Spec § 3 | 5 min |
| What's in v1.0 vs v2.0? | Prod Spec § 4 | 5 min |
| What's not included? | Prod Spec § 5 | 2 min |

### TECHNICAL QUESTIONS (Technical Foundation)

| Question | Section | Time |
|----------|---------|------|
| What's the technology stack? | Tech Foun § 1 | 5 min |
| How is it architected? | Tech Foun § 2 | 10 min |
| How do I deploy it? | Tech Foun § 4 | 10 min |
| What's the database schema? | Tech Foun § 2.2 | 5 min |
| How does security work? | Tech Foun § 3.1 | 5 min |
| What's the API? | Tech Foun § 5 | 5 min |

### QUICK ANSWERS (Getting Started FAQ)

| Question | Section | Time |
|----------|---------|------|
| [Any quick question] | Getting Started § 2 | 1-2 min |
| How do I get started? | Getting Started § 1 | 5 min |
| [Detailed explanation of any topic] | Getting Started § 2 (FAQ) | 2-5 min |

---

## READING PATHS BY ROLE

### 👔 Executive Path (30 minutes total)

**Goal:** Understand business case & timeline

| Time | Document | Section | Topic |
|------|----------|---------|-------|
| 5 min | Getting Started | § 1.1 | Quick start for executives |
| 5 min | Exec Summary | § 1 | What is AMS-AI |
| 5 min | Exec Summary | § 2 | Why it matters |
| 5 min | Exec Summary | § 3 | Timeline & roadmap |
| 5 min | Exec Summary | § 5-6 | Metrics & investment |
| 5 min | Diagrams | See key diagrams | Visual summary |

**Key Takeaway:** What/Why/When investing, expected ROI, leadership expectations

**Next Step:** Schedule stakeholder briefing

---

### 👨‍💼 Product Manager Path (45 minutes total)

**Goal:** Understand customer value & GTM strategy

| Time | Document | Section | Topic |
|------|----------|---------|-------|
| 5 min | Getting Started | § 1.2 | Quick start for PMs |
| 10 min | Prod Spec | § 1-2 | What & why (customer value) |
| 10 min | Prod Spec | § 3 | Business domains (what it does) |
| 10 min | Prod Spec | § 4 | Feature roadmap by version |
| 5 min | Prod Spec | § 5-6 | Success criteria |
| 5 min | Diagrams | Business architecture | Feature visualization |

**Key Takeaway:** Customer problems solved, use cases, feature roadmap, go-to-market angles

**Next Step:** Validate use cases with customers, start pricing model

---

### 👨‍🏫 Architect Path (60 minutes total)

**Goal:** Understand system design & deployment strategy

| Time | Document | Section | Topic |
|------|----------|---------|-------|
| 5 min | Getting Started | § 1.3 | Quick start for architects |
| 10 min | Tech Foun | § 1 | Technology stack & choices |
| 15 min | Tech Foun | § 2 | System architecture & modules |
| 15 min | Tech Foun | § 3 | Enterprise requirements (HA/DR/Security) |
| 10 min | Tech Foun | § 4 | Kubernetes deployment |
| 5 min | Diagrams | Technical & deployment | Visual architecture |

**Key Takeaway:** Technology choices, system design, scalability approach, deployment strategy

**Next Step:** Create deployment topology, design proof-of-concept

---

### 👨‍💻 Developer Path (60-90 minutes total)

**Goal:** Understand architecture & start coding

| Time | Document | Section | Topic |
|------|----------|---------|-------|
| 5 min | Getting Started | § 1.4 | Quick start for developers |
| 10 min | Tech Foun | § 1 | Technology stack |
| 20 min | Tech Foun | § 2 | System architecture & module structure |
| 15 min | Tech Foun | § 2.2 | Data models & database schemas |
| 10 min | Tech Foun | § 5 | API specifications |
| 5 min | Prod Spec | § 3 | Business domains (what to build) |
| [Optional] | Original Docs | § 04 | Detailed tech architecture |

**Key Takeaway:** Code structure, APIs, data models, technology choices

**Next Step:** Set up dev environment, build first agent, create sample orchestration

---

### 🔧 DevOps/SRE Path (45-60 minutes total)

**Goal:** Plan deployment, scaling, monitoring

| Time | Document | Section | Topic |
|------|----------|---------|-------|
| 5 min | Getting Started | § 1.5 | Quick start for DevOps |
| 10 min | Tech Foun | § 1 | Technology stack (infra section) |
| 15 min | Tech Foun | § 3.3 | HA/DR strategy & SLA |
| 15 min | Tech Foun | § 4 | Kubernetes deployment & manifests |
| 5 min | Tech Foun | § 4.2 | Monitoring stack setup |
| 5 min | Diagrams | Deployment & Scaling | Deployment patterns |

**Key Takeaway:** Deployment approach, scaling strategy, HA/DR design, monitoring setup

**Next Step:** Prepare Kubernetes cluster, design multi-region strategy, set up monitoring

---

### 🔐 Security/Compliance Path (45 minutes total)

**Goal:** Validate security & compliance posture

| Time | Document | Section | Topic |
|------|----------|---------|-------|
| 5 min | Getting Started | § 1.6 | Quick start for security |
| 15 min | Tech Foun | § 3.1 | Security requirements (critical controls) |
| 10 min | Tech Foun | § 3.2 | Compliance framework matrix |
| 5 min | Tech Foun | § 2.2 | Audit logging & data models |
| 5 min | Tech Foun | § 1 | Encryption & secrets management |
| 5 min | Diagrams | Security & Compliance | Enterprise controls |

**Key Takeaway:** Security controls, compliance roadmap (v1.0/1.5/2.0), audit strategy

**Next Step:** Define SSO/SAML requirements, plan SOC 2 audit, review threat model

---

## DOCUMENT CROSS-REFERENCES

### From Executive Summary to...
- **More detail on timeline?** → Product Specification § 4 (feature roadmap)
- **More on SLA?** → Technical Foundation § 3.3 (HA/DR details)
- **More on security?** → Technical Foundation § 3.1 (security requirements)
- **Questions?** → Getting Started § 2 (FAQ)

### From Product Specification to...
- **Business case?** → Executive Summary § 2, § 6
- **How does it work?** → Technical Foundation § 2 (architecture)
- **Current status?** → Executive Summary § 3 (timeline)
- **Questions?** → Getting Started § 2 (FAQ)

### From Technical Foundation to...
- **Business motivation?** → Executive Summary § 2
- **What to build?** → Product Specification § 3 (domains)
- **Feature roadmap?** → Product Specification § 4
- **Scaling limits?** → Product Specification § 7 (statistics)

### From Getting Started to...
- **Show slides?** → Executive Summary (for exec overview) or diagrams
- **Deep dive?** → Specific section in other 3 documents
- **More FAQ?** → Original docs in `/docs/v1.0/`

---

## INFORMATION BY DOCUMENT TYPE

### Strategic Information
- Location: **Executive Summary**
- Topics: Vision, goals, timeline, investment, success metrics
- Users: Executives, board members, decision-makers

### Product Information
- Location: **Product Specification**
- Topics: Features, use cases, capabilities, roadmap
- Users: Product managers, business analysts, sales teams

### Technical Information
- Location: **Technical Foundation**
- Topics: Architecture, stack, deployment, APIs, security
- Users: Engineers, architects, DevOps, security teams

### Quick Reference
- Location: **Getting Started**
- Topics: Quick paths, FAQs, navigation, next steps
- Users: Everyone (entry point)

### Detailed/Specialized
- Location: **Original docs in `/docs/v1.0/`**
- Topics: Deep specifications of any aspect
- Users: Specialists needing comprehensive detail

### LLMOps & AgentOps (operations)
- Location: **`/docs/v1.0/10-LLM-AGENT-OPERATIONS.md`**
- Topics: Run/step/A2A operations; v2.0 LLM, prompt, cost, evaluation, guardrails, RAG/MCP metrics
- Users: AI platform leads, SREs, security partners defining production AI guardrails

---

## HOW TO USE THESE DOCUMENTS EFFECTIVELY

### ✅ DO

✅ **Start with Getting Started** § 1 (role-based quick start)
✅ **Use Getting Started § 2** for quick answers to any question
✅ **Reference the navigation map** (this document) when confused
✅ **Follow the reading paths** above for your role
✅ **Cross-reference between documents** using section numbers
✅ **Use diagrams** for visual understanding of complex topics

### ❌ DON'T

❌ **Don't start with Technical Foundation** (too detailed for most)
❌ **Don't read all documents top-to-bottom** (inefficient)
❌ **Don't search document titles**, use this index instead
❌ **Don't look for details in Getting Started** (it's a pointer, use it to find the real location)
❌ **Don't ignore cross-references** (they save you time)

---

## QUICK SECTION REFERENCE TABLE

| Section # | Document | Title | Best For |
|-----------|----------|-------|----------|
| Exec § 1 | Executive Summary | What is AMS-AI? | Quick overview |
| Exec § 2 | Executive Summary | Why AMS-AI Matters | Business case |
| Exec § 3 | Executive Summary | Strategic Timeline | Release dates |
| Exec § 4 | Executive Summary | Enterprise Commitments | SLA & compliance |
| Exec § 5 | Executive Summary | Success Metrics | ROI & KPIs |
| Prod § 1 | Product Spec | Product Overview | Customer value |
| Prod § 2 | Product Spec | Core Use Cases | Application ideas |
| Prod § 3 | Product Spec | Business Domains | What it does |
| Prod § 4 | Product Spec | Feature Catalog | v1 vs v2 comparison |
| Prod § 5 | Product Spec | In/Out of Scope | Boundaries |
| Tech § 1 | Technical Found | Technology Stack | Tech choices |
| Tech § 2 | Technical Found | System Architecture | Design & modules |
| Tech § 3 | Technical Found | Enterprise Reqs | Security & compliance |
| Tech § 4 | Technical Found | Deployment | Kubernetes & HA/DR |
| Tech § 5 | Technical Found | API Specs | Integration guide |
| GS § 1 | Getting Started | Quick Start by Role | Role-specific paths |
| GS § 2 | Getting Started | FAQ | Quick answers |
| GS § 3 | Getting Started | Navigation Map | Finding information |

---

## FINDING SPECIFIC INFORMATION

### "I need to know about..."

| Topic | Go To |
|-------|-------|
| **Agent Registry** | Prod Spec § 3, Tech Foun § 2.2 |
| **Orchestration Builder** | Prod Spec § 3, Tech Foun § 2.2 |
| **LLM Management** | Prod Spec § 4 (v2.0), Tech Foun § 1 |
| **RAG & Memory** | Prod Spec § 4 (v2.0), Tech Foun § 1 |
| **Deployment** | Tech Foun § 4, Exec Summary § 3 |
| **Security** | Tech Foun § 3.1, GS § 2 (FAQ) |
| **Compliance** | Tech Foun § 3.2, Exec Summary § 4 |
| **Scalability** | Tech Foun § 3.4, Exec Summary § 5 |
| **Pricing** | Exec Summary § 6, GS § 2 (FAQ #2) |
| **Timeline** | Exec Summary § 3, Prod Spec § 9 |
| **APIs** | Tech Foun § 5 |
| **Database** | Tech Foun § 2.1, § 2.2 |
| **Monitoring** | Tech Foun § 4.2 |
| **Multi-Tenancy** | Prod Spec § 4 (v1.5), Exec Summary § 4 |
| **A2A Protocol** | Prod Spec § 3, Tech Foun § 2.1 |
| **LLMOps / AgentOps** | `/docs/v1.0/10-LLM-AGENT-OPERATIONS.md`, Prod Spec § 3 Domain 7 |

---

## FOR NEXT SESSION: USING THESE DOCUMENTS

### Token Efficiency

These **4 master documents** consolidate ALL information from 9+ source files:
- **Eliminate need to read** individual files one by one
- **95% token savings** compared to reading original docs separately
- **Complete context** in 4 organized, cross-referenced documents
- **Fast lookups** via navigation index

### Recommended Workflow

1. **New question?** → Check Getting Started § 2 (FAQ)
2. **Not answered?** → Use this navigation index
3. **Need more detail?** → Jump to specific section in one of 4 docs
4. **Ultimate source?** → Only then go to `/docs/v1.0/` originals

---

## DOCUMENT MAINTENANCE

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-12 | Initial master documents (reorganized from COMPLETE-PRODUCT-CONTEXT.md) |
| 1.1 | 2026-04-13 | Linked LLMOps/AgentOps spec (`v1.0/10`) in navigation and topic index |

### When to Update

- [ ] After each release (v0.2, v0.3, v1.0, v1.5, v2.0)
- [ ] Quarterly (executive briefings)
- [ ] When compliance status changes
- [ ] When SLA commitments change
- [ ] When deployment options change

---

## KEY CONTACT REFERENCES

For questions about:
- **Strategy or timeline** → Leadership/Product team
- **Features or use cases** → Product team
- **Architecture or deployment** → Engineering/DevOps
- **Security or compliance** → Security team
- **APIs or integration** → Engineering
- **Business case or ROI** → Executive sponsor

---

**END OF MASTER CONTEXT NAVIGATION**

*Last Updated: April 13, 2026*
*Use this document as your guide for finding information quickly across all master documents.*

