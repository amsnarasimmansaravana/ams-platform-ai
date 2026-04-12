# AMS-AI: Technical Foundation
## Architecture, Technology Stack & Infrastructure
**Generated:** April 12, 2026
**Audience:** Architects, Engineers, DevOps, Security Teams
**Version:** 1.0

---

## 1. TECHNOLOGY STACK

### 1.1 Backend Framework

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| **Language** | Python | 3.11+ | Rich AI ecosystem, async support, team preference |
| **API Framework** | FastAPI | 0.100+ | Async, OpenAPI, excellent performance |
| **Web Framework (Async)** | Starlette | Latest | Built into FastAPI |
| **CLI Framework** | Click/Typer | Latest | Developer experience, command structure |
| **Package Manager** | Poetry | Latest | Dependency management, reproducible builds |

### 1.2 Data Layer

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Primary Database** | PostgreSQL | 15+ | ACID compliance, JSON support, pgvector (v2.0) |
| **Cache Store** | Redis | 7+ | Session storage, cache, pub/sub messaging |
| **Object Storage** | MinIO / S3 | Compatible | File artifacts, logs, backups |
| **Vector DB** | Milvus, Weaviate, Pinecone, Qdrant | Latest | RAG embeddings & semantic search (v2.0) |
| **Search (Optional)** | Elasticsearch | 8.x | Full-text search (optional enhancement) |

### 1.3 Asynchronous Processing

| Component | Technology | Purpose | Justification |
|-----------|-----------|---------|---------------|
| **Task Queue** | Celery | Distributed task processing | Scalable job execution |
| **Message Broker** | Redis | Primary | Fast, in-memory broker |
| **Alt Broker** | RabbitMQ | Optional | More robust for high-throughput |
| **Job Scheduling** | APScheduler | Recurring tasks | Cron-like scheduling |

### 1.4 Frontend (Web)

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Framework** | React | 18+ | Component-based, large ecosystem |
| **Language** | TypeScript | 5.0+ | Type safety |
| **State Mgmt** | Zustand / Redux Toolkit | Latest | Lightweight & scalable |
| **UI Components** | Shadcn/ui | Latest | Modern, accessible, customizable |
| **Styling** | Tailwind CSS | Latest | Utility-first, responsive design |
| **Workflow Canvas** | React Flow | Latest | Visual workflow editor |
| **HTTP Client** | Axios / TanStack Query | Latest | API communication & caching |
| **Build Tool** | Vite | Latest | Fast builds, HMR, optimized |
| **Package Mgr** | pnpm | Latest | Fast, efficient package management |

### 1.5 Desktop Application

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Tauri | Lightweight, cross-platform |
| **Languages** | Rust (backend) + React (UI) | Performance + modern UI |
| **Supported OS** | Windows, macOS, Linux | Cross-platform support |
| **Native Capabilities** | System integration, file I/O | Desktop-specific features |

### 1.6 DevOps & Infrastructure

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Containerization** | Docker | 24+ | Environment consistency |
| **Container Compose** | Docker Compose | Latest | Local development |
| **Orchestration** | Kubernetes | 1.27+ | Production deployment |
| **IaC** | Terraform | Latest | Infrastructure as code |
| **CI/CD** | GitHub Actions | Native | Build, test, deploy pipelines |
| **Container Registry** | Docker Hub / ECR | Latest | Image storage & distribution |

### 1.7 Monitoring & Observability

| Layer | Technology | Purpose | Integration |
|-------|-----------|---------|-------------|
| **Metrics** | Prometheus | Time-series metrics collection | Scrapes endpoints |
| **Visualization** | Grafana | Dashboards & alerting | Reads Prometheus data |
| **Distributed Tracing** | OpenTelemetry | Trace requests across services | Exports to Jaeger/Datadog |
| **Logging** | Loki / ELK Stack | Centralized logging | Collects container logs |
| **APM** | Datadog / New Relic | Optional | Advanced monitoring |

### 1.8 Security & Secrets

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Secrets Management** | HashiCorp Vault / AWS Secrets Mgr | Credential rotation |
| **API Authentication** | JWT (JSON Web Tokens) | Stateless auth |
| **OAuth2/OIDC** | AuthLib / Authz0 | Enterprise SSO |
| **Encryption (in-transit)** | TLS 1.3 | Secure communication |
| **Encryption (at-rest)** | AES-256-GCM | Database encryption |
| **SSL Certificates** | Let's Encrypt / Managed Certs | HTTPS/TLS |

---

## 2. SYSTEM ARCHITECTURE

### 2.1 6-Tier Layered Architecture

```
┌────────────────────────────────────────────────────────────────┐
│ 1. CLIENT TIER                                                 │
│    Web (React SPA)  |  Desktop (Tauri)  |  CLI (Click)  |  SDK │
│    ↓ HTTP/WebSocket ↓                                          │
├────────────────────────────────────────────────────────────────┤
│ 2. API GATEWAY TIER                                            │
│    FastAPI Router  |  Auth (JWT/OAuth)  |  Rate Limiting       │
│    Request Validation  |  Error Handling  |  CORS              │
│    ↓ Async ↓                                                   │
├────────────────────────────────────────────────────────────────┤
│ 3. CORE SERVICES TIER (v1.0)                                   │
│    ├─ Agent Service (registry, lifecycle, versioning)         │
│    ├─ Tool Service (API registry, authentication)             │
│    ├─ Orchestration Service (builder, validator, compiler)    │
│    ├─ Execution Service (engine, scheduler, context)          │
│    ├─ Deployment Service (configs, scaling, health)           │
│    └─ Audit Service (immutable logs, compliance)              │
│    ↓ Async Processing ↓                                        │
├────────────────────────────────────────────────────────────────┤
│ 4. AI SERVICES TIER (v2.0)                                     │
│    ├─ LLM Service (model registry, provider routing)           │
│    ├─ Prompt Service (templates, A/B testing, optimization)   │
│    ├─ Memory Service (short/long/semantic memory)             │
│    ├─ RAG Service (document ingestion, semantic search)       │
│    └─ MCP Service (Model Context Protocol integration)        │
│    ↓ Adapters ↓                                                │
├────────────────────────────────────────────────────────────────┤
│ 5. ADAPTER TIER                                                │
│    ├─ Framework Adapters (LangChain, AutoGen, CrewAI)         │
│    ├─ LLM Adapters (OpenAI, Anthropic, Hugging Face, etc.)   │
│    ├─ Vector DB Adapters (Milvus, Weaviate, Pinecone, etc.)  │
│    ├─ Tool Adapters (HTTP, DB, File System, Messaging)       │
│    └─ Storage Adapters (PostgreSQL, S3, Redis)               │
│    ↓ Native Protocols ↓                                        │
├────────────────────────────────────────────────────────────────┤
│ 6. INFRASTRUCTURE TIER                                         │
│    ├─ PostgreSQL (primary data store, pgvector)              │
│    ├─ Redis (cache, sessions, pub/sub)                      │
│    ├─ MinIO/S3 (object storage)                              │
│    ├─ Vector DBs (Milvus, Weaviate, etc.)                   │
│    ├─ Message Brokers (Celery + Redis/RabbitMQ)            │
│    ├─ Celery Workers (async task processing)                │
│    └─ Observability Stack (Prometheus, Grafana, Loki, etc.) │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Module Structure

```
ams-ai/
├── core/
│   ├── a2a/                    # A2A Protocol Implementation
│   │   ├── protocol.py        # A2A message formats
│   │   ├── discovery.py       # Agent discovery service
│   │   ├── messaging.py       # Inter-agent messaging
│   │   └── validation.py      # A2A compliance checks
│   │
│   ├── registry/               # Agent & Tool Registry
│   │   ├── agent_registry.py  # Agent lifecycle
│   │   ├── tool_registry.py   # Tool management
│   │   ├── schema.py          # Data models
│   │   └── validator.py       # Schema validation
│   │
│   ├── orchestration/          # Orchestration Engine
│   │   ├── builder.py         # Visual builder API
│   │   ├── compiler.py        # Executable compilation
│   │   ├── validator.py       # Workflow validation
│   │   ├── patterns.py        # Sequential, Parallel, etc.
│   │   └── storage.py         # Workflow persistence
│   │
│   ├── execution/              # Execution Runtime
│   │   ├── engine.py          # Core execution loop
│   │   ├── scheduler.py       # Task scheduling
│   │   ├── context.py         # Execution context
│   │   ├── state.py           # State management
│   │   └── monitoring.py      # Runtime monitoring
│   │
│   ├── deployment/             # Deployment Management
│   │   ├── config.py          # Deployment configs
│   │   ├── scaling.py         # Auto-scaling logic
│   │   ├── health.py          # Health checks
│   │   └── rollback.py        # Rollback mechanisms
│   │
│   ├── ai/                     # AI Services (v2.0+)
│   │   ├── llm/               # LLM Management
│   │   ├── prompts/           # Prompt Engineering
│   │   ├── memory/            # Memory Systems
│   │   ├── rag/               # RAG Pipelines
│   │   └── mcp/               # MCP Integration
│   │
│   └── shared/                 # Shared Utilities
│       ├── security/          # Auth, encryption, secrets
│       ├── logging/           # Logging & tracing
│       ├── metrics/           # Metrics & observability
│       ├── messaging/         # Event publishing
│       ├── cache/             # Caching layer
│       ├── db/                # Database utilities
│       └── errors/            # Error handling
│
├── adapters/                   # Third-Party Adapters
│   ├── frameworks/            # LangChain, AutoGen, CrewAI
│   ├── llms/                  # LLM provider clients
│   ├── vector_dbs/            # Vector DB clients
│   ├── tools/                 # Tool execution adapters
│   └── storage/               # Storage backends
│
├── api/                        # FastAPI Application
│   ├── routers/               # API route handlers
│   ├── middleware/            # CORS, auth, logging
│   ├── dependencies/          # Dependency injection
│   ├── schemas/               # Request/response models
│   └── main.py               # Application entry point
│
├── cli/                        # Command-Line Interface
│   ├── agent.py              # Agent management commands
│   ├── workflow.py           # Workflow commands
│   ├── deploy.py             # Deployment commands
│   └── misc.py               # Utility commands
│
├── worker/                     # Celery Worker Setup
│   ├── tasks.py              # Async tasks
│   ├── config.py             # Worker configuration
│   └── main.py               # Worker entry point
│
├── tests/                      # Test Suite
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
│
├── docker/                     # Docker Configuration
│   ├── Dockerfile            # Container image
│   ├── docker-compose.yml    # Multi-container setup
│   └── .dockerignore
│
├── k8s/                        # Kubernetes Manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── statefulset.yaml
│   └── ingress.yaml
│
└── docs/
    ├── API.md
    ├── DEPLOYMENT.md
    ├── ARCHITECTURE.md
    └── CONTRIBUTING.md
```

###2.3 Data Models

#### Agent Registry Schema
```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    framework VARCHAR(50),           -- LangChain, AutoGen, CrewAI, etc.
    version VARCHAR(50),
    status ENUM('draft', 'active', 'deprecated', 'archived'),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_by UUID REFERENCES users(id),
    metadata JSONB,        -- Custom metadata
    skill_tags TEXT[],     -- For semantic search
    UNIQUE(name, version)
);

CREATE TABLE agent_versions (
    id UUID PRIMARY KEY,
    agent_id UUID REFERENCES agents(id),
    version_number INT,
    config JSONB,
    created_at TIMESTAMP,
    created_by UUID REFERENCES users(id)
);
```

#### Orchestration Schema
```sql
CREATE TABLE orchestrations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50),
    status ENUM('draft', 'active', 'deprecated'),
    graph_definition JSONB,        -- DAG structure
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_by UUID REFERENCES users(id),
    UNIQUE(name, version)
);

CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY,
    orchestration_id UUID REFERENCES orchestrations(id),
    status ENUM('pending', 'running', 'completed', 'failed'),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    result JSONB,
    error_message TEXT,
    execution_context JSONB,
    parent_execution_id UUID,      -- For hierarchical workflows
    created_at TIMESTAMP
);

CREATE TABLE execution_logs (
    id UUID PRIMARY KEY,
    execution_id UUID REFERENCES workflow_executions(id),
    step_id VARCHAR(255),          -- Node ID in DAG
    status ENUM('pending', 'running', 'completed', 'failed'),
    input_data JSONB,
    output_data JSONB,
    error TEXT,
    duration_ms INT,
    timestamp TIMESTAMP
);
```

#### Tool Registry Schema
```sql
CREATE TABLE tools (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tool_type ENUM('http', 'database', 'filesystem', 'messaging', 'custom'),
    config JSONB,          -- Type-specific config
    auth_config JSONB,     -- Encrypted credentials
    input_schema JSONB,    -- JSON Schema
    output_schema JSONB,   -- JSON Schema
    status VARCHAR(50),
    health_check_url VARCHAR(500),
    last_health TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(name)
);
```

#### Audit Log Schema
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(255),
    resource_type VARCHAR(50),     -- agent, tool, orchestration, etc.
    resource_id UUID,
    changes JSONB,                 -- Old vs new values
    timestamp TIMESTAMP IMMUTABLE,  -- Immutable timestamp
    ip_address INET,
    user_agent TEXT,
    tenant_id UUID REFERENCES tenants(id),  -- v1.5+
    CONSTRAINT audit_immutable CHECK (timestamp = timestamp)
);

CREATE INDEX audit_logs_tenant_timestamp ON audit_logs(tenant_id, timestamp DESC);
```

---

## 3. ENTERPRISE REQUIREMENTS

### 3.1 Security Requirements (Critical)

| ID | Requirement | Implementation | v1.0 |
|----|-------------|-----------------|------|
| **ER-SEC-001** | Enterprise SSO (SAML 2.0, OIDC) | AuthLib integration, JWT tokens | ✅ |
| **ER-SEC-002** | Multi-Factor Authentication | TOTP, WebAuthn, email OTP | ✅ |
| **ER-SEC-003** | TLS 1.3 & mTLS | Nginx/HAProxy termination + mTLS | ✅ |
| **ER-SEC-004** | AES-256-GCM at rest | Database encryption + file encryption | ✅ |
| **ER-SEC-005** | Secrets management | HashiCorp Vault / AWS Secrets Mgr | ✅ |
| **ER-SEC-006** | Role-Based Access Control | RBAC with role inheritance | ✅ |
| **ER-SEC-007** | Immutable audit logging | Append-only audit table with constraints | ✅ |
| **ER-SEC-008** | API key lifecycle | Signed keys, rotation policies, expiry | ✅ |

### 3.2 Compliance Requirements

| Framework | v1.0 | v1.5 | v2.0 | Approach |
|-----------|------|------|------|----------|
| **SOC 2 Type II** | 🟡 Ready | ✅ Certified | ✅ Certified | Annual audit |
| **ISO 27001** | 🟡 Ready | ✅ Certified | ✅ Certified | Certified ISMS |
| **GDPR** | ✅ Compliant | ✅ Compliant | ✅ Compliant | Data subject rights APIs |
| **HIPAA** | 🟡 Config | ✅ Ready | ✅ Ready | Encryption + audit trails |
| **PCI DSS** | 🟡 Config | ✅ Ready | ✅ Ready | Tokenization + encryption |
| **FedRAMP** | - | - | 🔄 In Progress | Authority to Operate (ATO) |

### 3.3 High Availability & Disaster Recovery

| Metric | v1.0 | v1.5 | v2.0 | Strategy |
|--------|------|------|------|----------|
| **Availability SLA** | 99.9% | 99.95% | 99.99% | Multi-region + load balancer |
| **RPO (max data loss)** | < 1 hour | < 15 min | 0 (zero loss) | Continuous replication |
| **RTO (max downtime)** | < 4 hours | < 1 hour | < 15 min | Automated failover |
| **Data Durability** | 99.99999% | 99.999999% | 99.999999999% | 3+ region replication |
| **Multi-Region** | Single | Yes (Active-passive) | Yes (Active-active) | Geographic clustering |
| **Backup Strategy** | Daily snapshots | Hourly + CDC | Continuous + CDC | Automated testing |

**HA/DR Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│ Global Load Balancer (Route 53 / CloudFlare)               │
└──────┬──────────────────────────────────────────┬──────────┘
       │                                          │
       ↓ Primary Region (Active)              ↓ DR Region (Standby → Active)
    ┌──────────────────────┐           ┌──────────────────────┐
    │ K8s Cluster (Primary)│           │ K8s Cluster (DR)    │
    │ ├─ App Tier         │           │ ├─ App Tier         │
    │ ├─ Cache (Redis)    │◄──────────┤ ├─ Cache (Redis)    │
    │ └─ Workers          │ Replication│ └─ Workers          │
    └──────────────────────┘           └──────────────────────┘
       │ CDC (Change Data Capture)
       ↓
    ┌──────────────────────┐           ┌──────────────────────┐
    │ Primary DB         │           │ Replica DB (Standby) │
    │ (PostgreSQL)       │◄──────────┤ (PostgreSQL)         │
    │ Write              │ Streaming │ Read-only            │
    └──────────────────────┘ Replication└──────────────────────┘
```

### 3.4 Scalability Targets

| Metric | Target | Scaling Strategy |
|--------|--------|-----------------|
| **Concurrent Workflows** | 10,000+ | Horizontal worker scaling |
| **Concurrent Users** | 5,000+ | Session pooling + Redis |
| **Managed Agents** | 100,000+ | Registry sharding by agent ID |
| **API Latency (p95)** | < 200ms | Caching + CDN |
| **Throughput** | 10,000+ req/sec | Load balancer + async processing |
| **Storage Growth** | Linear scaling | Partitioned archives by date |
| **Agent Registry** | 100,000+ agents | Consistent hashing + sharding |

---

## 4. DEPLOYMENT ARCHITECTURE

### 4.1 Kubernetes Manifests

**Deployment Strategy:**
```yaml
# Service: API Gateway (Load Balanced)
apiVersion: v1
kind: Service
metadata:
  name: ams-ai-api
spec:
  type: LoadBalancer
  selector:
    app: ams-ai
  ports:
    - port: 443
      targetPort: 8000
      protocol: TCP

---

# Deployment: Core Services
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ams-ai-core
spec:
  replicas: 3              # Multi-replica for HA
  selector:
    matchLabels:
      app: ams-ai
      tier: core
  template:
    metadata:
      labels:
        app: ams-ai
        tier: core
    spec:
      containers:
      - name: api
        image: ams-ai:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis_url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

---

# StatefulSet: Celery Workers (for stateful tasks)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ams-ai-workers
spec:
  serviceName: ams-ai-workers
  replicas: 5
  selector:
    matchLabels:
      app: ams-ai
      tier: worker
  template:
    metadata:
      labels:
        app: ams-ai
        tier: worker
    spec:
      containers:
      - name: worker
        image: ams-ai:latest
        command: ["celery", "-A", "worker", "worker"]
        env:
        - name: CELERY_BROKER_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis_url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"

---

# PersistentVolumeClaim: For logs & artifacts
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ams-ai-storage
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
```

### 4.2 Observability Stack Configuration

**Prometheus Scrape Targets:**
```yaml
global:
  scrape_interval: 15s
  scrape_timeout: 10s

scrape_configs:
  - job_name: 'ams-ai-api'
    static_configs:
      - targets: ['ams-ai-api:9090']
    metrics_path: '/metrics'

  - job_name: 'ams-ai-workers'
    static_configs:
      - targets: ['ams-ai-workers:9090']

  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  - job_name: 'kubernetes'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

**Key Metrics to Track:**
- API request latency (p95, p99)
- Database query performance
- Workflow execution success rate
- Agent response time
- Queue depth (Celery)
- Cache hit ratio
- System resource utilization (CPU, memory, disk)

### 4.3 LLMOps & AgentOps

Platform metrics and traces above cover **infrastructure**. **AgentOps** adds run/step/A2A-correlated signals for orchestration reliability; **LLMOps** (v2.0+) adds model, prompt, token/cost, evaluation, guardrail, and RAG/MCP operational metrics. Full capability matrix and requirement IDs: [`/docs/v1.0/10-LLM-AGENT-OPERATIONS.md`](../v1.0/10-LLM-AGENT-OPERATIONS.md). Diagrams: `diagrams/01-high-level-architecture.puml`, `02-technical-architecture-deepdive.puml`, `06-v2-advanced-ai-architecture.puml`.

---

## 5. API SPECIFICATIONS

### 5.1 RESTful API Endpoints

**Agent Registry Endpoints:**
```
GET    /api/v1/agents                      # List agents
POST   /api/v1/agents                      # Register agent
GET    /api/v1/agents/{agent_id}           # Get agent details
PUT    /api/v1/agents/{agent_id}           # Update agent
DELETE /api/v1/agents/{agent_id}           # Delete agent (soft)
GET    /api/v1/agents/search?skills=...    # Search by skills
```

**Orchestration Endpoints:**
```
GET    /api/v1/orchestrations              # List workflows
POST   /api/v1/orchestrations              # Create workflow
GET    /api/v1/orchestrations/{orch_id}    # Get workflow
PUT    /api/v1/orchestrations/{orch_id}    # Update workflow
DELETE /api/v1/orchestrations/{orch_id}    # Delete workflow
POST   /api/v1/orchestrations/{orch_id}/execute  # Execute async
GET    /api/v1/executions/{exec_id}        # Get execution status
```

**Execution Endpoints:**
```
POST   /api/v1/executions                  # Create execution
GET    /api/v1/executions/{exec_id}        # Get execution details
GET    /api/v1/executions/{exec_id}/logs   # Get execution logs
POST   /api/v1/executions/{exec_id}/cancel # Cancel execution
```

### 5.2 WebSocket API (Real-Time)

**For live execution tracking:**
```
ws://api.ams-ai.com/api/v1/ws/executions/{exec_id}
  Messages:
    - ExecutionStarted
    - StepStarted
    - StepCompleted
    - StepFailed
    - ExecutionCompleted
    - ExecutionFailed
```

---

## 6. REFERENCE DOCUMENTS

For more detail:

- **Executive Summary** → `1-EXECUTIVE-SUMMARY.md` (Strategy)
- **Product Specification** → `2-PRODUCT-SPECIFICATION.md` (Features)
- **Getting Started** → `4-GETTING-STARTED.md` (Developer guides)

For original specifications:
- Technical Architecture → `/docs/v1.0/04-TECHNICAL-ARCHITECTURE.md`
- Non-Functional Requirements → `/docs/v1.0/08-NON-FUNCTIONAL-REQUIREMENTS.md`
- A2A Protocol Spec → `/docs/v1.0/09-A2A-PROTOCOL-SPECIFICATION.md`

---

**END OF TECHNICAL FOUNDATION**

*For architecture decisions: Focus on sections 1-4. For deployment: Review sections 4-5.*

