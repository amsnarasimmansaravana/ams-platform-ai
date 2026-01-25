# Glossary of Terms

## AMS-AI: Multi-Agent Orchestration Platform

**Document Version:** 1.0  
**Last Updated:** 2026-01-25  
**Status:** Draft

---

## A

### A2A Protocol
Agent-to-Agent Protocol. An open protocol that enables agents from different frameworks and vendors to discover each other's capabilities and collaborate on tasks. AMS-AI implements A2A as the standard for agent onboarding and inter-agent communication.

### A2A Client
A component that communicates with A2A-compliant agents, sending tasks and receiving responses.

### A2A Server
An agent that exposes A2A-compliant endpoints for receiving tasks and returning results.

### Agent
An autonomous software unit capable of performing tasks. In AMS-AI, agents can be:
- **LLM Agent**: Powered by a Large Language Model for natural language understanding and generation
- **Workflow Agent**: Executes predefined logic without LLM involvement
- **External Agent**: A2A-compliant agent hosted outside the platform

### Agent Card
A JSON document that describes an agent's identity, capabilities, skills, authentication requirements, and endpoints. Required by the A2A protocol for agent discovery and communication. Located at `/.well-known/agent.json`.

### Agent Registry
The central repository for managing agent definitions, configurations, and lifecycle states.

### API Gateway
The entry point for all API requests, handling routing, authentication, and rate limiting.

### Adapter
A component that provides a standardized interface to external systems (LLM providers, frameworks, tools).

### Artifact
A file or data object produced by an A2A task, such as generated documents, images, or structured data.

---

## B

### Business Rule
A specific, actionable directive that governs business operations and decisions within the platform.

---

## C

### Capability
A declared function or skill that an agent can perform (e.g., "summarization", "classification", "data-extraction").

### Conditional Pattern
An orchestration pattern that routes execution based on conditions evaluated at runtime.

### Connection (Edge)
A link between two nodes in a workflow that defines data flow and execution order.

---

## D

### Deployment
A running instance of an orchestration configured for a specific environment (development, staging, production).

### Directed Graph
A graph structure where edges have direction, used to represent workflow execution flow.

---

## E

### Execution Engine
The core component responsible for running workflows, managing state, and coordinating agent/tool invocations.

### Edge
See **Connection**.

---

## F

### Framework Adapter
An adapter that integrates external agent frameworks (LangChain, AutoGen, CrewAI) into the AMS-AI platform.

### Fan-out
Splitting execution into multiple parallel branches.

### Fan-in
Merging multiple parallel branches back into a single execution path.

---

## G

### GA (General Availability)
A software release that is stable and ready for production use.

---

## H

### Hierarchical Pattern
An orchestration pattern where a parent agent delegates tasks to child agents.

---

## I

### Input Schema
A JSON Schema definition specifying the expected structure and validation rules for input data.

---

## J

### JSON Schema
A vocabulary for annotating and validating JSON documents, used for defining input/output schemas.

---

## L

### LLM (Large Language Model)
An AI model trained on large text datasets capable of understanding and generating natural language.

### LLM Agent
An agent that uses an LLM for its core reasoning and response generation.

### Loop Pattern
An orchestration pattern that repeats execution until a condition is met.

---

## M

### Message Bus
Internal communication system for asynchronous messaging between components.

### Multi-Agent System
A system composed of multiple agents working together to accomplish tasks.

---

## N

### Node
A single unit in a workflow graph representing an agent, tool, or control logic.

**Node Types:**
- **Agent Node**: Executes an agent
- **Tool Node**: Invokes a tool
- **Start Node**: Entry point of workflow
- **End Node**: Exit point of workflow
- **Condition Node**: Branching logic
- **Loop Node**: Iteration control
- **Parallel Node**: Splits execution
- **Join Node**: Merges parallel branches
- **Transform Node**: Data transformation
- **Subflow Node**: Nested workflow

---

## O

### Orchestration
A workflow definition that combines multiple agents, tools, and control logic to accomplish a complex task.

### Orchestration Builder
The module responsible for creating, validating, and managing workflow definitions.

### Output Schema
A JSON Schema definition specifying the expected structure of output data.

---

## P

### Parallel Pattern
An orchestration pattern that executes multiple nodes simultaneously.

### Pattern
A reusable orchestration structure (sequential, parallel, conditional, loop, router, hierarchical).

### Plugin
An extension module that adds functionality to the platform without modifying core code.

### Provider
An external service that provides capabilities (e.g., OpenAI as an LLM provider).

---

## R

### RBAC (Role-Based Access Control)
A security model where permissions are assigned to roles, and users are assigned to roles.

### Router Pattern
An orchestration pattern that dynamically routes execution based on content analysis.

### Run
A single execution instance of a deployed orchestration.

### Run Step
A single node execution within a run.

---

## S

### Sandbox
An isolated execution environment for running untrusted code safely.

### Schema
A formal definition of data structure and validation rules.

### Sequential Pattern
An orchestration pattern that executes nodes in a defined order, one after another.

### Semantic Versioning
A versioning scheme using MAJOR.MINOR.PATCH format to indicate compatibility.

### Skill
In A2A protocol, a specific capability that an agent can perform. Each skill has:
- Unique identifier
- Name and description
- Input/output schemas
- Tags for discovery

### SSE (Server-Sent Events)
A protocol for streaming real-time updates from server to client. Used in A2A for task output streaming.

### Subflow
A nested workflow that can be referenced and executed from a parent workflow.

---

## T

### Task (A2A)
A unit of work sent to an agent via the A2A protocol. Tasks have:
- Unique identifier
- Status (pending, running, completed, failed, canceled)
- Input message
- Output message (when completed)
- State history

### Task State
The current status of an A2A task:
- **pending**: Created, awaiting processing
- **running**: Currently being executed
- **completed**: Successfully finished
- **failed**: Terminated with error
- **canceled**: Terminated by request
- **input_required**: Waiting for additional input
- **blocked**: Waiting for external dependency

### Tool
An external capability that agents can invoke, such as API calls, database queries, or file operations.

**Tool Types:**
- **HTTP Tool**: Makes REST API calls
- **Database Tool**: Performs database operations
- **Filesystem Tool**: Handles file operations
- **Custom Tool**: User-defined functionality

### Tool Registry
The central repository for managing tool definitions and configurations.

---

## V

### Validation
The process of checking workflow integrity, schema compliance, and dependency resolution.

### Version
A specific release of an agent, tool, or workflow identified by a version number.

---

## W

### WebSocket
A protocol providing full-duplex communication channels over TCP, used for real-time updates.

### Workflow
See **Orchestration**.

### Workflow Agent
An agent that executes predefined logic without LLM involvement.

### Workflow Engine
See **Execution Engine**.

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | - | Initial draft |
