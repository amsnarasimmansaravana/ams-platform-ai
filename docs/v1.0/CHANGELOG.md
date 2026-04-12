# Changelog

## AMS-AI: Multi-Agent Orchestration Platform

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `10-LLM-AGENT-OPERATIONS.md` — LLMOps and AgentOps capability matrix, requirements (OPS-AGT-*, OPS-LLM-*), and diagram references
- Documentation navigation refresh in `docs/README.md` (full tree: `context/`, `diagrams/`, master context files)
- Cross-links from `COMPLETE-PRODUCT-CONTEXT.md`, `CONTEXT-FILE-INDEX.md`, and `context/*` master documents to the operations spec

### Changed
- `06-GLOSSARY.md` — entries for **AgentOps** and **LLMOps**
- `09-A2A-PROTOCOL-SPECIFICATION.md` — removed duplicate §2.1 heading

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## [0.1.0] - TBD (Planned)

### Planned Features
- Core package structure
- Agent entity model and CRUD operations
- Tool entity model and CRUD operations
- LLM provider adapters (OpenAI, Anthropic)
- Basic agent execution
- SQLite storage (development)
- CLI for agent and tool management
- Basic configuration system
- Logging infrastructure

---

## [0.2.0] - TBD (Planned)

### Planned Features
- Workflow entity model
- Node types (Agent, Tool, Control)
- Orchestration patterns (sequential, parallel, conditional)
- Workflow validation
- Workflow execution engine
- REST API (FastAPI)
- PostgreSQL integration
- API authentication (API keys)
- YAML workflow definition
- Python SDK (basic)

---

## [0.3.0] - TBD (Planned)

### Planned Features
- Web application (React)
- Desktop application (Tauri)
- Visual workflow builder
- Agent/Tool/Workflow management UI
- Execution monitoring UI
- Loop and Router patterns
- WebSocket real-time updates
- User authentication (JWT)
- Role-based access control
- Deployment management

---

## [1.0.0] - TBD (Planned)

### Planned Features
- Production hardening
- Horizontal scaling
- High availability
- Comprehensive monitoring
- Audit logging
- Secrets management
- Framework adapters (LangChain, AutoGen)
- Local model support (Ollama)
- Error recovery & retry
- Rate limiting
- Backup & restore
- Complete documentation

---

## Version History Summary

| Version | Status | Focus |
|---------|--------|-------|
| 0.1.0 | Planned | Core Engine & Agent Registry |
| 0.2.0 | Planned | Orchestration Builder & API |
| 0.3.0 | Planned | Desktop & Web Applications |
| 1.0.0 | Planned | Production Ready |
| 1.5.0 | Planned | Enterprise Features |
| 2.0.0 | Planned | Next Generation |

---

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | - | Initial changelog |
