# PulseOrchestrator Public Repository

This repository is the public companion to the closed-source PulseOrchestrator codebase.

It currently contains:

- the public `update-policy.json` consumed by release/update clients
- the versioned documentation site published to GitHub Pages

## Local docs workflow

Install the docs toolchain:

```powershell
py -m pip install -r requirements-docs.txt
```

Preview the site locally:

```powershell
py -m mkdocs serve
```

Build the site locally:

```powershell
py -m mkdocs build --strict
```

## Docs release flow

- Pushes to `main` publish the current docs as the `dev` version.
- GitHub Releases publish versioned docs using the release tag, for example `v1.0.0` becomes docs version `1.0.0`.
- Release docs are also aliased to `latest`, which becomes the default version on GitHub Pages.

## GitHub Pages setup

Set the repository Pages source to the `gh-pages` branch once. After that, the workflows in `.github/workflows` keep the site updated.
