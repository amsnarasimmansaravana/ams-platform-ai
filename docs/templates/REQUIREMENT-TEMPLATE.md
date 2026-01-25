# Requirement Template

## AMS-AI: Multi-Agent Orchestration Platform

Use this template when adding new requirements to the documentation.

---

## Functional Requirement Template

```markdown
#### FR-XX-NNN: [Requirement Title]

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-XX-NNN |
| **Title** | [Short descriptive title] |
| **Priority** | Critical \| High \| Medium \| Low |
| **Description** | [Detailed description of the requirement] |

**Input Parameters:** (if applicable)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| field_name | type | Yes/No | Description |

**Business Rules:** (if applicable)
- Rule 1
- Rule 2

**Preconditions:** (if applicable)
- Condition 1
- Condition 2

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

---

## Business Rule Template

```markdown
| ID | Rule | Description |
|----|------|-------------|
| BR-XX-NNN | [Rule Name] | [Rule description] |
```

---

## Feature Template (for Roadmap)

```markdown
| ID | Feature | Priority | Status |
|----|---------|----------|--------|
| F-X.Y-NNN | [Feature name] | Critical \| High \| Medium \| Low | Planned \| In Progress \| Complete |
```

---

## API Endpoint Template

```markdown
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST/PUT/DELETE | /api/v1/resource | [Description] |
```

---

## ID Conventions

### Requirement IDs

| Prefix | Domain |
|--------|--------|
| FR-AR | Agent Registry |
| FR-TR | Tool Registry |
| FR-OB | Orchestration Builder |
| FR-DM | Deployment & Management |
| FR-PF | Platform Features |

### Business Rule IDs

| Prefix | Domain |
|--------|--------|
| BR-AR | Agent Registry |
| BR-TR | Tool Registry |
| BR-OB | Orchestration Builder |
| BR-DM | Deployment & Management |

### Feature IDs

Format: `F-{version}-{number}`
Example: `F-0.2-005`

---

## Priority Definitions

| Priority | Description |
|----------|-------------|
| **Critical** | Must have for release, blocks other work |
| **High** | Important for release, significant value |
| **Medium** | Nice to have, can be deferred |
| **Low** | Future consideration |

---

## Status Definitions

| Status | Description |
|--------|-------------|
| **Planned** | Scheduled for implementation |
| **In Progress** | Currently being developed |
| **In Review** | Code complete, under review |
| **Complete** | Implemented and tested |
| **Deferred** | Postponed to future release |
| **Cancelled** | Will not be implemented |
