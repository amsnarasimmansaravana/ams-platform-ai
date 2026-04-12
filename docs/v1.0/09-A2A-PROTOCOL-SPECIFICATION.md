# A2A Protocol Specification

## AMS-AI: Multi-Agent Orchestration Platform

**Document Version:** 1.0
**Last Updated:** 2026-04-12
**Status:** Complete Protocol Specification
**Protocol Status:** Ready for Implementation & External Adoption

---

## 1. Overview & Protocol Architecture

### 1.1 Introduction

AMS-AI implements the **Agent-to-Agent (A2A) Protocol v1.0**, an open standard for agent discovery, capability advertisement, and inter-agent communication. A2A enables:

- **Interoperability** - Agents from LangChain, AutoGen, CrewAI, and custom frameworks communicate seamlessly
- **Framework-Agnostic** - Core logic independent of specific AI implementation details
- **Capability-Driven** - Agents advertise skills, others discover and invoke dynamically
- **Enterprise-Ready** - Built-in security, streaming, async patterns, error handling
- **Production-Proven** - Tested with LLM agents, workflow agents, and external services

### 1.2 Why A2A Protocol

| Benefit | Description | Use Case |
|---------|-------------|----------|
| **Interoperability** | Agents from different frameworks communicate natively | LangChain agent calling AutoGen agent |
| **Discovery** | Dynamic skill/capability discovery without hardcoding | Marketplace of agent capabilities |
| **Standardization** | Common interface across vendors | Enterprise integration standards |
| **Security** | Built-in auth, encryption, rate limiting | Secure multi-tenant execution |
| **Flexibility** | Async, streaming, long-polling patterns | Real-time vs batch workflows |

### 1.3 A2A Protocol Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    AGENT-TO-AGENT PROTOCOL STACK                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  DISCOVERY LAYER (Agent Capability Discovery)                            │
│  ├─ Agent Card Publication (/.well-known/agent.json)                     │
│  ├─ Capability Indexing (Full-text skill search)                          │
│  └─ Registry Integration (Onboarding, versioning)                         │
│                                                                           │
│  COMMUNICATION LAYER (Task Execution Patterns)                            │
│  ├─ Synchronous RPC (Request-Response, blocking)                          │
│  ├─ Asynchronous Queue (Fire-and-forget with polling)                     │
│  ├─ Streaming (Server-Sent Events, real-time updates)                     │
│  └─ Callback (Webhook-based notifications)                               │
│                                                                           │
│  MESSAGE LAYER (Protocol Messages & Schemas)                             │
│  ├─ Task Message (Input + metadata)                                       │
│  ├─ Result Message (Output + execution info)                              │
│  ├─ Error Message (Structured error responses)                            │
│  └─ Event Message (State transitions, progress updates)                   │
│                                                                           │
│  TRANSPORT LAYER (HTTP/TLS, gRPC - future)                               │
│  ├─ HTTP POST/GET with TLS 1.3                                            │
│  ├─ Authentication (Bearer, API Key, mTLS, OAuth2)                        │
│  └─ Rate Limiting (Token bucket, backpressure)                            │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.4 A2A in AMS-AI Context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AMS-AI PLATFORM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     A2A PROTOCOL LAYER                               │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │   Agent Discovery    Agent Communication    Task Management         │   │
│  │   (Agent Cards)      (Messages/Tasks)       (Lifecycle)             │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐            │
│         │                          │                          │            │
│         ▼                          ▼                          ▼            │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐        │
│  │  Internal   │          │  External   │          │  Framework  │        │
│  │   Agents    │          │   Agents    │          │   Agents    │        │
│  │  (AMS-AI)   │          │  (Remote)   │          │ (LangChain) │        │
│  └─────────────┘          └─────────────┘          └─────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Discovery Layer & Agent Card

### 2.1 Agent Card Overview

The **Agent Card** is the core identity document for any agent in the A2A protocol. It describes the agent's capabilities, endpoints, authentication requirements, and supported interaction modes.

### 2.2 Agent Card Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Unique agent identifier"
    },
    "displayName": {
      "type": "string",
      "description": "Human-readable agent name"
    },
    "description": {
      "type": "string",
      "description": "Agent description for discovery and LLM understanding"
    },
    "version": {
      "type": "string",
      "description": "Agent version (semver)"
    },
    "url": {
      "type": "string",
      "format": "uri",
      "description": "Agent's A2A endpoint URL"
    },
    "provider": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "url": { "type": "string", "format": "uri" }
      }
    },
    "capabilities": {
      "type": "object",
      "properties": {
        "streaming": { "type": "boolean" },
        "pushNotifications": { "type": "boolean" },
        "stateTransitionHistory": { "type": "boolean" }
      }
    },
    "authentication": {
      "type": "object",
      "properties": {
        "schemes": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["bearer", "api_key", "oauth2", "mtls", "none"]
          }
        },
        "credentials": { "type": "string" }
      }
    },
    "skills": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/skill"
      }
    },
    "defaultInputModes": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["text", "file", "data"]
      }
    },
    "defaultOutputModes": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["text", "file", "data"]
      }
    }
  },
  "required": ["name", "description", "version", "url", "skills"],
  "$defs": {
    "skill": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "inputSchema": { "type": "object" },
        "outputSchema": { "type": "object" },
        "tags": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["id", "name", "description"]
    }
  }
}
```

### 2.3 Agent Card Examples

#### 2.3.1 LLM Agent Card

```json
{
  "name": "customer-support-agent",
  "displayName": "Customer Support Agent",
  "description": "An intelligent agent that handles customer support queries, can access knowledge bases, create support tickets, and escalate to human agents when needed.",
  "version": "1.2.0",
  "url": "https://agents.ams-ai.example.com/a2a/customer-support-agent",
  "provider": {
    "name": "AMS-AI Platform",
    "url": "https://ams-ai.example.com"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "authentication": {
    "schemes": ["bearer", "api_key"],
    "credentials": "Authorization header or X-API-Key header"
  },
  "skills": [
    {
      "id": "answer-query",
      "name": "Answer Customer Query",
      "description": "Answers customer questions using knowledge base and conversation history",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "customerId": { "type": "string" },
          "conversationHistory": { "type": "array" }
        },
        "required": ["query"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "response": { "type": "string" },
          "confidence": { "type": "number" },
          "sources": { "type": "array" }
        }
      },
      "tags": ["customer-service", "qa", "support"]
    },
    {
      "id": "create-ticket",
      "name": "Create Support Ticket",
      "description": "Creates a support ticket in the ticketing system",
      "inputSchema": {
        "type": "object",
        "properties": {
          "subject": { "type": "string" },
          "description": { "type": "string" },
          "priority": { "type": "string", "enum": ["low", "medium", "high", "urgent"] },
          "customerId": { "type": "string" }
        },
        "required": ["subject", "description"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "ticketId": { "type": "string" },
          "status": { "type": "string" }
        }
      },
      "tags": ["ticketing", "support"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"]
}
```

#### 2.3.2 Workflow Agent Card

```json
{
  "name": "data-pipeline-agent",
  "displayName": "Data Pipeline Agent",
  "description": "A workflow agent that processes data through configurable transformation pipelines including validation, transformation, and loading.",
  "version": "2.0.0",
  "url": "https://agents.ams-ai.example.com/a2a/data-pipeline-agent",
  "provider": {
    "name": "AMS-AI Platform",
    "url": "https://ams-ai.example.com"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "authentication": {
    "schemes": ["bearer", "mtls"]
  },
  "skills": [
    {
      "id": "validate-data",
      "name": "Validate Data",
      "description": "Validates input data against a schema",
      "inputSchema": {
        "type": "object",
        "properties": {
          "data": { "type": "object" },
          "schema": { "type": "object" }
        },
        "required": ["data", "schema"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "valid": { "type": "boolean" },
          "errors": { "type": "array" }
        }
      },
      "tags": ["data", "validation"]
    },
    {
      "id": "transform-data",
      "name": "Transform Data",
      "description": "Applies transformations to data",
      "inputSchema": {
        "type": "object",
        "properties": {
          "data": { "type": "object" },
          "transformations": { "type": "array" }
        }
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "transformedData": { "type": "object" },
          "appliedTransformations": { "type": "array" }
        }
      },
      "tags": ["data", "transformation", "etl"]
    }
  ],
  "defaultInputModes": ["data", "file"],
  "defaultOutputModes": ["data", "file"]
}
```

---

## 3. A2A Communication Patterns & Error Handling

### 3.1 Core Interaction Models

The A2A Protocol supports multiple communication patterns optimized for different use cases:

#### Model 1: Synchronous RPC (Request-Response)
- **Use Case:** Real-time responses, short tasks (< 10 seconds)
- **Pattern:** Client blocks waiting for response
- **Latency:** 30-200ms p95 target
- **Reliability:** Connection-level (client retries on network failure)
- **Best For:** Chat interfaces, immediate feedback needed

#### Model 2: Asynchronous Queue
- **Use Case:** Long-running tasks (30s - 1 hour)
- **Pattern:** Client receives task ID immediately, polls for status
- **Latency:** 100ms p95 for polling endpoint
- **Reliability:** Task persisted, retriable
- **Best For:** Batch processing, heavy computations

#### Model 3: Server-Sent Events (Streaming)
- **Use Case:** Real-time streaming output, progress updates
- **Pattern:** Server pushes updates to client over persistent connection
- **Latency:** 50ms p95 for stream updates
- **Reliability:** Connection-based (reconnect on failure)
- **Best For:** LLM token streaming, live updates

#### Model 4: Webhook Callbacks
- **Use Case:** Notification when async task completes
- **Pattern:** Agent calls back to provided webhook URL
- **Latency:** Variable (depends on network latency)
- **Reliability:** Retry policy with exponential backoff
- **Best For:** Integration with external systems

---

### 3.2 Error Handling

All A2A errors use standardized error response format:

```json
{
  "taskId": "task_uuid",
  "status": "FAILED",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { "field": "error details" },
    "retryable": true,
    "retryAfterSeconds": 5
  }
}
```

**Standard Error Codes:**

| Code | Cause | Retryable | Action |
|------|-------|-----------|--------|
| INVALID_INPUT | Input doesn't match schema | No | Fix input, resubmit |
| AUTHENTICATION_FAILED | Auth credentials invalid | No | Verify credentials |
| RATE_LIMIT_EXCEEDED | Too many requests | Yes | Backoff & retry |
| SKILL_NOT_FOUND | Requested skill unknown | No | Verify skill exists |
| AGENT_INTERNAL_ERROR | Unhandled exception | Yes | Retry with backoff |
| EXTERNAL_SERVICE_ERROR | Dependency failure (LLM down) | Yes | Retry or fallback |
| TIMEOUT | Task exceeded timeout | Maybe | Increase timeout, retry |
| RESOURCE_EXHAUSTED | Agent at capacity | Yes | Queue, retry later |

---

## 4. Task Lifecycle & Management

## 3. A2A Endpoints

### 3.1 Required Endpoints

Every A2A-compliant agent must implement these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent.json` | GET | Returns the Agent Card |
| `/a2a/tasks` | POST | Create a new task |
| `/a2a/tasks/{taskId}` | GET | Get task status |
| `/a2a/tasks/{taskId}` | DELETE | Cancel a task |
| `/a2a/tasks/{taskId}/messages` | POST | Send a message to a task |
| `/a2a/tasks/{taskId}/messages` | GET | Get task messages |

### 3.2 Optional Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/a2a/tasks/{taskId}/stream` | GET (SSE) | Stream task updates |
| `/a2a/tasks/{taskId}/artifacts` | GET | Get task artifacts |
| `/a2a/health` | GET | Health check |

### 3.3 Endpoint Specifications

#### 3.3.1 Agent Card Discovery

```http
GET /.well-known/agent.json HTTP/1.1
Host: agents.example.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "name": "customer-support-agent",
  "description": "...",
  ...
}
```

#### 3.3.2 Create Task

```http
POST /a2a/tasks HTTP/1.1
Host: agents.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "skillId": "answer-query",
  "input": {
    "parts": [
      {
        "type": "text",
        "content": "How do I reset my password?"
      }
    ]
  },
  "metadata": {
    "conversationId": "conv-123",
    "customerId": "cust-456"
  },
  "config": {
    "timeout": 30000,
    "priority": "normal"
  }
}
```

**Response:**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "taskId": "task-789",
  "status": "pending",
  "createdAt": "2026-01-25T10:30:00Z",
  "skillId": "answer-query"
}
```

#### 3.3.3 Get Task Status

```http
GET /a2a/tasks/task-789 HTTP/1.1
Host: agents.example.com
Authorization: Bearer <token>

HTTP/1.1 200 OK
Content-Type: application/json

{
  "taskId": "task-789",
  "status": "completed",
  "createdAt": "2026-01-25T10:30:00Z",
  "completedAt": "2026-01-25T10:30:05Z",
  "skillId": "answer-query",
  "output": {
    "parts": [
      {
        "type": "text",
        "content": "To reset your password, go to Settings > Security > Reset Password..."
      }
    ]
  },
  "artifacts": [],
  "history": [
    {"status": "pending", "timestamp": "2026-01-25T10:30:00Z"},
    {"status": "running", "timestamp": "2026-01-25T10:30:01Z"},
    {"status": "completed", "timestamp": "2026-01-25T10:30:05Z"}
  ]
}
```

---

## 4. Task Lifecycle

### 4.1 Task States

```
┌─────────────────────────────────────────────────────────────────┐
│                      TASK STATE MACHINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                        ┌─────────┐                              │
│              ┌─────────│ pending │─────────┐                    │
│              │         └────┬────┘         │                    │
│              │              │              │                    │
│              │              ▼              │                    │
│              │         ┌─────────┐         │                    │
│              │         │ running │         │                    │
│              │         └────┬────┘         │                    │
│              │              │              │                    │
│              │    ┌─────────┼─────────┐    │                    │
│              │    │         │         │    │                    │
│              ▼    ▼         ▼         ▼    ▼                    │
│         ┌────────┐  ┌───────────┐  ┌────────┐                  │
│         │ failed │  │ completed │  │canceled│                  │
│         └────────┘  └───────────┘  └────────┘                  │
│                                                                 │
│  Additional States:                                             │
│  - input_required: Waiting for additional input                │
│  - blocked: Waiting for external dependency                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Task State Definitions

| State | Description |
|-------|-------------|
| `pending` | Task created, waiting to be processed |
| `running` | Task is being executed |
| `completed` | Task completed successfully |
| `failed` | Task failed with error |
| `canceled` | Task was canceled |
| `input_required` | Agent needs additional input to continue |
| `blocked` | Task blocked waiting for external resource |

---

## 5. Message Format

### 5.1 Message Structure

```json
{
  "messageId": "msg-uuid",
  "role": "user | agent",
  "timestamp": "2026-01-25T10:30:00Z",
  "parts": [
    {
      "type": "text | file | data",
      "content": "...",
      "mimeType": "text/plain",
      "metadata": {}
    }
  ]
}
```

### 5.2 Message Part Types

#### Text Part

```json
{
  "type": "text",
  "content": "What is the status of order #12345?"
}
```

#### File Part

```json
{
  "type": "file",
  "content": "base64-encoded-content-or-url",
  "mimeType": "application/pdf",
  "filename": "invoice.pdf",
  "size": 102400
}
```

#### Data Part

```json
{
  "type": "data",
  "content": {
    "orderId": "12345",
    "items": [...]
  },
  "schema": "https://schemas.example.com/order.json"
}
```

---

## 6. Agent Onboarding via A2A

### 6.1 Onboarding Process

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        A2A AGENT ONBOARDING FLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. REGISTRATION                                                            │
│  ┌──────────────┐                                                          │
│  │ User submits │ ──► Agent URL or Agent Card JSON                         │
│  │ agent info   │                                                          │
│  └──────────────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  2. DISCOVERY                                                               │
│  ┌──────────────┐                                                          │
│  │ Platform     │ ──► GET /.well-known/agent.json                          │
│  │ fetches card │     (if URL provided)                                    │
│  └──────────────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  3. VALIDATION                                                              │
│  ┌──────────────┐                                                          │
│  │ Validate     │ ──► Schema validation                                    │
│  │ Agent Card   │ ──► Endpoint reachability                                │
│  │              │ ──► Authentication test                                  │
│  └──────────────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  4. CAPABILITY INDEXING                                                     │
│  ┌──────────────┐                                                          │
│  │ Index skills │ ──► Store skills for discovery                           │
│  │ and metadata │ ──► Generate embeddings for semantic search              │
│  └──────────────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  5. HEALTH CHECK SETUP                                                      │
│  ┌──────────────┐                                                          │
│  │ Configure    │ ──► Periodic health checks                               │
│  │ monitoring   │ ──► Alerting rules                                       │
│  └──────────────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  6. ACTIVATION                                                              │
│  ┌──────────────┐                                                          │
│  │ Agent        │ ──► Available for orchestrations                         │
│  │ activated    │ ──► Discoverable by other agents                         │
│  └──────────────┘                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Onboarding API

#### Register Agent via URL

```http
POST /api/v1/agents/register HTTP/1.1
Content-Type: application/json

{
  "type": "a2a",
  "agentUrl": "https://external-agent.example.com",
  "authentication": {
    "scheme": "bearer",
    "token": "secret-token"
  },
  "organizationId": "org-123",
  "projectId": "proj-456",
  "tags": ["customer-service", "external"]
}
```

#### Register Agent via Agent Card

```http
POST /api/v1/agents/register HTTP/1.1
Content-Type: application/json

{
  "type": "a2a",
  "agentCard": {
    "name": "my-custom-agent",
    "description": "...",
    "url": "https://my-agent.example.com/a2a",
    "skills": [...]
  },
  "authentication": {
    "scheme": "api_key",
    "apiKey": "my-api-key"
  },
  "organizationId": "org-123"
}
```

### 6.3 Agent Types in A2A Context

| Agent Type | Hosting | A2A Role |
|------------|---------|----------|
| **Internal Agent** | Hosted by AMS-AI | A2A Server (exposes endpoints) |
| **External Agent** | Hosted externally | A2A Server (platform calls) |
| **Platform Client** | N/A | A2A Client (calls agents) |

---

## 7. Agent Discovery

### 7.1 Discovery Mechanisms

| Mechanism | Description |
|-----------|-------------|
| **Registry Search** | Search agents by name, skills, tags |
| **Capability Matching** | Find agents with specific capabilities |
| **Semantic Search** | Natural language search for agent skills |
| **Federation** | Discover agents from federated registries |

### 7.2 Discovery API

#### Search Agents

```http
GET /api/v1/agents/discover?q=customer+support&capabilities=streaming HTTP/1.1

HTTP/1.1 200 OK
{
  "agents": [
    {
      "name": "customer-support-agent",
      "description": "...",
      "skills": [...],
      "relevanceScore": 0.95
    }
  ],
  "total": 5,
  "page": 1
}
```

#### Find by Skill

```http
POST /api/v1/agents/discover/by-skill HTTP/1.1
Content-Type: application/json

{
  "skillDescription": "I need an agent that can analyze sentiment in customer feedback",
  "requiredCapabilities": ["streaming"],
  "maxResults": 10
}
```

---

## 8. Inter-Agent Communication

### 8.1 Communication Patterns

#### 8.1.1 Request-Response

```
┌─────────┐         ┌─────────┐
│ Agent A │ ──────► │ Agent B │
│         │ ◄────── │         │
└─────────┘ request └─────────┘
            response
```

#### 8.1.2 Streaming

```
┌─────────┐         ┌─────────┐
│ Agent A │ ──────► │ Agent B │
│         │ ◄═════► │         │  (SSE stream)
└─────────┘         └─────────┘
```

#### 8.1.3 Multi-Agent Conversation

```
┌─────────┐    ┌───────────────┐    ┌─────────┐
│ Agent A │───►│ Orchestrator  │◄───│ Agent B │
└─────────┘    │               │    └─────────┘
               │  Coordinates  │
┌─────────┐    │   messages    │    ┌─────────┐
│ Agent C │◄───│               │───►│ Agent D │
└─────────┘    └───────────────┘    └─────────┘
```

### 8.2 Communication in Orchestration

```yaml
# Workflow using A2A agents
name: multi-agent-support-flow
nodes:
  - id: classify
    type: a2a_agent
    agent: "intent-classifier"  # A2A agent reference
    skill: "classify-intent"
    input:
      text: "{{ input.query }}"

  - id: support
    type: a2a_agent
    agent: "customer-support-agent"
    skill: "answer-query"
    input:
      query: "{{ input.query }}"
      context: "{{ classify.output }}"
    capabilities:
      streaming: true  # Request streaming response

edges:
  - from: classify
    to: support
```

---

## 9. Authentication & Security

### 9.1 Supported Authentication Schemes

| Scheme | Description | Use Case |
|--------|-------------|----------|
| `bearer` | JWT or opaque token | Standard API authentication |
| `api_key` | Static API key | Simple integrations |
| `oauth2` | OAuth 2.0 flow | Delegated authorization |
| `mtls` | Mutual TLS | High-security environments |
| `none` | No authentication | Public agents (rare) |

### 9.2 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   A2A AUTHENTICATION FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Client reads Agent Card                                     │
│     GET /.well-known/agent.json                                 │
│                                                                 │
│  2. Client checks authentication.schemes                        │
│     ["bearer", "api_key"]                                       │
│                                                                 │
│  3. Client obtains credentials                                  │
│     - From AMS-AI secrets store                                 │
│     - From OAuth token exchange                                 │
│     - From configured API key                                   │
│                                                                 │
│  4. Client makes authenticated request                          │
│     POST /a2a/tasks                                             │
│     Authorization: Bearer <token>                               │
│                                                                 │
│  5. Agent validates credentials                                 │
│     - Verify token signature                                    │
│     - Check permissions/scopes                                  │
│     - Rate limiting                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 Credential Management

| Feature | Description |
|---------|-------------|
| Secure Storage | Credentials stored encrypted in Vault |
| Rotation | Automated credential rotation |
| Scoping | Per-agent, per-skill credential scoping |
| Audit | All credential usage logged |

---

## 10. Error Handling

### 10.1 Error Response Format

```json
{
  "error": {
    "code": "SKILL_NOT_FOUND",
    "message": "The requested skill 'unknown-skill' does not exist",
    "details": {
      "availableSkills": ["answer-query", "create-ticket"]
    },
    "timestamp": "2026-01-25T10:30:00Z",
    "requestId": "req-123"
  }
}
```

### 10.2 Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials |
| `PERMISSION_DENIED` | 403 | Insufficient permissions |
| `AGENT_NOT_FOUND` | 404 | Agent does not exist |
| `SKILL_NOT_FOUND` | 404 | Skill does not exist |
| `TASK_NOT_FOUND` | 404 | Task does not exist |
| `RATE_LIMITED` | 429 | Too many requests |
| `AGENT_UNAVAILABLE` | 503 | Agent is not available |
| `TASK_TIMEOUT` | 504 | Task execution timed out |

---

## 11. Streaming Protocol

### 11.1 Server-Sent Events (SSE)

```http
GET /a2a/tasks/task-123/stream HTTP/1.1
Accept: text/event-stream
Authorization: Bearer <token>

HTTP/1.1 200 OK
Content-Type: text/event-stream

event: status
data: {"status": "running", "timestamp": "2026-01-25T10:30:01Z"}

event: output
data: {"type": "text", "content": "Analyzing your request..."}

event: output
data: {"type": "text", "content": "Based on your query, here's what I found:"}

event: output
data: {"type": "text", "content": "To reset your password..."}

event: status
data: {"status": "completed", "timestamp": "2026-01-25T10:30:05Z"}

event: done
data: {"taskId": "task-123"}
```

### 11.2 Event Types

| Event | Description |
|-------|-------------|
| `status` | Task status change |
| `output` | Output part from agent |
| `artifact` | File/data artifact created |
| `error` | Error occurred |
| `done` | Stream complete |

---

## 12. Push Notifications

### 12.1 Webhook Configuration

```json
{
  "pushNotifications": {
    "enabled": true,
    "url": "https://callback.example.com/a2a/webhooks",
    "events": ["task.completed", "task.failed"],
    "authentication": {
      "scheme": "bearer",
      "token": "webhook-secret"
    },
    "retry": {
      "maxAttempts": 3,
      "backoff": "exponential"
    }
  }
}
```

### 12.2 Webhook Payload

```json
{
  "event": "task.completed",
  "timestamp": "2026-01-25T10:30:05Z",
  "task": {
    "taskId": "task-123",
    "status": "completed",
    "output": {...}
  },
  "signature": "sha256=abc123..."
}
```

---

## 13. Platform Extensions

### 13.1 AMS-AI A2A Extensions

AMS-AI extends the base A2A protocol with platform-specific features:

| Extension | Description |
|-----------|-------------|
| `x-ams-organization` | Organization context |
| `x-ams-project` | Project context |
| `x-ams-trace-id` | Distributed tracing |
| `x-ams-cost-tracking` | Token/cost attribution |
| `x-ams-audit` | Audit metadata |

### 13.2 Extended Agent Card

```json
{
  "name": "my-agent",
  "...": "...",
  "x-ams-extensions": {
    "costPerInvocation": {
      "currency": "USD",
      "estimate": 0.002
    },
    "sla": {
      "availability": 99.9,
      "latencyP95Ms": 500
    },
    "compliance": ["SOC2", "GDPR"],
    "dataResidency": ["us-east-1", "eu-west-1"]
  }
}
```

---

## 14. Implementation Checklist

### 14.1 For Internal Agents

- [ ] Implement `/.well-known/agent.json` endpoint
- [ ] Implement `/a2a/tasks` CRUD endpoints
- [ ] Implement `/a2a/tasks/{id}/messages` endpoint
- [ ] Implement SSE streaming (if supported)
- [ ] Implement webhook callbacks (if supported)
- [ ] Add authentication middleware
- [ ] Add rate limiting
- [ ] Add request validation
- [ ] Add error handling
- [ ] Add logging and tracing

### 14.2 For External Agent Integration

- [ ] Validate Agent Card schema
- [ ] Test endpoint reachability
- [ ] Verify authentication
- [ ] Test each declared skill
- [ ] Configure health monitoring
- [ ] Set up credential rotation
- [ ] Configure rate limiting
- [ ] Set up alerting

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | - | Initial draft |
