# Performance Skills References

Purpose: collect practical agent skills that treat performance as a first class engineering requirement. These references are useful for building a simple skill that forces agents to measure, budget, test, and verify performance as part of feature delivery.

## Recommended base skill

### Addy Osmani Performance Optimization Skill

URL: https://github.com/addyosmani/agent-skills/blob/main/skills/performance-optimization/SKILL.md

Best use: general application performance optimization.

Why it matters:

1. It activates when performance requirements exist.
2. It activates when Core Web Vitals, load time, or regressions matter.
3. It emphasizes profiling before optimization.
4. It is broad enough to serve as the base for a custom “performance as a feature” skill.

Recommended role in your skill system: use this as the primary reference.

## Web performance skills

### Addy Osmani Web Quality Skills

URL: https://github.com/addyosmani/web-quality-skills

Best use: web application quality, Lighthouse, Core Web Vitals, accessibility, SEO, and performance budgets.

Why it matters:

1. It is framework agnostic.
2. It focuses on Google Lighthouse and Core Web Vitals guidance.
3. It supports performance budgets and production quality checks.
4. It is a strong companion to the general performance optimization skill.

Recommended role in your skill system: use for frontend and web application performance gates.

### perf lighthouse Skill

URL: https://github.com/christophacham/agent-skills-library/blob/main/skills/web-dev/perf-lighthouse/SKILL.md

Best use: Lighthouse audits, performance budgets, report interpretation, and CI integration.

Why it matters:

1. It is focused and practical.
2. It tells the agent when to run Lighthouse.
3. It supports budget driven development.
4. It is useful for automated performance verification.

Recommended role in your skill system: use when a feature needs a Lighthouse score, budget check, or CI audit.

## React and Next.js skills

### Vercel React Best Practices Skill

URL: https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md

Best use: React and Next.js performance optimization.

Why it matters:

1. It is maintained by Vercel Labs.
2. It focuses on React and Next.js performance patterns.
3. It covers component behavior, data fetching, bundle size, rendering, and load time.
4. It is useful when agents are writing or reviewing React code.

Recommended role in your skill system: use for React and Next.js feature development.

## React Native and mobile skills

### Callstack React Native Best Practices Skill

URL: https://github.com/callstackincubator/agent-skills/blob/main/skills/react-native-best-practices/SKILL.md

Best use: React Native performance, mobile responsiveness, memory, bundle size, animation smoothness, and frame drops.

Why it matters:

1. It covers FPS, time to interactive, bundle size, memory leaks, re renders, and animations.
2. It addresses Hermes optimization, JS thread blocking, bridge overhead, and jank.
3. It is directly relevant to mobile application quality.
4. It gives agents mobile specific constraints that are easy to miss.

Recommended role in your skill system: use for React Native and Expo projects.

## Platform specific performance skills

### WordPress wp performance Skill

URL: https://github.com/WordPress/agent-skills/blob/trunk/skills/wp-performance/SKILL.md

Best use: WordPress backend performance.

Why it matters:

1. It covers profiling and measurement with WP CLI, Server Timing, and Query Monitor.
2. It covers database and query optimization.
3. It covers autoloaded options, object caching, cron, and HTTP API calls.
4. It includes safe verification patterns.

Recommended role in your skill system: use for WordPress sites, plugins, and backend performance investigations.

### RTK Performance Skill

URL: https://github.com/rtk-ai/rtk/blob/master/.claude/skills/performance/SKILL.md

Best use: CLI performance and measurable performance targets.

Why it matters:

1. It defines explicit performance targets.
2. It treats startup time, memory usage, token savings, and binary size as acceptance criteria.
3. It is a useful example of concrete performance budgets.
4. It shows how to make performance measurable instead of aspirational.

Recommended role in your skill system: use as a model for measurable acceptance criteria.

## Performance engineering and nonfunctional requirement skills

### OpenRequirementsAI Performance Engineering Skill

URL: https://github.com/AgenticTesting/OpenRequirementsAI/blob/main/.claude/skills/performanceengineering/SKILL.md

Best use: performance requirements, SLAs, scalability, capacity planning, monitoring, and load testing documentation.

Why it matters:

1. It turns nonfunctional requirements into performance budgets.
2. It supports SLA definition.
3. It supports capacity planning and scalability assessment.
4. It helps connect product requirements to measurable engineering targets.

Recommended role in your skill system: use during requirements analysis and architecture planning.

## Suggested custom skill pattern

### Name

performance-as-a-feature

### Description

Use this skill whenever a user facing change, backend change, API change, data processing change, mobile feature, or UI feature could affect speed, responsiveness, cost, memory, bundle size, scalability, or reliability.

### Core principle

Performance is not cleanup work. Performance is part of the feature.

### Required behavior

1. Identify the performance surface area before coding.
2. Define the relevant metric or budget.
3. Measure the current baseline when possible.
4. Add or update tests, benchmarks, Lighthouse checks, or profiling steps.
5. Implement the smallest safe change.
6. Verify the performance result.
7. Document any tradeoff.
8. Treat regressions as failed acceptance criteria.

### Positive test examples

1. A page renders within the target time budget.
2. An API response stays below the latency threshold.
3. A list renders correctly with a large input data set.
4. A mobile interaction stays smooth under realistic load.
5. A bundle size stays under the defined limit.

### Negative test examples

1. The feature rejects or handles oversized input safely.
2. The system does not block the main thread under heavy usage.
3. The API does not degrade catastrophically under invalid or excessive requests.
4. The UI does not re render unnecessarily under repeated state changes.
5. The build fails when the performance budget is exceeded.

### Exit criteria

1. Relevant tests pass.
2. Relevant performance checks pass.
3. No obvious regression is introduced.
4. The performance budget is documented.
5. Any unresolved risk is stated clearly.

## Recommended ranking

1. Addy Osmani Performance Optimization Skill
2. Addy Osmani Web Quality Skills
3. Vercel React Best Practices Skill
4. Callstack React Native Best Practices Skill
5. perf lighthouse Skill
6. OpenRequirementsAI Performance Engineering Skill
7. WordPress wp performance Skill
8. RTK Performance Skill

## Reference links

1. Addy Osmani Performance Optimization Skill: https://github.com/addyosmani/agent-skills/blob/main/skills/performance-optimization/SKILL.md
2. Addy Osmani Web Quality Skills: https://github.com/addyosmani/web-quality-skills
3. Vercel React Best Practices Skill: https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md
4. Callstack React Native Best Practices Skill: https://github.com/callstackincubator/agent-skills/blob/main/skills/react-native-best-practices/SKILL.md
5. WordPress wp performance Skill: https://github.com/WordPress/agent-skills/blob/trunk/skills/wp-performance/SKILL.md
6. perf lighthouse Skill: https://github.com/christophacham/agent-skills-library/blob/main/skills/web-dev/perf-lighthouse/SKILL.md
7. OpenRequirementsAI Performance Engineering Skill: https://github.com/AgenticTesting/OpenRequirementsAI/blob/main/.claude/skills/performanceengineering/SKILL.md
8. RTK Performance Skill: https://github.com/rtk-ai/rtk/blob/master/.claude/skills/performance/SKILL.md

