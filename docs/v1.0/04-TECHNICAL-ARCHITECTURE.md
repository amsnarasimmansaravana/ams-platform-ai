# Technical Architecture Document

## AMS-AI: Multi-Agent Orchestration Platform

**Document Version:** 1.0
**Last Updated:** 2026-04-12
**Status:** Complete Architecture Specification with Deployment Patterns

---

## Executive Summary

This document provides the complete technical architecture of AMS-AI platform v1.0, covering:

1. **System Architecture** - 6-tier layered design, component interactions, data flows
2. **Technology Stack** - Backend, frontend, database, infrastructure selections with justifications
3. **Module Structure** - Detailed Python package organization, service boundaries, API contracts
4. **Deployment Architecture** - Kubernetes specs, containerization, scaling patterns
5. **Integration Patterns** - A2A protocol implementation, adapter framework, extensibility hooks
6. **DevOps & Infrastructure** - CI/CD pipeline, monitoring, observability, secrets management

**Target Audience:** Architects, Tech Leads, Senior Engineers, DevOps Teams

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Web App   │    │ Desktop App │    │     CLI     │    │  Python SDK │  │
│  │   (React)   │    │   (Tauri)   │    │   (Click)   │    │             │  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
└─────────┼──────────────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │                  │
          └──────────────────┴────────┬─────────┴──────────────────┘
                                      │
                              ┌───────▼───────┐
                              │   API Gateway │
                              │    (FastAPI)  │
                              └───────┬───────┘
                                      │
┌─────────────────────────────────────┼─────────────────────────────────────┐
│                              SERVICE LAYER                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  Agent Service  │    │  Orchestration  │    │   Deployment    │        │
│  │                 │    │    Service      │    │    Service      │        │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘        │
│           │                      │                      │                  │
│  ┌────────┴────────┐    ┌────────┴────────┐    ┌────────┴────────┐        │
│  │  Tool Service   │    │ Workflow Engine │    │ Execution Engine│        │
│  │                 │    │                 │    │                 │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                            ADAPTER LAYER                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   OpenAI    │    │  Anthropic  │    │   LangChain │    │   AutoGen   │ │
│  │   Adapter   │    │   Adapter   │    │   Adapter   │    │   Adapter   │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                         INFRASTRUCTURE LAYER                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  PostgreSQL │    │    Redis    │    │   MinIO/S3  │    │   Celery    │ │
│  │  (Primary)  │    │   (Cache)   │    │  (Storage)  │    │  (Workers)  │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
└───────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles

| Principle | Description |
|-----------|-------------|
| **Modularity** | Loosely coupled components with clear boundaries |
| **Framework Agnostic** | Core logic independent of specific AI frameworks |
| **Extensibility** | Plugin architecture for adapters and extensions |
| **Scalability** | Horizontal scaling support for all components |
| **Portability** | Cross-platform support with containerization |

---

## 2. Technology Stack

### 2.1 Core Technologies

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Language** | Python 3.11+ | User requirement, rich AI ecosystem |
| **API Framework** | FastAPI | Async support, OpenAPI, performance |
| **Task Queue** | Celery + Redis | Distributed task processing |
| **Database** | PostgreSQL | ACID compliance, JSON support |
| **Cache** | Redis | Session, cache, pub/sub |
| **Object Storage** | MinIO / S3 | File storage, logs |
| **Search** | PostgreSQL FTS / Meilisearch | Full-text search |

### 2.2 Frontend Technologies

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Web Framework** | React 18+ | Large ecosystem, TypeScript support |
| **State Management** | Zustand / Redux Toolkit | Lightweight, scalable |
| **UI Components** | Shadcn/ui + Tailwind | Modern, customizable |
| **Workflow Canvas** | React Flow | Visual workflow builder |
| **Desktop** | Tauri | Lightweight, native performance |

### 2.3 DevOps & Infrastructure

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Containerization** | Docker | Consistent environments |
| **Orchestration** | Docker Compose / Kubernetes | Deployment flexibility |
| **CI/CD** | GitHub Actions | Automation |
| **Monitoring** | Prometheus + Grafana | Metrics and dashboards |
| **Logging** | Loki / ELK | Centralized logging |

---

## 3. Component Design

### 3.1 Core Module Structure

```
core/
├── __init__.py
├── config.py                    # Configuration management
├── exceptions.py                # Custom exceptions
│
├── a2a/                         # A2A Protocol Implementation
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent_card.py       # A2A Agent Card model
│   │   ├── task.py             # A2A Task model
│   │   ├── message.py          # A2A Message model
│   │   └── skill.py            # A2A Skill model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── card_service.py     # Agent Card generation/validation
│   │   ├── task_service.py     # A2A Task lifecycle
│   │   ├── discovery_service.py # Agent discovery
│   │   └── communication.py    # Inter-agent communication
│   ├── endpoints/
│   │   ├── __init__.py
│   │   ├── well_known.py       # /.well-known/agent.json
│   │   ├── tasks.py            # /a2a/tasks endpoints
│   │   └── streaming.py        # SSE streaming
│   ├── client/
│   │   ├── __init__.py
│   │   ├── a2a_client.py       # Client for external A2A agents
│   │   └── connection_pool.py  # Connection management
│   └── schemas/
│       ├── __init__.py
│       ├── agent_card_schema.py
│       └── task_schemas.py
│
├── registry/                    # Agent & Tool Registry
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent.py            # Agent entity (A2A-enhanced)
│   │   ├── tool.py             # Tool entity
│   │   └── capability.py       # Capability definitions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py    # Agent CRUD + A2A onboarding
│   │   ├── tool_service.py     # Tool CRUD operations
│   │   ├── discovery.py        # Capability discovery
│   │   └── external_agent.py   # External A2A agent management
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── agent_repository.py
│   │   └── tool_repository.py
│   └── schemas/
│       ├── __init__.py
│       ├── agent_schemas.py    # Pydantic schemas (A2A-aligned)
│       └── tool_schemas.py
│
├── orchestration/               # Orchestration Builder
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── workflow.py         # Workflow definition
│   │   ├── node.py             # Node types
│   │   └── edge.py             # Connections
│   ├── services/
│   │   ├── __init__.py
│   │   ├── workflow_service.py
│   │   ├── validator.py        # Workflow validation
│   │   └── compiler.py         # Compile to executable
│   ├── patterns/
│   │   ├── __init__.py
│   │   ├── base.py             # Pattern interface
│   │   ├── sequential.py
│   │   ├── parallel.py
│   │   ├── conditional.py
│   │   ├── loop.py
│   │   └── router.py
│   └── schemas/
│       └── workflow_schemas.py
│
├── execution/                   # Execution Engine
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── deployment.py
│   │   ├── run.py
│   │   └── step.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── deployment_service.py
│   │   ├── execution_service.py
│   │   └── monitoring_service.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── executor.py         # Main execution logic
│   │   ├── scheduler.py        # Task scheduling
│   │   ├── context.py          # Execution context
│   │   └── sandbox.py          # Isolated execution
│   └── workers/
│       ├── __init__.py
│       └── celery_tasks.py     # Celery task definitions
│
└── shared/                      # Shared Components
    ├── __init__.py
    ├── messaging/
    │   ├── __init__.py
    │   ├── event_bus.py        # Internal event bus
    │   └── message_broker.py   # External messaging
    ├── security/
    │   ├── __init__.py
    │   ├── auth.py             # Authentication
    │   ├── permissions.py      # Authorization
    │   └── secrets.py          # Secrets management
    └── utils/
        ├── __init__.py
        ├── json_utils.py
        └── template_engine.py  # Expression evaluation
```

### 3.2 API Module Structure

```
api/
├── __init__.py
├── main.py                      # FastAPI application
├── dependencies.py              # Dependency injection
│
├── routes/
│   ├── __init__.py
│   ├── agents.py               # /api/v1/agents
│   ├── tools.py                # /api/v1/tools
│   ├── workflows.py            # /api/v1/workflows
│   ├── deployments.py          # /api/v1/deployments
│   ├── runs.py                 # /api/v1/runs
│   └── health.py               # /api/v1/health
│
├── middleware/
│   ├── __init__.py
│   ├── auth.py                 # Authentication middleware
│   ├── logging.py              # Request logging
│   └── error_handler.py        # Global error handling
│
└── websocket/
    ├── __init__.py
    ├── manager.py              # WebSocket connection manager
    └── handlers.py             # WebSocket event handlers
```

### 3.3 Adapter Module Structure

```
adapters/
├── __init__.py
├── base.py                      # Base adapter interfaces
│
├── llm_providers/               # LLM Provider Adapters
│   ├── __init__.py
│   ├── base.py                 # LLM adapter interface
│   ├── openai_adapter.py
│   ├── anthropic_adapter.py
│   ├── azure_openai_adapter.py
│   └── local_adapter.py        # Ollama, vLLM
│
├── frameworks/                  # Framework Adapters
│   ├── __init__.py
│   ├── base.py                 # Framework adapter interface
│   ├── langchain/
│   │   ├── __init__.py
│   │   ├── agent_adapter.py
│   │   └── tool_adapter.py
│   ├── autogen/
│   │   └── ...
│   └── crewai/
│       └── ...
│
└── tools/                       # Tool Adapters
    ├── __init__.py
    ├── base.py                 # Tool adapter interface
    ├── http_adapter.py         # REST API calls
    ├── database_adapter.py     # Database operations
    └── filesystem_adapter.py   # File operations
```

---

## 4. Data Models

### 4.1 Core Entities

```python
# Agent Entity (A2A-Enhanced)
class Agent:
    id: UUID
    name: str                    # Unique A2A identifier
    display_name: str
    type: AgentType              # LLM | WORKFLOW | EXTERNAL
    hosting: AgentHosting        # INTERNAL | EXTERNAL
    status: AgentStatus          # DRAFT | ACTIVE | DEPRECATED | ARCHIVED
    description: str             # Used in Agent Card
    url: str                     # A2A endpoint URL
    skills: List[Skill]          # A2A skill definitions
    a2a_capabilities: A2ACapabilities  # streaming, pushNotifications
    authentication: AgentAuth    # A2A auth configuration
    config: Dict[str, Any]       # Type-specific configuration
    version: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    created_by: UUID

# A2A Skill Entity
class Skill:
    id: str                      # Unique skill identifier
    name: str
    description: str             # For LLM understanding
    input_schema: Dict           # JSON Schema
    output_schema: Dict          # JSON Schema
    tags: List[str]

# A2A Capabilities
class A2ACapabilities:
    streaming: bool
    push_notifications: bool
    state_transition_history: bool

# A2A Task Entity
class A2ATask:
    id: UUID
    agent_id: UUID
    skill_id: str
    status: TaskStatus           # pending | running | completed | failed | canceled
    input_message: Message
    output_message: Optional[Message]
    artifacts: List[Artifact]
    history: List[TaskStateChange]
    created_at: datetime
    completed_at: Optional[datetime]
    metadata: Dict[str, Any]

# Tool Entity
class Tool:
    id: UUID
    name: str
    display_name: str
    type: ToolType               # HTTP | DATABASE | FILESYSTEM | CUSTOM
    status: ToolStatus
    description: str             # Used by LLM for tool selection
    input_schema: Dict           # JSON Schema
    output_schema: Dict
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

# Workflow Entity
class Workflow:
    id: UUID
    name: str
    display_name: str
    status: WorkflowStatus       # DRAFT | VALIDATED | PUBLISHED | DEPRECATED
    description: str
    input_schema: Dict
    output_schema: Dict
    nodes: List[Node]
    edges: List[Edge]
    config: Dict[str, Any]
    version: str
    created_at: datetime
    updated_at: datetime

# Deployment Entity
class Deployment:
    id: UUID
    name: str
    workflow_id: UUID
    workflow_version: str
    environment: Environment     # DEVELOPMENT | STAGING | PRODUCTION
    status: DeploymentStatus     # PENDING | RUNNING | STOPPED | FAILED
    config: Dict[str, Any]
    scaling_config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

# Run Entity
class Run:
    id: UUID
    deployment_id: UUID
    status: RunStatus            # PENDING | RUNNING | COMPLETED | FAILED | CANCELLED
    input_data: Dict
    output_data: Dict
    error: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    steps: List[Step]
    metrics: Dict[str, Any]
```

### 4.2 Database Schema

```sql
-- Agents Table
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    description TEXT,
    capabilities JSONB DEFAULT '[]',
    config JSONB NOT NULL,
    version VARCHAR(50) DEFAULT '1.0.0',
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID
);

-- Agent Versions Table
CREATE TABLE agent_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id),
    version VARCHAR(50) NOT NULL,
    config JSONB NOT NULL,
    changelog TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_id, version)
);

-- Tools Table
CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    description TEXT NOT NULL,
    input_schema JSONB NOT NULL,
    output_schema JSONB NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflows Table
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    description TEXT,
    input_schema JSONB NOT NULL,
    output_schema JSONB NOT NULL,
    nodes JSONB NOT NULL,
    edges JSONB NOT NULL,
    config JSONB DEFAULT '{}',
    version VARCHAR(50) DEFAULT '1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Deployments Table
CREATE TABLE deployments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    workflow_id UUID REFERENCES workflows(id),
    workflow_version VARCHAR(50),
    environment VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    config JSONB DEFAULT '{}',
    scaling_config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Runs Table
CREATE TABLE runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deployment_id UUID REFERENCES deployments(id),
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    input_data JSONB,
    output_data JSONB,
    error TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Run Steps Table
CREATE TABLE run_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES runs(id),
    node_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    error TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metrics JSONB DEFAULT '{}'
);

-- Indexes
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_deployments_workflow ON deployments(workflow_id);
CREATE INDEX idx_runs_deployment ON runs(deployment_id);
CREATE INDEX idx_runs_status ON runs(status);
CREATE INDEX idx_run_steps_run ON run_steps(run_id);
```

---

## 5. API Design

### 5.1 REST API Endpoints

#### Agents API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/agents | Create agent |
| POST | /api/v1/agents/register | Register external A2A agent |
| GET | /api/v1/agents | List agents |
| GET | /api/v1/agents/{id} | Get agent details |
| PUT | /api/v1/agents/{id} | Update agent |
| DELETE | /api/v1/agents/{id} | Delete agent |
| POST | /api/v1/agents/{id}/activate | Activate agent |
| POST | /api/v1/agents/{id}/deprecate | Deprecate agent |
| POST | /api/v1/agents/{id}/test | Test agent via A2A |
| GET | /api/v1/agents/{id}/versions | Get version history |
| GET | /api/v1/agents/{id}/card | Get A2A Agent Card |
| POST | /api/v1/agents/discover | Discover agents by capability |

#### A2A Protocol Endpoints (per-agent)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /.well-known/agent.json | Get Agent Card |
| POST | /a2a/tasks | Create A2A task |
| GET | /a2a/tasks/{taskId} | Get task status |
| DELETE | /a2a/tasks/{taskId} | Cancel task |
| POST | /a2a/tasks/{taskId}/messages | Send message to task |
| GET | /a2a/tasks/{taskId}/messages | Get task messages |
| GET | /a2a/tasks/{taskId}/stream | Stream task updates (SSE) |
| GET | /a2a/tasks/{taskId}/artifacts | Get task artifacts |
| GET | /a2a/health | A2A health check |

#### Tools API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/tools | Register tool |
| GET | /api/v1/tools | List tools |
| GET | /api/v1/tools/{id} | Get tool details |
| PUT | /api/v1/tools/{id} | Update tool |
| DELETE | /api/v1/tools/{id} | Delete tool |
| POST | /api/v1/tools/{id}/test | Test tool |

#### Workflows API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/workflows | Create workflow |
| GET | /api/v1/workflows | List workflows |
| GET | /api/v1/workflows/{id} | Get workflow details |
| PUT | /api/v1/workflows/{id} | Update workflow |
| DELETE | /api/v1/workflows/{id} | Delete workflow |
| POST | /api/v1/workflows/{id}/validate | Validate workflow |
| POST | /api/v1/workflows/{id}/publish | Publish workflow |
| GET | /api/v1/workflows/{id}/versions | Get version history |

#### Deployments API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/deployments | Create deployment |
| GET | /api/v1/deployments | List deployments |
| GET | /api/v1/deployments/{id} | Get deployment details |
| PUT | /api/v1/deployments/{id} | Update deployment |
| DELETE | /api/v1/deployments/{id} | Delete deployment |
| POST | /api/v1/deployments/{id}/start | Start deployment |
| POST | /api/v1/deployments/{id}/stop | Stop deployment |

#### Runs API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/runs | Execute orchestration |
| GET | /api/v1/runs | List runs |
| GET | /api/v1/runs/{id} | Get run details |
| GET | /api/v1/runs/{id}/logs | Get run logs |
| POST | /api/v1/runs/{id}/cancel | Cancel run |
| POST | /api/v1/runs/{id}/retry | Retry run |

### 5.2 WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| run.started | Server → Client | Run started |
| run.step.started | Server → Client | Step started |
| run.step.completed | Server → Client | Step completed |
| run.step.failed | Server → Client | Step failed |
| run.completed | Server → Client | Run completed |
| run.failed | Server → Client | Run failed |
| run.log | Server → Client | Log entry |

---

## 6. Security Architecture

### 6.1 Authentication

- **API Keys**: For programmatic access
- **JWT Tokens**: For user sessions
- **OAuth 2.0**: For SSO integration

### 6.2 Authorization

```python
# Role-Based Access Control
class Role(Enum):
    ADMIN = "admin"           # Full access
    DEVELOPER = "developer"   # Create/manage agents, workflows
    OPERATOR = "operator"     # Deploy and manage runs
    VIEWER = "viewer"         # Read-only access

# Permission Matrix
PERMISSIONS = {
    "admin": ["*"],
    "developer": [
        "agents:*",
        "tools:*",
        "workflows:*",
        "deployments:read",
        "runs:*"
    ],
    "operator": [
        "agents:read",
        "tools:read",
        "workflows:read",
        "deployments:*",
        "runs:*"
    ],
    "viewer": [
        "agents:read",
        "tools:read",
        "workflows:read",
        "deployments:read",
        "runs:read"
    ]
}
```

### 6.3 Secrets Management

- Credentials stored encrypted (AES-256)
- Environment-based secret injection
- Integration with external vaults (HashiCorp Vault, AWS Secrets Manager)

---

## 7. Deployment Architecture

### 7.1 Container Architecture

```yaml
# docker-compose.yml structure
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  worker:
    build: ./worker
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  minio:
    image: minio/minio
    volumes:
      - minio_data:/data
```

### 7.2 Scalability

```
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
     │  API 1  │    │  API 2  │    │  API 3  │
     └────┬────┘    └────┬────┘    └────┬────┘
          │               │               │
          └───────────────┼───────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
     │Worker 1 │    │Worker 2 │    │Worker N │
     └─────────┘    └─────────┘    └─────────┘
```

---

## 8. Monitoring & Observability

### 8.1 Metrics (Prometheus)

- Request latency
- Request throughput
- Error rates
- Active runs
- Queue depth
- Resource utilization

### 8.2 Logging (Structured)

```python
{
    "timestamp": "2026-01-25T10:30:00Z",
    "level": "INFO",
    "service": "execution-engine",
    "run_id": "uuid",
    "step_id": "uuid",
    "message": "Step completed",
    "duration_ms": 1234,
    "context": {...}
}
```

### 8.3 Tracing (OpenTelemetry)

- Distributed tracing across services
- Run execution traces
- External API call traces

### 8.4 LLMOps & AgentOps Signals

Infrastructure metrics, logs, and traces above are complemented by **AgentOps** (run/step/A2A correlation, operator error taxonomy) and **LLMOps** (v2.0+: model/prompt versions, token/cost, eval hooks, guardrails, RAG health). See [10-LLM-AGENT-OPERATIONS.md](./10-LLM-AGENT-OPERATIONS.md) and diagrams `01`, `02`, and `06` under `/docs/diagrams/`.

---

## 9. Architecture Evolution - v2.0 and Beyond

### 9.1 v2.0 Architecture - Enhanced AI Platform

Version 2.0 extends the core platform with advanced AI capabilities including LLM management, prompt engineering, memory/RAG pipelines, MCP integration, and enhanced tools management.

#### 9.1.1 v2.0 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Web App   │    │ Desktop App │    │     CLI     │    │  Python SDK │  │
│  │   (React)   │    │   (Tauri)   │    │   (Click)   │    │             │  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
└─────────┼──────────────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │                  │
          └──────────────────┴────────┬─────────┴──────────────────┘
                                      │
                              ┌───────▼───────┐
                              │   API Gateway │
                              │    (FastAPI)  │
                              └───────┬───────┘
                                      │
┌─────────────────────────────────────┼─────────────────────────────────────┐
│                         AI SERVICES LAYER (v2.0)                           │
│  ┌────────────────────┐    ┌────────────────────┐    ┌────────────────┐   │
│  │   LLM Management   │    │  Prompt Management │    │  Memory & RAG  │   │
│  │   Service          │    │  Service           │    │  Service       │   │
│  └────────┬───────────┘    └────────┬───────────┘    └────────┬───────┘   │
│           │                         │                         │            │
│  ┌────────┴──────────────────────────┴─────────────────────────┴────────┐  │
│  │  MCP Integration Service | Enhanced Tools Management Service         │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
┌─────────────────────────────────────┼─────────────────────────────────────┐
│              CORE ORCHESTRATION LAYER (v1.0 components)                    │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  Agent Service  │    │  Orchestration  │    │   Deployment    │        │
│  │                 │    │    Service      │    │    Service      │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                            ADAPTER LAYER                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────┐ │
│  │   LLM        │    │   Vector DB  │    │     MCP      │    │ Framework
│  │   Providers  │    │   Adapters   │    │   Clients    │    │ Adapters │
│  │              │    │              │    │              │    │          │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └─────────┘ │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                       INFRASTRUCTURE LAYER (v2.0)                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  PostgreSQL │    │    Redis    │    │ Vector DBs  │    │   Celery    │ │
│  │  +Metadata  │    │   (Cache)   │    │ (Milvus,    │    │  (Workers)  │ │
│  │  Store      │    │             │    │ Weaviate)   │    │             │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                    │
│  │ MinIO/S3    │    │ Message     │    │ External    │                    │
│  │ (Storage)   │    │ Queue       │    │ APIs        │                    │
│  │             │    │ (RabbitMQ)  │    │             │                    │
│  └─────────────┘    └─────────────┘    └─────────────┘                    │
└───────────────────────────────────────────────────────────────────────────┘
```

#### 9.1.2 v2.0 New Core Modules Structure

```
core/
├── ai/                          # NEW: AI Management Layer
│   ├── __init__.py
│   │
│   ├── llm/                     # LLM Model Management
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── model.py         # LLM Model entity
│   │   │   ├── provider.py      # Provider configuration
│   │   │   └── performance.py   # Performance metrics
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── model_service.py # Model CRUD + deployment
│   │   │   ├── provider_service.py # Provider management
│   │   │   ├── fallback_service.py # Model failover logic
│   │   │   └── cost_tracker.py  # Token/cost tracking
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # LLM adapter interface
│   │   │   ├── openai_adapter.py
│   │   │   ├── anthropic_adapter.py
│   │   │   ├── azure_adapter.py
│   │   │   └── local_adapter.py # Ollama, vLLM
│   │   └── schemas/
│   │       └── model_schemas.py
│   │
│   ├── prompts/                 # Prompt Management
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── template.py      # Prompt template entity
│   │   │   ├── variable.py      # Template variables
│   │   │   └── test_case.py     # Prompt test cases
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── template_service.py # Template CRUD
│   │   │   ├── engine.py        # Prompt rendering engine
│   │   │   ├── optimizer.py     # Optimization suggestions
│   │   │   └── tester.py        # A/B testing
│   │   ├── repositories/
│   │   │   └── template_repository.py
│   │   └── schemas/
│   │       └── template_schemas.py
│   │
│   ├── memory/                  # Memory & Context Management
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── memory.py        # Memory entity
│   │   │   ├── context.py       # Context window
│   │   │   └── summary.py       # Memory summary
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── memory_service.py # Memory CRUD
│   │   │   ├── context_manager.py # Context window mgmt
│   │   │   ├── cleanup_service.py # Memory lifecycle
│   │   │   └── summarizer.py    # Context summarization
│   │   └── schemas/
│   │       └── memory_schemas.py
│   │
│   ├── rag/                     # RAG Pipeline Management
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py      # RAG pipeline entity
│   │   │   ├── document.py      # Document entity
│   │   │   ├── chunk.py         # Document chunk
│   │   │   ├── embedding.py     # Embedding entity
│   │   │   └── retrieval.py     # Retrieval strategy
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── pipeline_service.py # Pipeline CRUD
│   │   │   ├── ingestion_service.py # Document ingestion
│   │   │   ├── chunking_service.py # Document chunking
│   │   │   ├── embedding_service.py # Embedding generation
│   │   │   ├── retrieval_service.py # Semantic search
│   │   │   └── knowledge_base_service.py # KB management
│   │   ├── chunkers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── semantic_chunker.py
│   │   │   └── recursive_chunker.py
│   │   ├── vector_clients/
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Vector DB interface
│   │   │   ├── milvus_client.py
│   │   │   ├── weaviate_client.py
│   │   │   ├── pinecone_client.py
│   │   │   └── qdrant_client.py
│   │   └── schemas/
│   │       └── rag_schemas.py
│   │
│   └── mcp/                     # MCP Integration
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── server.py        # MCP server entity
│       │   ├── resource.py      # MCP resource entity
│       │   ├── tool.py          # MCP tool entity
│       │   └── capability.py    # MCP capability
│       ├── services/
│       │   ├── __init__.py
│       │   ├── server_service.py # MCP server mgmt
│       │   ├── discovery_service.py # Resource discovery
│       │   ├── resource_service.py # Resource access
│       │   ├── tool_service.py  # Tool registration
│       │   └── cache_service.py # Resource caching
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── base_client.py   # MCP client interface
│       │   ├── stdio_client.py  # Stdio transport
│       │   └── sse_client.py    # SSE transport
│       └── schemas/
│           └── mcp_schemas.py
│
├── tools/                       # ENHANCED: Tools Management (v2.0)
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tool.py              # Enhanced tool entity
│   │   ├── version.py           # Tool versioning
│   │   ├── dependency.py        # Tool dependencies
│   │   └── capability.py        # Tool capabilities
│   ├── services/
│   │   ├── __init__.py
│   │   ├── tool_service.py      # Enhanced CRUD
│   │   ├── version_service.py   # Version management
│   │   ├── dependency_resolver.py # Dependency resolution
│   │   ├── capability_service.py # Capability discovery
│   │   ├── execution_service.py # Tool execution
│   │   ├── sandbox_service.py   # Execution sandbox
│   │   ├── validation_service.py # Parameter validation
│   │   └── analytics_service.py # Usage analytics
│   ├── repositories/
│   │   └── tool_repository.py
│   └── schemas/
│       └── tool_schemas.py
│
# ... rest of core modules (agent, orchestration, execution, registry, shared)
```

#### 9.1.3 v2.0 Database Extensions

New tables to support v2.0 features:

```sql
-- LLM Models Table
CREATE TABLE llm_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    provider VARCHAR(100) NOT NULL,          -- openai, anthropic, azure, local
    model_id VARCHAR(255) NOT NULL,          -- gpt-4, claude-3, etc.
    version VARCHAR(50),
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    config JSONB NOT NULL,                   -- temperature, max_tokens, etc.
    performance_metrics JSONB DEFAULT '{}',  -- latency, cost, error_rate
    cost_per_1k_tokens DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prompt Templates Table
CREATE TABLE prompt_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    template TEXT NOT NULL,                  -- Template with {variables}
    variables JSONB NOT NULL,                -- {name, type, required}
    version VARCHAR(50) DEFAULT '1.0.0',
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Memory Storage Table
CREATE TABLE agent_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id),
    conversation_id UUID,
    memory_type VARCHAR(50),                 -- SHORT_TERM, LONG_TERM, SEMANTIC
    content JSONB NOT NULL,
    ttl INTEGER,                             -- Time to live in seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- RAG Documents Table
CREATE TABLE rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pipeline_id UUID,
    source_url VARCHAR(1000),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RAG Document Chunks Table
CREATE TABLE rag_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES rag_documents(id),
    chunk_index INTEGER,
    content TEXT NOT NULL,
    embedding VECTOR(1536),                  -- Vector embedding
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MCP Servers Table
CREATE TABLE mcp_servers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    url VARCHAR(1000),                       -- Stdio or SSE endpoint
    transport_type VARCHAR(50),              -- stdio, sse, http
    status VARCHAR(50) NOT NULL DEFAULT 'INITIALIZED',
    config JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MCP Resources Table
CREATE TABLE mcp_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    server_id UUID REFERENCES mcp_servers(id),
    resource_uri VARCHAR(1000) NOT NULL,
    description TEXT,
    resource_type VARCHAR(100),
    content_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Tool Dependencies Table
CREATE TABLE tool_dependencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id UUID REFERENCES tools(id),
    dependency_tool_id UUID REFERENCES tools(id),
    dependency_type VARCHAR(50),             -- RUNTIME, BUILD, OPTIONAL
    version_constraint VARCHAR(100),         -- >=1.0.0, <2.0.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tool Analytics Table
CREATE TABLE tool_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id UUID REFERENCES tools(id),
    execution_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    avg_execution_time_ms DECIMAL(10,2),
    last_executed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for v2.0 performance
CREATE INDEX idx_llm_models_provider ON llm_models(provider);
CREATE INDEX idx_prompt_templates_status ON prompt_templates(status);
CREATE INDEX idx_agent_memories_agent_id ON agent_memories(agent_id);
CREATE INDEX idx_agent_memories_expires ON agent_memories(expires_at);
CREATE INDEX idx_rag_chunks_document ON rag_chunks(document_id);
CREATE INDEX idx_rag_chunks_embedding ON rag_chunks USING ivfflat (embedding);
CREATE INDEX idx_mcp_resources_server ON mcp_resources(server_id);
CREATE INDEX idx_tool_dependencies_tool ON tool_dependencies(tool_id);
```

#### 9.1.4 v2.0 New API Endpoints

| Module | Endpoints |
|--------|-----------|
| **LLM Models** | POST/GET/PUT/DELETE /api/v1/llm/models |
| | POST /api/v1/llm/models/{id}/test |
| | GET /api/v1/llm/models/{id}/performance |
| **Prompts** | POST/GET/PUT/DELETE /api/v1/prompts/templates |
| | POST /api/v1/prompts/templates/{id}/test |
| | POST /api/v1/prompts/templates/{id}/ab-test |
| **Memory** | GET/DELETE /api/v1/agents/{id}/memory |
| | POST /api/v1/agents/{id}/memory/cleanup |
| **RAG** | POST/GET/PUT/DELETE /api/v1/rag/pipelines |
| | POST /api/v1/rag/pipelines/{id}/ingest |
| | POST /api/v1/rag/pipelines/{id}/search |
| **MCP** | POST/GET/DELETE /api/v1/mcp/servers |
| | GET /api/v1/mcp/servers/{id}/resources |
| | POST /api/v1/mcp/servers/{id}/test |
| **Tools** | Enhanced with /api/v1/tools/{id}/dependencies |
| | /api/v1/tools/{id}/analytics |
| | /api/v1/tools/{id}/versions |

#### 9.1.5 v2.0 Technology Stack Additions

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Vector DB** | Milvus, Weaviate, Pinecone, Qdrant | RAG embeddings storage |
| **Embedding Models** | OpenAI, Sentence Transformers | Document embeddings |
| **Document Processing** | LangChain, Unstructured.io | Document parsing |
| **Vector Indexing** | pgvector (PostgreSQL) | Efficient similarity search |
| **MCP SDK** | Claude SDK for MCP | MCP client/server |
| **Message Queue** | RabbitMQ (optional) | Async job processing |
| **Monitoring** | Enhanced metrics | LLM usage, RAG performance |

#### 9.1.6 v2.0 Architecture Considerations

**Scalability:**
- LLM provider load balancing
- Vector DB horizontal scaling
- RAG pipeline parallelization
- MCP server discovery & pooling
- Tool execution queue optimization

**Performance:**
- LLM response caching
- Vector embedding caching
- Memory summarization for context
- RAG retrieval optimization
- Tool execution performance tracking

**Reliability:**
- LLM provider failover
- RAG indexing recovery
- Memory persistence
- MCP server health checks
- Tool versioning & rollback

**Security:**
- LLM API key management
- Memory encryption at rest
- RAG document access control
- MCP server authentication
- Tool execution sandboxing

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | - | Initial draft |
| 1.1 | 2026-04-12 | - | Added v2.0 architecture for LLM, Prompt, Memory/RAG, MCP, and enhanced Tools management |
