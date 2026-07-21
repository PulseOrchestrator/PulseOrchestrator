# PulseOrchestrator

<div class="hero">
  <div>
    <p class="eyebrow">Operations docs</p>
    <h1>Run, route, and scale Minecraft services from one control plane.</h1>
    <p class="hero-copy">
      PulseOrchestrator combines a launcher-managed control plane, a persistent process host, a built-in Velocity proxy, and Minecraft integrations into one workflow for provisioning and routing game services.
    </p>
    <div class="hero-actions">
      <a class="md-button md-button--primary" href="getting-started/install/">Install guide</a>
      <a class="md-button" href="guides/feature-guide/">Feature guide</a>
    </div>
  </div>
  <div class="hero-panel">
    <p class="hero-kicker">What ships together</p>
    <ul>
      <li>Launcher for version activation and orchestrator restart</li>
      <li>Runtime Host that keeps proxy and service processes alive</li>
      <li>Orchestrator CLI, API, setup, and lifecycle policy</li>
      <li>Paper plugin for bridge access, placeholders, and service metrics</li>
      <li>Velocity plugin for proxy commands, routing, and maintenance integration</li>
    </ul>
  </div>
</div>

## Documentation map

<div class="card-grid">
  <a class="doc-card" href="getting-started/install/">
    <strong>Install guide</strong>
    <span>What to download, how to start the orchestrator, what the setup wizard does, and how to connect the plugins.</span>
  </a>
  <a class="doc-card" href="guides/feature-guide/">
    <strong>Feature guide</strong>
    <span>The core concepts, CLI flows, proxy routing model, and day-to-day operations.</span>
  </a>
  <a class="doc-card" href="guides/runtime-architecture/">
    <strong>Runtime architecture</strong>
    <span>How Launcher, Runtime Host, and Orchestrator divide ownership and preserve live services.</span>
  </a>
  <a class="doc-card" href="guides/updates/">
    <strong>Updating Pulse</strong>
    <span>Warm updates, maintenance updates, rollback limits, verification, and recovery.</span>
  </a>
</div>

## What These Docs Cover

This site is for PulseOrchestrator users and operators.

The focus is:

- getting the orchestrator running
- connecting Paper and Velocity integrations
- understanding the task, service, and proxy model
- learning the main operational commands and workflows
- applying compatible updates without restarting Minecraft services
- planning maintenance when the Runtime Host or persistence model changes

## Typical Next Steps

1. Install PulseOrchestrator and complete the setup wizard.
2. Connect the Paper plugin or Velocity plugin to the API.
3. Create your first task blueprint.
4. Create and start your first service.
5. Configure proxy routing for player entry and fallback behavior.
