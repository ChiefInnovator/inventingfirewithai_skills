# Preferred stack

The owner's preferred technologies are a Python backend, Azure, Flutter for mobile, and React with TypeScript for web. The table fills in the rest. These are preferences, not limits: choose another technology when it fits the product better. C#/.NET and Swift/SwiftUI are possible but not preferred, except that Swift/SwiftUI is the choice for a native macOS app. Record each choice as a decision in step 3, with the reason when it departs from this table. An existing product keeps its own stack (step 1).

The builder deploys nothing. Every Azure service below is the eventual target: the build runs locally against the stand-in, and connecting the real service is a launch checklist item.

|Part|Preferred|Local stand-in during the build|
|---|---|---|
|Backend|Python with FastAPI|Runs locally|
|Backend hosting|Azure Container Apps; Azure Functions only for a small event-driven backend|Local server|
|Web app|React and TypeScript, built with Vite; no server-side rendering unless the product needs search traffic|Local dev server|
|Web hosting|Azure Static Web Apps|Local static build|
|Mobile|Flutter|Simulator or emulator|
|Desktop|Flutter desktop; Swift/SwiftUI for a native macOS app|Runs locally|
|Browser game|TypeScript with Vite, and no React for the game canvas|Local dev server|
|Browser or VS Code extension|TypeScript|Loaded unpacked|
|Command-line tool|Python|Runs locally|
|Database|Azure SQL; Azure Database for PostgreSQL is also acceptable|SQLite, through the same data access layer|
|Sign-in|Microsoft Entra External ID|A local stand-in behind one interface|
|Payments|Stripe on web; store in-app purchase on mobile|The money path stand-in from milestone 5|
|AI features inside the product|Microsoft Foundry when the product is Azure-backed; the model and any local runtime are chosen per project|A stub behind one interface|
|Tests|pytest for Python, Playwright for web, Flutter's own test tools for mobile|None needed|
|Launch checklist items|Bicep for infrastructure, GitHub Actions for CI, Application Insights for telemetry|Not built or run|
