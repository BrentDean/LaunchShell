# LaunchShell

LaunchShell is a project portfolio and tutorial site for practical technology projects.
It is meant to document real builds, experiments, notes, and lessons from working with Linux, cloud hosting, web servers, electronics, and safe cybersecurity fundamentals.

The core idea is:

Build it. Break it. Back it up. Learn why.

This repository currently contains the coming-soon homepage for LaunchShell. The site is a plain static website with no framework, build system, backend, or package manager.

## Current Status

Coming-soon homepage.

## Deployment Target

Cloudflare Pages.

Cloudflare Pages can serve this repository directly because `index.html` is at the repository root and assets are stored in `assets/`.

## Basic Edit Workflow

Edit `index.html`, then commit and push:

```sh
git add .
git commit -m "Update LaunchShell homepage"
git push
```

After the push, Cloudflare Pages redeploys the site from GitHub.
