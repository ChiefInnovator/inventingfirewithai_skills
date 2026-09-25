# Microsoft Agent Skills Research for .NET, Azure, Python, React, TypeScript, Microsoft Foundry, and Related Platforms

**Prepared for:** Rich Crane  
**Prepared on:** May 02, 2026, 11:47 AM EST  
**Focus:** Microsoft aligned skills for Claude Code, Codex, GitHub Copilot, Cursor, OpenCode, Gemini CLI, and other Agent Skills compatible coding agents.

## Executive Summary

Microsoft now has a real skills ecosystem for AI coding agents.

The most important repository is:

https://github.com/microsoft/skills

It contains skills, custom agents, AGENTS.md templates, and MCP configurations for AI coding agents working with Azure SDKs and Microsoft Foundry. The repo includes skills for Python, .NET, TypeScript, Java, Rust, Azure SDKs, Microsoft Foundry, Microsoft 365 Agents, AI Search, Azure OpenAI, Cosmos DB, Azure Identity, Key Vault, monitoring, messaging, frontend UI, and more.

The most important guidance from Microsoft is:

1. Do not load every skill.
2. Pick only the skills essential to the current project.
3. Too many skills create context rot.
4. Use skills as high signal activation context for SDK and platform patterns.
5. Pair skills with MCP servers only when the task needs live docs, GitHub, browser automation, Azure operations, or deployment tooling.

## Primary Microsoft Skill Sources

## 1. Microsoft Agent Skills Repository

**Best use case:** Core source for Microsoft and Azure SDK skills.

Repository:

https://github.com/microsoft/skills

Microsoft describes this repository as a collection of skills, custom agents, AGENTS.md templates, and MCP configurations for AI coding agents working with Azure SDKs and Microsoft AI Foundry.

Install:

```bash
npx skills add microsoft/skills
```

The repository currently lists:

1. Core skills.
2. Python skills.
3. .NET skills.
4. TypeScript skills.
5. Java skills.
6. Rust skills.
7. Custom agents.
8. AGENTS.md templates.
9. MCP configurations.

Important Microsoft guidance:

```text
Use skills selectively. Loading all skills causes context rot: diluted attention, wasted tokens, conflated patterns. Only copy skills essential for your current project.
```

## 2. Microsoft Agent Skills Web Catalog

**Best use case:** Browsing and installing individual skills.

Catalog:

https://microsoft.github.io/skills/

This is the easiest way to browse Microsoft skills and pick individual skills instead of cloning the entire repository.

Use this when:

1. You know the technology category.
2. You want one skill at a time.
3. You want install commands.
4. You want to avoid copying the entire catalog.

## 3. Microsoft Azure Skills Plugin

**Best use case:** Azure operations, deployment workflows, diagnostics, cost, compliance, RBAC, and MCP backed execution.

Repository:

https://github.com/microsoft/azure-skills

Microsoft describes this as an official Azure Skills Plugin that packages Azure expertise and MCP backed execution so compatible coding agents can do real Azure work instead of giving generic cloud advice.

Use this when the agent needs to:

1. Choose Azure services.
2. Prepare deployment.
3. Validate infrastructure.
4. Deploy Azure resources.
5. Diagnose Azure failures.
6. Check cost and compliance.
7. Work with RBAC.
8. Use Azure and Foundry MCP servers.

Important skills in this plugin include:

1. `azure-prepare`
2. `azure-validate`
3. `azure-deploy`
4. `microsoft-foundry`

Microsoft Learn article for the Foundry skill:

https://learn.microsoft.com/en-us/azure/developer/azure-skills/skills/microsoft-foundry

## 4. MicrosoftDocs Agent Skills

**Best use case:** Azure service level skills generated from Microsoft Learn style knowledge.

Repository:

https://github.com/MicrosoftDocs/Agent-Skills

Catalog:

https://github.com/MicrosoftDocs/Agent-Skills/blob/main/docs/CATALOG.md

This repository contains curated Agent Skills for Microsoft and Azure. It says skills are folders containing markdown instructions, scripts, and resources that teach AI agents how to work with Azure services correctly.

It includes a very large Azure service catalog, including:

1. Azure AI Foundry Local.
2. Microsoft Foundry.
3. Azure Functions.
4. Azure App Service.
5. Azure API Management.
6. Azure Service Bus.
7. Azure Event Grid.
8. Azure Event Hubs.
9. Azure Storage.
10. Azure Key Vault.
11. Azure RBAC.
12. Azure Security.
13. Azure Monitor.
14. Azure Cosmos DB.
15. Azure AI Search.
16. Azure Machine Learning.
17. Azure OpenAI related services.
18. Azure Networking.
19. Azure IoT.

## 5. Microsoft Foundry Skill

**Best use case:** Model discovery, model deployment, Foundry agent lifecycle, evaluation, troubleshooting, hosted agents, and prompt optimization.

Source code:

https://github.com/microsoft/azure-skills/blob/main/skills/microsoft-foundry/SKILL.md

GitHub Copilot for Azure version:

https://github.com/microsoft/GitHub-Copilot-for-Azure/blob/main/plugin/skills/microsoft-foundry/SKILL.md

Microsoft Learn:

https://learn.microsoft.com/en-us/azure/developer/azure-skills/skills/microsoft-foundry

Use this skill when working with:

1. Microsoft Foundry resources.
2. Model discovery.
3. Model deployment.
4. Hosted agents.
5. Prompt agents.
6. Agent evaluation.
7. Prompt optimization.
8. Agent tracing.
9. Hosted agent logs.
10. Docker build and ACR push.
11. Agent YAML.
12. Dataset curation from traces.

## 6. Foundry Hosted Agent Skills REST API

**Best use case:** Storing and managing `SKILL.md` files inside Microsoft Foundry for hosted agents.

Microsoft Learn:

https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/skills

This is important because it confirms Microsoft Foundry itself now supports skill management for hosted agents through a Skills REST API.

Use this when:

1. You want centrally stored skills in a Foundry project.
2. You want hosted agents to use downloaded `SKILL.md` files.
3. You want skill CRUD operations.
4. You want skills bundled into hosted agent containers.

Important detail:

```text
Use skills in hosted agents only. The Skills REST API handles storage and retrieval. Your agent code bundles the downloaded SKILL.md files into the container image and loads them when creating sessions.
```

## 7. Azure Scaffold Wizard

**Best use case:** Scaffolding production ready Azure applications.

Repository:

https://github.com/microsoft/Foundry-AI-solution-templates-creation

Microsoft describes this as a universal AI agent skill that scaffolds complete, production ready Azure projects through adaptive questioning.

Install:

```bash
npx skills add microsoft/Foundry-AI-solution-templates-creation
```

Use it for:

1. RAG chatbots.
2. Multi agent systems.
3. API backends.
4. Data pipelines.
5. Azure project scaffolding.
6. Production ready Azure patterns.

## 8. Microsoft Agent Framework

**Best use case:** Building and orchestrating AI agents and multi agent workflows in .NET and Python.

GitHub:

https://github.com/microsoft/agent-framework

Docs:

https://learn.microsoft.com/en-us/agent-framework/

Overview:

https://learn.microsoft.com/en-us/agent-framework/overview/

Workflows:

https://learn.microsoft.com/en-us/agent-framework/workflows/

Microsoft describes Agent Framework as a framework for building, orchestrating, and deploying AI agents and multi agent workflows with support for Python and .NET.

Use this for:

1. .NET agents.
2. Python agents.
3. Multi agent workflows.
4. Workflow orchestration.
5. Streaming.
6. Checkpointing.
7. Human in the loop.
8. Telemetry.
9. Enterprise grade agent systems.

## 9. Microsoft Foundry Documentation and SDKs

**Best use case:** Grounding skills and agents in official Foundry behavior.

Foundry documentation:

https://learn.microsoft.com/en-us/azure/foundry/

What is Microsoft Foundry:

https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

SDK overview:

https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview

Quickstart:

https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code

Python AI Projects SDK:

https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme?view=azure-python

Microsoft says the Foundry API provides a consistent contract for building agentic applications across model providers, with SDK client libraries for Python, C#, JavaScript and TypeScript, and Java.

# Recommended Skill Set by Technology

## .NET Skills

Use these when building C#, ASP.NET Core, .NET workers, Azure SDK apps, AI agents, or infrastructure management tools.

### Must Have

1. `azure-ai-projects-dotnet`

   Foundry project client, agents, connections, and evaluations.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-ai-projects-dotnet

2. `azure-ai-openai-dotnet`

   Azure OpenAI chat, embeddings, image generation, audio, and assistants.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-ai-openai-dotnet

3. `azure-search-documents-dotnet`

   Azure AI Search, full text search, vector search, semantic search, and hybrid search.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-search-documents-dotnet

4. `m365-agents-dotnet`

   Microsoft 365 Agents SDK with ASP.NET Core hosting, AgentApplication routing, and Copilot Studio client.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/m365-agents-dotnet

5. `azure-identity-dotnet`

   DefaultAzureCredential, managed identity, service principals, and Azure authentication.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-identity-dotnet

6. `azure-servicebus-dotnet`

   Queues, topics, sessions, dead letter handling, and enterprise messaging.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-servicebus-dotnet

### Strong Additions

1. `azure-resource-manager-sql-dotnet`
2. `azure-resource-manager-cosmosdb-dotnet`
3. `azure-mgmt-apimanagement-dotnet`
4. `azure-mgmt-applicationinsights-dotnet`
5. `azure-security-keyvault-keys-dotnet`
6. `azure-eventhub-dotnet`
7. `azure-eventgrid-dotnet`
8. `azure-ai-document-intelligence-dotnet`
9. `azure-ai-voicelive-dotnet`

## Python Skills

Use these when building FastAPI services, AI agents, SDK integrations, RAG systems, data pipelines, and Azure automation.

### Must Have

1. `agent-framework-azure-ai-py`

   Agent Framework SDK, persistent agents, hosted tools, MCP servers, and streaming.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/agent-framework-azure-ai-py

2. `azure-ai-projects-py`

   High level Foundry SDK, project client, versioned agents, evaluations, connections, and OpenAI compatible clients.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-ai-projects-py

3. `hosted-agents-v2-py`

   Hosted agents refreshed preview, protocol libraries, azd deployment, Python and .NET container hosts, dedicated endpoints.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/hosted-agents-v2-py

4. `azure-search-documents-py`

   Azure AI Search, vector search, hybrid search, semantic ranking, indexing, and skillsets.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-search-documents-py

5. `azure-cosmos-db-py`

   Production grade Cosmos DB service layer with FastAPI patterns, dual authentication, partitioning, parameterized queries, and TDD.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-cosmos-db-py

6. `fastapi-router-py`

   FastAPI routers, CRUD operations, auth dependencies, and response models.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/fastapi-router-py

7. `pydantic-models-py`

   Pydantic model patterns for Base, Create, Update, Response, and InDB variants.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/pydantic-models-py

8. `azure-identity-py`

   DefaultAzureCredential, managed identity, and service principals.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-identity-py

### Strong Additions

1. `azure-keyvault-py`
2. `azure-monitor-opentelemetry-py`
3. `azure-monitor-query-py`
4. `azure-servicebus-py`
5. `azure-eventhub-py`
6. `azure-eventgrid-py`
7. `azure-storage-blob-py`
8. `azure-appconfiguration-py`
9. `azure-ai-contentsafety-py`
10. `azure-ai-contentunderstanding-py`
11. `azure-ai-ml-py`
12. `azure-ai-voicelive-py`

## TypeScript and React Skills

Use these when building React frontends, Node services, TypeScript SDK integrations, workflow designers, real time apps, or Azure hosted web applications.

### Must Have

1. `azure-ai-projects-ts`

   Foundry client, agents, connections, and evaluations.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-ai-projects-ts

2. `azure-search-documents-ts`

   AI Search, vector search, hybrid search, semantic ranking, and knowledge bases.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-search-documents-ts

3. `m365-agents-ts`

   Microsoft 365 Agents SDK, AgentApplication routing, Express hosting, streaming, and Copilot Studio client.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/m365-agents-ts

4. `azure-identity-ts`

   DefaultAzureCredential, managed identity, and browser login.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-identity-ts

5. `azure-keyvault-secrets-ts`

   Store and retrieve application secrets.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-keyvault-secrets-ts

6. `azure-monitor-opentelemetry-ts`

   Tracing, metrics, logs, and Application Insights.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-monitor-opentelemetry-ts

7. `frontend-ui-dark-ts`

   Vite, React, Tailwind, Framer Motion, dark themed UI design system.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/frontend-ui-dark-ts

8. `react-flow-node-ts`

   React Flow nodes with TypeScript types, handles, and Zustand.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/react-flow-node-ts

9. `zustand-store-ts`

   TypeScript Zustand store patterns with subscribeWithSelector and action separation.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/zustand-store-ts

### Strong Additions

1. `azure-cosmos-ts`
2. `azure-postgres-ts`
3. `azure-storage-blob-ts`
4. `azure-storage-queue-ts`
5. `azure-servicebus-ts`
6. `azure-eventhub-ts`
7. `azure-web-pubsub-ts`
8. `azure-appconfiguration-ts`
9. `azure-ai-contentsafety-ts`
10. `azure-ai-document-intelligence-ts`
11. `azure-ai-voicelive-ts`
12. `aspire-ts`

## Microsoft Foundry Skills

Use these for agentic applications, model orchestration, evaluations, tools, hosted agents, and Foundry SDK development.

### Must Have

1. `microsoft-foundry`

   End to end Microsoft Foundry resources, agents, model deployment, evaluation, troubleshooting, and prompt optimization.

   https://github.com/microsoft/azure-skills/blob/main/skills/microsoft-foundry/SKILL.md

2. `azure-ai-projects-py`

   Foundry SDK for Python.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-ai-projects-py

3. `azure-ai-projects-dotnet`

   Foundry SDK for .NET.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/azure-ai-projects-dotnet

4. `azure-ai-projects-ts`

   Foundry SDK for TypeScript.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/azure-ai-projects-ts

5. `agent-framework-azure-ai-py`

   Microsoft Agent Framework and Azure AI integration for Python.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/agent-framework-azure-ai-py

6. `hosted-agents-v2-py`

   Hosted agent patterns and deployment.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/hosted-agents-v2-py

7. `azure-ai-voicelive-py`, `azure-ai-voicelive-dotnet`, and `azure-ai-voicelive-ts`

   Real time voice AI with bidirectional WebSocket support.

### Foundry Official References

1. Microsoft Foundry documentation  
   https://learn.microsoft.com/en-us/azure/foundry/

2. What is Microsoft Foundry  
   https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

3. Foundry SDK overview  
   https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview

4. Foundry quickstart  
   https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code

5. Foundry skills for hosted agents  
   https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/skills

## Azure Platform Skills

Use these for Azure architecture, deployment, infrastructure, security, monitoring, and operations.

### Must Have

1. `cloud-solution-architect`

   Azure architecture, Well Architected Framework pillars, design patterns, mission critical workloads, and technology choices.

   https://github.com/microsoft/skills/tree/main/.github/skills/cloud-solution-architect

2. `mcp-builder`

   Build MCP servers for Python, Node and TypeScript, or C# and .NET.

   https://github.com/microsoft/skills/tree/main/.github/skills/mcp-builder

3. `entra-agent-id`

   Microsoft Entra Agent ID, OAuth capable AI agent identities, Microsoft Graph beta API, blueprints, permissions, and workload identity federation.

   https://github.com/microsoft/skills/tree/main/.github/skills/entra-agent-id

4. `azure-identity` skills by language.

   Use for DefaultAzureCredential, managed identity, browser login, service principals, and secure auth.

5. `azure-keyvault` skills by language.

   Use for secrets, keys, certificates, encryption, signing, and secure configuration.

6. `azure-monitor-opentelemetry` skills by language.

   Use for tracing, metrics, logs, Application Insights, and observability.

7. `azure-mgmt-apimanagement` or `azure-mgmt-apicenter` skills by language.

   Use for API governance, API inventory, APIs, products, and policies.

8. `azure-servicebus`, `azure-eventhub`, and `azure-eventgrid`.

   Use for messaging, streaming, and event driven architecture.

9. `azure-storage-blob`, `azure-storage-queue`, `azure-storage-file-share`.

   Use for cloud storage and queue patterns.

10. `azure-cosmos-db-py` or `azure-cosmos` skills.

   Use for document persistence, partitioning, queries, and service layers.

## Microsoft 365 Agent Skills

Use these for Microsoft 365 Agents SDK, Copilot Studio integration, and enterprise assistants.

### Must Have

1. `m365-agents-py`

   Microsoft 365 Agents SDK with aiohttp hosting, AgentApplication routing, streaming, and Copilot Studio client.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/m365-agents-py

2. `m365-agents-dotnet`

   Microsoft 365 Agents SDK with ASP.NET Core hosting, AgentApplication routing, and Copilot Studio client.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-dotnet/skills/m365-agents-dotnet

3. `m365-agents-ts`

   Microsoft 365 Agents SDK with AgentApplication routing, Express hosting, streaming, and Copilot Studio client.

   https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/m365-agents-ts

## AI Services Skills

Use these for real AI workloads beyond basic chat.

### Recommended

1. `azure-ai-contentsafety-py`
2. `azure-ai-contentsafety-ts`
3. `azure-ai-contentunderstanding-py`
4. `azure-ai-document-intelligence-dotnet`
5. `azure-ai-document-intelligence-ts`
6. `azure-ai-ml-py`
7. `azure-ai-vision-imageanalysis-py`
8. `azure-ai-voicelive-py`
9. `azure-ai-voicelive-dotnet`
10. `azure-ai-voicelive-ts`
11. `azure-ai-textanalytics-py`
12. `azure-ai-transcription-py`
13. `azure-search-documents-py`
14. `azure-search-documents-dotnet`
15. `azure-search-documents-ts`

## Recommended Skill Bundles

## Bundle 1: Full Stack Microsoft Foundry App

Use this for a React plus API plus Foundry agent application.

```text
microsoft-foundry
azure-ai-projects-ts
azure-ai-projects-py or azure-ai-projects-dotnet
azure-search-documents-ts
azure-search-documents-py or azure-search-documents-dotnet
azure-identity-ts
azure-identity-py or azure-identity-dotnet
azure-keyvault-secrets-ts
azure-keyvault-py or azure-security-keyvault-keys-dotnet
azure-monitor-opentelemetry-ts
azure-monitor-opentelemetry-py or azure-mgmt-applicationinsights-dotnet
frontend-ui-dark-ts
react-flow-node-ts
zustand-store-ts
cloud-solution-architect
```

## Bundle 2: Python FastAPI Azure Backend

Use this for Python APIs, RAG backends, and service layers.

```text
fastapi-router-py
pydantic-models-py
azure-ai-projects-py
azure-search-documents-py
azure-cosmos-db-py
azure-identity-py
azure-keyvault-py
azure-servicebus-py
azure-eventgrid-py
azure-monitor-opentelemetry-py
cloud-solution-architect
```

## Bundle 3: .NET Enterprise Agent Backend

Use this for ASP.NET Core, Microsoft Foundry, Microsoft 365 Agents, and Azure SDK services.

```text
azure-ai-projects-dotnet
azure-ai-openai-dotnet
m365-agents-dotnet
azure-search-documents-dotnet
azure-identity-dotnet
azure-security-keyvault-keys-dotnet
azure-servicebus-dotnet
azure-eventhub-dotnet
azure-resource-manager-sql-dotnet
azure-mgmt-apimanagement-dotnet
azure-mgmt-applicationinsights-dotnet
cloud-solution-architect
```

## Bundle 4: TypeScript React Workflow UI

Use this for workflow builders, agent control planes, dashboards, and visual orchestration UIs.

```text
frontend-ui-dark-ts
react-flow-node-ts
zustand-store-ts
azure-ai-projects-ts
azure-search-documents-ts
azure-monitor-opentelemetry-ts
azure-identity-ts
azure-keyvault-secrets-ts
azure-web-pubsub-ts
azure-microsoft-playwright-testing-ts
aspire-ts
```

## Bundle 5: Azure Operations and Deployment

Use this when agents need to do real Azure work.

```text
azure-skills plugin
azure-prepare
azure-validate
azure-deploy
microsoft-foundry
cloud-solution-architect
azure-identity
azure-monitor
azure-rbac
azure-security
azure-cost-management
```

## Bundle 6: Agentic Enterprise Platform

Use this for OpenClaw style or enterprise agent orchestration platforms using Microsoft technology.

```text
microsoft-foundry
agent-framework-azure-ai-py
azure-ai-projects-py
azure-ai-projects-dotnet
m365-agents-py or m365-agents-dotnet
mcp-builder
entra-agent-id
azure-identity
azure-keyvault
azure-monitor-opentelemetry
azure-servicebus
azure-eventgrid
azure-storage-queue
cloud-solution-architect
```

# Recommended CLAUDE.md or AGENTS.md Policy

Use this policy in Claude Code and Codex projects.

```markdown
# Microsoft Skills Policy

Use Microsoft skills selectively. Do not load the full catalog.

Before implementing Microsoft Azure, Microsoft Foundry, .NET, Python, TypeScript, React, or Microsoft 365 agent code:

1. Identify the target platform.
2. Load only the relevant Microsoft skill files.
3. Prefer Microsoft official skills and Microsoft Learn references.
4. Use the language specific skill that matches the implementation language.
5. Use Microsoft Foundry skills for agents, models, evaluations, hosted agents, and prompt optimization.
6. Use Azure Identity skills for authentication and managed identity.
7. Use Key Vault skills for secrets and keys.
8. Use Azure Monitor and OpenTelemetry skills for observability.
9. Use API Management and API Center skills for API governance.
10. Use Cloud Solution Architect skill for architecture decisions.
11. Use MCP Builder when creating MCP servers.
12. Use Entra Agent ID when creating OAuth capable agent identities.
13. Do not mix patterns from different SDK versions without checking official docs.
14. Do not use deprecated or classic Foundry patterns unless the project explicitly requires them.
15. Validate with official Microsoft Learn docs when the SDK version or API lifecycle matters.
```

# Installation Guidance

## Install Microsoft Agent Skills

```bash
npx skills add microsoft/skills
```

## Install Azure Scaffold Wizard

```bash
npx skills add microsoft/Foundry-AI-solution-templates-creation
```

## Clone and Copy Selective Skills

```bash
git clone https://github.com/microsoft/skills.git

cp -r skills/.github/plugins/azure-sdk-python/skills/azure-ai-projects-py your-project/.github/skills/
cp -r skills/.github/plugins/azure-sdk-dotnet/skills/azure-ai-projects-dotnet your-project/.github/skills/
cp -r skills/.github/plugins/azure-sdk-typescript/skills/azure-ai-projects-ts your-project/.github/skills/
```

## Share Skills Across Agent Hosts

```bash
ln -s ../.github/skills .claude/skills
ln -s ../.github/skills .opencode/skills
```

## Use Microsoft Learn MCP

Use Microsoft Learn MCP when the agent needs current, authoritative Microsoft docs.

Microsoft Learn MCP is mentioned by Microsoft as one of the MCP servers included in the skills ecosystem.

# Selection Rules

## Rule 1: Use language specific skills first

If coding in Python, use the `-py` skill.

If coding in .NET, use the `-dotnet` skill.

If coding in TypeScript or React, use the `-ts` skill.

## Rule 2: Use platform skills for cross cutting concerns

Use these across languages:

1. `cloud-solution-architect`
2. `mcp-builder`
3. `entra-agent-id`
4. `microsoft-foundry`
5. `skill-creator`

## Rule 3: Load by workload, not by vendor

Do not load every Azure skill because the project uses Azure.

Load by workload:

1. RAG needs AI Search, Foundry, identity, monitoring, and storage.
2. Messaging needs Service Bus, Event Grid, or Event Hubs.
3. Secrets need Key Vault.
4. APIs need API Management or API Center.
5. React workflow UI needs frontend, React Flow, Zustand, Playwright.
6. Agent platform needs Foundry, Agent Framework, Entra Agent ID, MCP Builder, Service Bus, Monitor.

## Rule 4: Pair every Azure service skill with identity and observability

For production grade work, most Azure service skills should be paired with:

1. Azure Identity.
2. Key Vault when secrets are involved.
3. Azure Monitor or OpenTelemetry.
4. Cloud Solution Architect for architectural decisions.

## Rule 5: Avoid context rot

Do not load skills that do not directly apply to the current task.

Bad:

```text
Load all Azure skills.
```

Good:

```text
For a Python RAG API, load:
azure-ai-projects-py
azure-search-documents-py
azure-cosmos-db-py
azure-identity-py
azure-keyvault-py
azure-monitor-opentelemetry-py
fastapi-router-py
pydantic-models-py
```

# Best Practical Starting Stack for You

Given your work around Microsoft Foundry, Azure, agent orchestration, OpenClaw style systems, .NET, Python, TypeScript, and React, start with this set:

```text
cloud-solution-architect
mcp-builder
entra-agent-id
microsoft-foundry
agent-framework-azure-ai-py
azure-ai-projects-py
azure-ai-projects-dotnet
azure-ai-projects-ts
hosted-agents-v2-py
m365-agents-dotnet
m365-agents-ts
fastapi-router-py
pydantic-models-py
azure-search-documents-py
azure-search-documents-dotnet
azure-search-documents-ts
azure-cosmos-db-py
azure-identity-py
azure-identity-dotnet
azure-identity-ts
azure-keyvault-py
azure-keyvault-secrets-ts
azure-security-keyvault-keys-dotnet
azure-monitor-opentelemetry-py
azure-monitor-opentelemetry-ts
azure-mgmt-applicationinsights-dotnet
frontend-ui-dark-ts
react-flow-node-ts
zustand-store-ts
azure-microsoft-playwright-testing-ts
```

# Final Recommendation

Use Microsoft skills as your Microsoft engineering substrate.

For a modern Microsoft AI application, the core skill baseline should be:

1. `cloud-solution-architect`
2. `microsoft-foundry`
3. `agent-framework-azure-ai-py`
4. `azure-ai-projects-py`
5. `azure-ai-projects-dotnet`
6. `azure-ai-projects-ts`
7. `azure-search-documents` in the target language
8. `azure-identity` in the target language
9. `azure-keyvault` in the target language
10. `azure-monitor-opentelemetry` in the target language
11. `frontend-ui-dark-ts`
12. `react-flow-node-ts`
13. `zustand-store-ts`
14. `mcp-builder`
15. `entra-agent-id`

Do not install everything into every project. Create project specific skill bundles and keep the context narrow.

# References

## Microsoft Skills

1. Microsoft Agent Skills repository  
   https://github.com/microsoft/skills

2. Microsoft Agent Skills web catalog  
   https://microsoft.github.io/skills/

3. Microsoft All Things Azure blog: Context Driven Development, Agent Skills for Microsoft Foundry and Azure  
   https://devblogs.microsoft.com/all-things-azure/context-driven-development-agent-skills-for-microsoft-foundry-and-azure/

4. Microsoft Azure Skills Plugin  
   https://github.com/microsoft/azure-skills

5. Microsoft Azure Skills Plugin getting started blog  
   https://devblogs.microsoft.com/all-things-azure/azure-skills-plugin-lets-get-started/

6. MicrosoftDocs Agent Skills  
   https://github.com/MicrosoftDocs/Agent-Skills

7. MicrosoftDocs Agent Skills catalog  
   https://github.com/MicrosoftDocs/Agent-Skills/blob/main/docs/CATALOG.md

8. Microsoft Foundry skill source  
   https://github.com/microsoft/azure-skills/blob/main/skills/microsoft-foundry/SKILL.md

9. Microsoft Learn: Azure skill for Microsoft Foundry  
   https://learn.microsoft.com/en-us/azure/developer/azure-skills/skills/microsoft-foundry

10. GitHub Copilot for Azure Microsoft Foundry skill  
    https://github.com/microsoft/GitHub-Copilot-for-Azure/blob/main/plugin/skills/microsoft-foundry/SKILL.md

11. Azure Scaffold Wizard  
    https://github.com/microsoft/Foundry-AI-solution-templates-creation

## Microsoft Foundry

1. Microsoft Foundry documentation  
   https://learn.microsoft.com/en-us/azure/foundry/

2. What is Microsoft Foundry  
   https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

3. Microsoft Foundry SDKs and Endpoints  
   https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview

4. Microsoft Foundry quickstart  
   https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code

5. Use skills with Microsoft Foundry agents  
   https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/skills

6. Azure AI Projects Python SDK  
   https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme?view=azure-python

## Microsoft Agent Framework

1. Microsoft Agent Framework GitHub  
   https://github.com/microsoft/agent-framework

2. Microsoft Agent Framework docs  
   https://learn.microsoft.com/en-us/agent-framework/

3. Microsoft Agent Framework overview  
   https://learn.microsoft.com/en-us/agent-framework/overview/

4. Microsoft Agent Framework workflows  
   https://learn.microsoft.com/en-us/agent-framework/workflows/

5. Agents in workflows  
   https://learn.microsoft.com/en-us/agent-framework/workflows/agents-in-workflows
