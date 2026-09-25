# Security, API Security, and Preconditions Skills Research

**Prepared for:** Rich Crane  
**Prepared on:** May 02, 2026, 11:08 AM EST  
**Primary platforms:** Claude Code and OpenAI Codex  
**Purpose:** Identify the best skills and reference patterns for secure coding, API security, endpoint preconditions, input validation, authorization, negative testing, and adversarial review.

## Executive Summary

The best solution is not one skill. It is a combined security skill set.

Use a general application security skill, an API security skill, a preconditions and contract skill, and an adversarial review skill. Together, these prevent an agent from simply writing code that works on the happy path. The agent must also prove that each endpoint rejects invalid, unauthorized, unsafe, and unexpected requests.

The recommended operating pattern is:

```text
Define preconditions.
Enforce preconditions.
Test preconditions.
Review for bypasses.
Document security assumptions.
```

For API work, the agent should treat every endpoint as a security boundary.

## Best Skills Found

## 1. Security and Hardening Skill

**Source:** Addy Osmani agent skills  
**Best use case:** General secure coding and hardening across applications.

This is the best general application security skill found. It is triggered for user input, authentication, authorization, sensitive data, external APIs, file uploads, webhooks, callbacks, payments, and PII.

**Why it matters:**

1. Broad trigger coverage.
2. Good default for secure coding.
3. Useful for any feature that crosses a trust boundary.
4. Strong fit for mandatory secure development behavior.

**Best copied ideas:**

1. Treat user input as untrusted.
2. Apply security reviews whenever code accepts input.
3. Review authentication and authorization explicitly.
4. Treat external API integration as a security boundary.
5. Treat file uploads, callbacks, webhooks, payments, and PII as high risk.

**Reference:**

https://github.com/addyosmani/agent-skills/blob/main/skills/security-and-hardening/SKILL.md

## 2. API Security Best Practices Skill

**Source:** davila7 claude code templates  
**Best use case:** REST, GraphQL, and WebSocket API security.

This is the best direct API security skill found. It covers authentication, authorization, input validation, rate limiting, injection protection, DDoS protection, security reviews, audits, and sensitive data handling.

**Why it matters:**

1. Directly focused on APIs.
2. Covers REST, GraphQL, and WebSocket APIs.
3. Includes authentication and authorization.
4. Includes rate limiting and throttling.
5. Fits new endpoint development and existing API hardening.

**Best copied ideas:**

1. Use this whenever designing or modifying endpoints.
2. Require authentication and authorization review.
3. Require input validation.
4. Require rate limiting where abuse is possible.
5. Require secure sensitive data handling.
6. Require API specific negative tests.

**Reference:**

https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/security/api-security-best-practices/SKILL.md

## 3. Senior Security Skill

**Source:** Alireza Rezvani Claude skills  
**Best use case:** Threat modeling, vulnerability analysis, secure architecture, and security review.

This is a strong senior security engineer skill. It includes STRIDE analysis, OWASP guidance, cryptography patterns, security scanning tools, threat modeling, vulnerability assessment, attack surface analysis, and CVE remediation.

**Why it matters:**

1. Strong security architecture coverage.
2. Useful before implementing risky systems.
3. Good for deciding what must be protected.
4. Good for reviewing architectural security assumptions.

**Best copied ideas:**

1. Use STRIDE for threat modeling.
2. Identify attack surface before coding.
3. Review cryptography choices.
4. Review secure architecture, not only code.
5. Include vulnerability analysis before production.

**Reference:**

https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/senior-security/SKILL.md

## 4. Security Pen Testing Skill

**Source:** Alireza Rezvani Claude skills  
**Best use case:** Security audits, vulnerability scanning, API security testing, SAST, dependency scanning, secret detection, and report generation.

This is stronger for active testing than general secure coding. Use it after the agent has implemented or changed code.

**Why it matters:**

1. Covers API security testing.
2. Covers static analysis.
3. Covers dependency scanning.
4. Covers secret detection.
5. Supports pen test style reporting.

**Best copied ideas:**

1. Run SAST and dependency checks.
2. Check for secrets.
3. Include API focused security testing.
4. Generate findings with severity.
5. Use after implementation and before merge.

**Reference:**

https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/security-pen-testing/SKILL.md

## 5. OWASP Security Skill for Claude Code

**Source:** agamm Claude Code OWASP  
**Best use case:** OWASP aligned secure development.

This skill packages OWASP security guidance for Claude Code and includes recent OWASP oriented material for secure application development.

**Why it matters:**

1. Designed specifically for Claude Code.
2. OWASP aligned.
3. Useful as a baseline security skill.
4. Easy to install in `.claude/skills`.

**Best copied ideas:**

1. Keep OWASP guidance close to the coding agent.
2. Use an OWASP skill as a reusable security lens.
3. Make secure development part of the normal agent workflow.

**Reference:**

https://github.com/agamm/claude-code-owasp

## 6. Adversarial Code Reviewer Skill

**Source:** Alireza Rezvani Claude skills  
**Best use case:** Catching blind spots before merge.

This skill forces multiple hostile reviewer personas, including a security auditor, to find issues rather than accepting weak code. It is useful when the agent is too agreeable or when the implementation has passed basic checks but may still contain security gaps.

**Why it matters:**

1. Forces critical review.
2. Prevents easy "looks good" reviews.
3. Uses a security auditor lens.
4. Good for risky PRs and endpoint changes.

**Best copied ideas:**

1. Every security review must try to break the code.
2. Reviewers must look for bypasses.
3. Findings should be severity classified.
4. A security auditor persona should be mandatory for API work.

**Reference:**

https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/adversarial-reviewer/SKILL.md

## 7. Agent OWASP ASI Compliance Skill

**Source:** GitHub Awesome Copilot  
**Best use case:** Agentic systems and tool calling security.

This skill evaluates AI agent systems against OWASP Agentic Security Initiative risks. It is useful when the codebase includes agents, tool calls, automation, plugins, skills, or delegated execution.

**Why it matters:**

1. Focuses on agentic systems rather than normal web apps.
2. Useful for tools, plugins, and autonomous workflows.
3. Helps map controls to agentic risks.
4. Good for production readiness reviews of agent systems.

**Best copied ideas:**

1. Treat agent tools as security boundaries.
2. Review delegated execution.
3. Review permissions and tool access.
4. Generate a compliance report when preparing for production.

**Reference:**

https://github.com/github/awesome-copilot/blob/main/skills/agent-owasp-compliance/SKILL.md

## 8. Invariant Analyzer Skill

**Source:** Claude skill registry  
**Best use case:** Identifying invariants, preconditions, postconditions, and proof outlines.

This is useful for the preconditions part of the requested research. It focuses on correctness proof elements, including invariants, preconditions, and postconditions.

**Why it matters:**

1. Makes hidden assumptions explicit.
2. Helps the agent reason about correctness.
3. Useful for critical functions, state changes, and endpoint contracts.
4. Provides a structured output schema.

**Best copied ideas:**

1. Extract preconditions before coding.
2. Extract postconditions after coding.
3. Track invariants that must remain true.
4. Use proof outlines for critical logic.

**Reference:**

https://github.com/majiayu000/claude-skill-registry/blob/main/skills/other/other/invariant-analyzer/SKILL.md

## 9. Contract Oriented Docstring Skill

**Source:** Matthew Honnibal Claude skills  
**Best use case:** Documenting function contracts and failure modes.

This reference is useful because it frames docstrings as contracts. It documents what a function requires, what it guarantees, and how it fails. It explicitly looks at input invariants, preconditions beyond the type signature, explicit versus implicit errors, external state errors, and swallowed errors.

**Why it matters:**

1. Strong precondition thinking.
2. Helps prevent silent failure.
3. Makes error behavior explicit.
4. Good for APIs, services, and core business logic.

**Best copied ideas:**

1. Document what the caller must provide.
2. Document what the function guarantees.
3. Document expected failure modes.
4. Replace implicit crashes with explicit errors.
5. Avoid swallowed errors.

**Reference:**

https://github.com/honnibal/claude-skills

## 10. Tiger Style Skill

**Source:** M64GitHub TigerStyle  
**Best use case:** High integrity coding discipline.

Tiger Style is not primarily an API security skill, but it is valuable for preconditions, postconditions, invariants, assertions, explicit error handling, bounded logic, and safety critical coding.

**Why it matters:**

1. Requires assertions for preconditions, postconditions, and invariants.
2. Requires explicit error handling.
3. Avoids unsafe control flow.
4. Emphasizes safety first.

**Best copied ideas:**

1. Require precondition assertions.
2. Require postcondition assertions.
3. Require invariant checks.
4. Do not ignore errors.
5. Make every branch explicit where risk is high.

**Reference:**

https://github.com/M64GitHub/tiger-style

## 11. API Design Skill

**Source:** affaan everything Claude Code  
**Best use case:** API design foundations, including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting.

This is not a pure security skill, but it is useful for designing APIs that are easier to secure. Poor API design often creates security risk later.

**Why it matters:**

1. Includes rate limiting.
2. Encourages consistent error responses.
3. Supports production API conventions.
4. Useful before applying security review.

**Reference:**

https://github.com/affaan-m/everything-claude-code/blob/main/skills/api-design/SKILL.md

## 12. API Designer Skill

**Source:** Jeffallan Claude skills  
**Best use case:** REST or GraphQL API architecture and OpenAPI specifications.

This is a design skill, not a security skill. It is useful as a companion because OpenAPI schemas make preconditions, validation, request shapes, response shapes, and error contracts explicit.

**Why it matters:**

1. Supports OpenAPI specifications.
2. Helps define schema driven contracts.
3. Useful before generating endpoint code.
4. Makes validation easier to enforce and test.

**Reference:**

https://github.com/Jeffallan/claude-skills/blob/main/skills/api-designer/SKILL.md

# OWASP Reference Standards

## OWASP API Security Top 10 2023

The OWASP API Security Top 10 2023 lists the major API risk categories, including broken object level authorization, broken authentication, broken object property level authorization, unrestricted resource consumption, broken function level authorization, unrestricted access to sensitive business flows, server side request forgery, security misconfiguration, improper inventory management, and unsafe consumption of APIs.

**Use in the skill:**

1. Every endpoint must be reviewed for object level authorization.
2. Every endpoint must be reviewed for function level authorization.
3. Every endpoint must reject over posting and mass assignment.
4. Every endpoint must control resource consumption.
5. Every outbound API call must be reviewed for unsafe consumption.

**Reference:**

https://owasp.org/API-Security/editions/2023/en/0x00-header/

## OWASP ASVS

OWASP ASVS provides a basis for testing web application technical security controls and a list of requirements for secure development.

**Use in the skill:**

1. Treat ASVS as the verification backbone.
2. Map high risk changes to ASVS controls.
3. Use ASVS as a yardstick for confidence.
4. Use ASVS to define non negotiable security requirements.

**Reference:**

https://owasp.org/www-project-application-security-verification-standard/

## OWASP REST Security Cheat Sheet

The REST Security Cheat Sheet emphasizes not trusting input parameters or objects, validating length, range, format, and type, using strong types, constraining strings, rejecting unexpected content, and using validation libraries.

**Use in the skill:**

1. Validate every request.
2. Reject unexpected content.
3. Use strong types.
4. Enforce length, range, format, and type.
5. Use allow lists where possible.

**Reference:**

https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html

## OWASP Input Validation Cheat Sheet

The Input Validation Cheat Sheet provides actionable guidance for input validation security functionality.

**Use in the skill:**

1. Validate as early as possible.
2. Prefer positive validation.
3. Validate syntax and semantics.
4. Use framework validation tools.
5. Test invalid input explicitly.

**Reference:**

https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

# Recommended Skill Stack

Use these skills together:

## Default Security Stack

1. Security and Hardening Skill.
2. API Security Best Practices Skill.
3. Preconditions and Contract Skill.
4. Adversarial Code Reviewer Skill.
5. Security Pen Testing Skill.

## API Endpoint Stack

1. API Designer Skill.
2. API Security Best Practices Skill.
3. Preconditions and Contract Skill.
4. TDD Skill.
5. Security and Hardening Skill.
6. Adversarial Code Reviewer Skill.

## Agentic System Stack

1. Security and Hardening Skill.
2. Agent OWASP ASI Compliance Skill.
3. Preconditions and Contract Skill.
4. Security Pen Testing Skill.
5. Adversarial Code Reviewer Skill.

# Recommended Mandatory Rules

Add these rules to `CLAUDE.md` and `AGENTS.md`.

```markdown
# Security and API Preconditions

Every API endpoint is a security boundary.

Before implementing or changing an endpoint, define:

1. Authentication preconditions.
2. Authorization preconditions.
3. Tenant or ownership preconditions.
4. Input schema preconditions.
5. Content type and request size preconditions.
6. Business rule preconditions.
7. Rate limit or quota preconditions.
8. Idempotency preconditions where repeated requests matter.
9. External dependency preconditions.
10. Logging and audit preconditions.

For every behavior changing API change, add tests for:

1. Positive authorized path.
2. Unauthenticated request.
3. Authenticated but unauthorized request.
4. Wrong tenant or wrong owner request.
5. Invalid input.
6. Missing required input.
7. Extra unexpected input.
8. Boundary values.
9. Rate limit or abuse case when applicable.
10. Sensitive data exposure.

Do not ship an endpoint that only has happy path tests.

Use OWASP API Security Top 10, OWASP ASVS, OWASP REST Security Cheat Sheet, and OWASP Input Validation Cheat Sheet as the baseline.
```

# Ready To Use Skill: Security API Preconditions

Save this as:

```text
security-api-preconditions/SKILL.md
```

```markdown
---
name: security-api-preconditions
description: Use when designing, implementing, modifying, or reviewing API endpoints, authentication, authorization, input validation, sensitive data handling, webhooks, callbacks, external API calls, or agent tool interfaces. Defines endpoint preconditions, enforces them in code, adds positive and negative tests, and reviews for OWASP API security risks.
---

# Security API Preconditions Skill

## Purpose

Use this skill to make security, API protection, and precondition enforcement part of normal coding.

The agent must not only make the endpoint work. The agent must prove the endpoint rejects invalid, unauthorized, unsafe, abusive, and unexpected requests.

## Core Principle

Every API endpoint is a security boundary.

Every endpoint must define, enforce, test, and document its preconditions.

## Trigger Conditions

Use this skill when the work includes:

1. REST APIs.
2. GraphQL APIs.
3. WebSocket APIs.
4. Authentication.
5. Authorization.
6. Session handling.
7. Tokens.
8. Webhooks.
9. Callbacks.
10. File uploads.
11. External API calls.
12. Sensitive data.
13. PII.
14. Payments.
15. Tenant scoped data.
16. Admin operations.
17. Agent tools.
18. Plugin actions.
19. Background jobs that process external input.
20. Any code that accepts user controlled input.

## Security Baseline

Use these standards as the baseline:

1. OWASP API Security Top 10.
2. OWASP ASVS.
3. OWASP REST Security Cheat Sheet.
4. OWASP Input Validation Cheat Sheet.

## Endpoint Preconditions

Before writing or modifying endpoint code, define the endpoint contract.

### Authentication Preconditions

Define:

1. Whether authentication is required.
2. Which identity provider is trusted.
3. Which token type is accepted.
4. Required session state.
5. Expiration behavior.
6. Required claims.
7. Failure status code.

Expected failures:

1. Missing token.
2. Expired token.
3. Invalid token.
4. Wrong issuer.
5. Wrong audience.
6. Revoked session.

### Authorization Preconditions

Define:

1. Required role.
2. Required permission.
3. Required ownership.
4. Required tenant membership.
5. Required resource relationship.
6. Admin only constraints.
7. Feature flag or license constraints.

Expected failures:

1. Authenticated user without permission.
2. User from wrong tenant.
3. User accessing another user's object.
4. Non admin calling admin endpoint.
5. User with stale or revoked permission.

### Input Preconditions

Define:

1. Required fields.
2. Optional fields.
3. Rejected fields.
4. Type constraints.
5. Length constraints.
6. Range constraints.
7. Format constraints.
8. Enum constraints.
9. Cross field constraints.
10. Content type.
11. Maximum request size.

Expected failures:

1. Missing required field.
2. Wrong type.
3. Out of range value.
4. Over length string.
5. Malformed identifier.
6. Unknown enum value.
7. Extra unexpected field.
8. Invalid content type.
9. Oversized request.

### Business Preconditions

Define:

1. Resource must exist.
2. Resource must be in an allowed state.
3. Operation must be allowed for that state.
4. Request must be idempotent if repeated.
5. User must not exceed quota.
6. Operation must not bypass approval.
7. Operation must preserve accounting or audit rules.

Expected failures:

1. Missing resource.
2. Resource in wrong state.
3. Duplicate request.
4. Exceeded quota.
5. Attempted workflow bypass.
6. Attempted business rule bypass.

### External Dependency Preconditions

Define:

1. Which external systems are called.
2. What data may be sent.
3. Timeout.
4. Retry limit.
5. Circuit breaker behavior.
6. SSRF protection.
7. Response validation.
8. Error handling.
9. Secret handling.

Expected failures:

1. External timeout.
2. External error.
3. Invalid external response.
4. Unsafe redirect.
5. Disallowed host.
6. Secret missing.
7. Secret exposure risk.

## Implementation Rules

When implementing an endpoint:

1. Authenticate before loading sensitive resources.
2. Authorize before returning or mutating data.
3. Enforce object level authorization on every resource access.
4. Enforce function level authorization on every privileged action.
5. Validate input before business logic.
6. Reject unknown fields unless the framework safely ignores them by design.
7. Prevent mass assignment.
8. Avoid leaking whether protected resources exist when that matters.
9. Use consistent error responses.
10. Do not log secrets, tokens, passwords, or full PII.
11. Rate limit high abuse endpoints.
12. Validate outbound API responses.
13. Use safe defaults.
14. Fail closed.
15. Add audit events for sensitive actions.

## Required Tests

For every new or changed endpoint, add tests for:

1. Happy path.
2. Missing authentication.
3. Invalid authentication.
4. Authenticated but unauthorized.
5. Wrong tenant or wrong owner.
6. Missing required input.
7. Invalid input type.
8. Invalid input range.
9. Extra unexpected input.
10. Boundary values.
11. Business rule violation.
12. Sensitive field exposure.
13. Rate limit or quota when applicable.
14. External API failure when applicable.
15. Idempotency when applicable.

Do not accept only happy path tests.

## API Security Review Checklist

Review every endpoint for:

1. Broken object level authorization.
2. Broken authentication.
3. Broken object property level authorization.
4. Unrestricted resource consumption.
5. Broken function level authorization.
6. Unrestricted access to sensitive business flows.
7. Server side request forgery.
8. Security misconfiguration.
9. Improper inventory management.
10. Unsafe consumption of APIs.

## Preconditions Table Format

Use this format before implementation:

```markdown
## Endpoint Preconditions

| Category | Requirement | Enforcement Point | Failure Case | Test Required |
|---|---|---|---|---|
| Authentication | User must have valid token | Auth middleware | Missing token returns 401 | Yes |
| Authorization | User must own resource | Service layer | Wrong owner returns 403 or 404 | Yes |
| Input | `id` must be valid UUID | Request validator | Invalid id returns 400 | Yes |
| Business | Resource must be active | Domain service | Inactive resource returns 409 | Yes |
| External | Vendor response must match schema | Client wrapper | Invalid response fails closed | Yes |
```

## Decision Rules

When unsure, choose the safer default:

1. Require authentication unless explicitly public.
2. Require authorization even when authentication exists.
3. Deny by default.
4. Reject unexpected input.
5. Prefer allow lists over block lists.
6. Prefer explicit schemas over loose objects.
7. Prefer 403 or 404 over revealing resource existence.
8. Prefer explicit audit logging for sensitive actions.
9. Prefer no data over too much data.
10. Prefer failing closed over guessing.

## Status Codes

Use consistent status codes:

1. `400` for malformed or invalid request syntax.
2. `401` for missing or invalid authentication.
3. `403` for authenticated but forbidden.
4. `404` when the resource does not exist or existence should not be revealed.
5. `409` for business state conflict.
6. `413` for request too large.
7. `415` for unsupported content type.
8. `422` for semantic validation errors when used by project convention.
9. `429` for rate limit.
10. `500` only for unexpected server errors.

Follow existing project conventions if they are secure and consistent.

## Security Test Naming

Name tests clearly:

```text
returns_401_when_token_missing
returns_403_when_user_lacks_permission
returns_404_when_resource_belongs_to_other_tenant
rejects_extra_fields_to_prevent_mass_assignment
rejects_invalid_uuid
rejects_oversized_payload
does_not_return_sensitive_fields
fails_closed_when_external_vendor_response_is_invalid
```

## Final Report Format

After implementation or review, report:

```markdown
## Security Summary

**Endpoint or component:** <name>

**Preconditions enforced:**
1. <precondition>
2. <precondition>

**Tests added:**
1. <positive test>
2. <negative test>

**OWASP API risks reviewed:**
1. <risk>
2. <risk>

**Security decisions:**
1. <decision and rationale>

**Remaining risks:**
1. <risk or none>

**Validation:**
1. <command and result>
```

## Anti Patterns

Avoid these behaviors:

1. Writing only happy path tests.
2. Assuming authentication implies authorization.
3. Trusting client supplied IDs without ownership checks.
4. Returning full model objects directly.
5. Accepting extra request fields without review.
6. Using client controlled URLs in server requests without allow lists.
7. Logging secrets or full PII.
8. Implementing rate limits only after abuse occurs.
9. Treating admin endpoints as internal and therefore safe.
10. Skipping tests because middleware is assumed to work.
11. Swallowing validation errors.
12. Failing open when external systems fail.

## Operating Mantra

Define the contract.  
Enforce the boundary.  
Reject unsafe input.  
Prove authorization.  
Test the negative paths.  
Fail closed.
```

# Claude Code Setup

Use this structure:

```text
CLAUDE.md
.claude/
  skills/
    security-api-preconditions/
      SKILL.md
  agents/
    security-reviewer.md
    api-security-reviewer.md
    precondition-validator.md
```

## Claude Security Reviewer Agent

```markdown
---
name: security-reviewer
description: Reviews code for authentication, authorization, input validation, secrets, data exposure, unsafe external calls, and OWASP risks.
tools: Read, Glob, Grep, Bash
model: opus
effort: high
---

You are a security reviewer.

Review only for real security risk. Focus on authentication, authorization, tenant isolation, input validation, injection, secrets, data exposure, unsafe external calls, and missing negative tests.

Return findings with severity, file references, exploit path, recommended fix, and required test.
```

## Claude API Security Reviewer Agent

```markdown
---
name: api-security-reviewer
description: Reviews API endpoints against OWASP API Security Top 10, endpoint preconditions, negative tests, and sensitive data exposure.
tools: Read, Glob, Grep, Bash
model: sonnet
effort: high
---

You are an API security reviewer.

For each endpoint, identify preconditions, enforcement points, missing tests, and bypass risks.

Focus on object level authorization, function level authorization, property level authorization, authentication, rate limits, request validation, mass assignment, SSRF, and unsafe outbound API consumption.

Do not edit files unless explicitly instructed.
```

## Claude Precondition Validator Agent

```markdown
---
name: precondition-validator
description: Extracts and verifies preconditions, postconditions, invariants, and failure modes for functions and API endpoints.
tools: Read, Glob, Grep, Bash
model: sonnet
effort: medium
---

You are a precondition validator.

Extract what each endpoint or function requires, guarantees, and rejects.

Return:
1. Preconditions.
2. Enforcement points.
3. Missing checks.
4. Missing negative tests.
5. Recommended assertions or validators.
```

# Codex Setup

Use this structure:

```text
AGENTS.md
.codex/
  agents/
    security_reviewer.toml
    api_security_reviewer.toml
    precondition_validator.toml
skills/
  security-api-preconditions/
    SKILL.md
```

## Codex Security Reviewer Agent

```toml
name = "security_reviewer"
description = "Read only reviewer for authentication, authorization, input validation, secrets, data exposure, unsafe external calls, and OWASP risks."
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = '''
Review only for real security risk.
Focus on authentication, authorization, tenant isolation, input validation, injection, secrets, data exposure, unsafe external calls, and missing negative tests.
Return severity, file references, exploit path, recommended fix, and required test.
'''
```

## Codex API Security Reviewer Agent

```toml
name = "api_security_reviewer"
description = "Read only API reviewer against OWASP API Security Top 10, endpoint preconditions, negative tests, and sensitive data exposure."
model_reasoning_effort = "high"
sandbox_mode = "read-only"

developer_instructions = '''
For each endpoint, identify preconditions, enforcement points, missing tests, and bypass risks.
Focus on object level authorization, function level authorization, property level authorization, authentication, rate limits, request validation, mass assignment, SSRF, and unsafe outbound API consumption.
'''
```

## Codex Precondition Validator Agent

```toml
name = "precondition_validator"
description = "Extracts and verifies preconditions, postconditions, invariants, and failure modes for functions and API endpoints."
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = '''
Extract what each endpoint or function requires, guarantees, and rejects.
Return preconditions, enforcement points, missing checks, missing negative tests, and recommended assertions or validators.
'''
```

# Recommended Workflow

Use this sequence for new or modified APIs:

1. Design the endpoint contract.
2. Write the preconditions table.
3. Add positive and negative tests.
4. Implement validation, authentication, authorization, and business rules.
5. Run tests.
6. Run API security review.
7. Run adversarial review for high risk endpoints.
8. Fix findings.
9. Document remaining risks.

# Best First Skills To Install

Install in this order:

1. API Security Best Practices Skill.
2. Security and Hardening Skill.
3. Security API Preconditions Skill from this document.
4. Adversarial Code Reviewer Skill.
5. Security Pen Testing Skill.
6. Agent OWASP ASI Compliance Skill if building agents or tool calling systems.

# Final Recommendation

Create one custom skill named:

```text
security-api-preconditions
```

Then pair it with existing skills:

1. Addy Osmani Security and Hardening.
2. davila7 API Security Best Practices.
3. Alireza Senior Security.
4. Alireza Security Pen Testing.
5. Alireza Adversarial Reviewer.
6. OWASP Security Skill for Claude Code.
7. GitHub Agent OWASP ASI Compliance.
8. Invariant Analyzer or contract oriented docstring skill for precondition extraction.

The most important behavior is this:

```text
The agent must define preconditions before implementation and must add negative tests proving those preconditions are enforced.
```

# Reference List

## Skills

1. Addy Osmani Security and Hardening  
   https://github.com/addyosmani/agent-skills/blob/main/skills/security-and-hardening/SKILL.md

2. API Security Best Practices  
   https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/security/api-security-best-practices/SKILL.md

3. Senior Security  
   https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/senior-security/SKILL.md

4. Security Pen Testing  
   https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/security-pen-testing/SKILL.md

5. OWASP Security Skill for Claude Code  
   https://github.com/agamm/claude-code-owasp

6. Adversarial Code Reviewer  
   https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/adversarial-reviewer/SKILL.md

7. Agent OWASP ASI Compliance  
   https://github.com/github/awesome-copilot/blob/main/skills/agent-owasp-compliance/SKILL.md

8. Invariant Analyzer  
   https://github.com/majiayu000/claude-skill-registry/blob/main/skills/other/other/invariant-analyzer/SKILL.md

9. Contract oriented docstring skills  
   https://github.com/honnibal/claude-skills

10. Tiger Style  
   https://github.com/M64GitHub/tiger-style

11. API Design  
   https://github.com/affaan-m/everything-claude-code/blob/main/skills/api-design/SKILL.md

12. API Designer  
   https://github.com/Jeffallan/claude-skills/blob/main/skills/api-designer/SKILL.md

## Standards and Official References

1. OWASP API Security Top 10 2023  
   https://owasp.org/API-Security/editions/2023/en/0x00-header/

2. OWASP Application Security Verification Standard  
   https://owasp.org/www-project-application-security-verification-standard/

3. OWASP REST Security Cheat Sheet  
   https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html

4. OWASP Input Validation Cheat Sheet  
   https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

5. Claude Code Skills  
   https://code.claude.com/docs/en/skills

6. OpenAI Codex Skills  
   https://developers.openai.com/codex/skills

7. Codex AGENTS.md  
   https://developers.openai.com/codex/guides/agents-md
