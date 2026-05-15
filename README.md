# LaunchShell

**Build it. Back it up. Break it. Fix it. Learn why.**

LaunchShell is a static project portfolio and tutorial site for practical technology builds: Linux, cloud servers, Git/GitHub, web apps, electronics, virtual machines, and safe beginner cybersecurity labs.

The site is intentionally simple. It is plain HTML and CSS so the content stays easy to inspect, edit, commit, and publish.

## Current Site

- Homepage: `index.html`
- Guides index: `guides/index.html`
- Projects index: `projects/index.html`
- Resources index: `resources/index.html`
- Shared styling: `assets/site.css`
- Shared images and icons: `assets/`

## Guides

- Linux Terminal Intro: `guides/linux-terminal-intro/`
- AWS Free VPS Setup: `guides/aws-free-vps/`
- What Is a VM?: `guides/what-is-a-vm/`
- What Is Hacking?: `guides/what-is-hacking/`
- Git and GitHub: `guides/git-and-github/`
- GitHub Codespaces: `guides/github-codespace/`
- Cloudflare Pages: `guides/cloudflare/`
- IT and Cybersecurity Certifications: `guides/certification/`

## Projects

- Flask JSON app on a cheap server: `projects/cheap-server-web-app/`
- T-Pot honeynet project: `projects/tpot-honeynet/`
- 8-bit computer and ROM tooling: `projects/8-bit/`
- How this site was built: `projects/build-this-site/`

## Tech Stack

- Plain HTML
- Shared CSS
- Local assets
- No framework
- No build step
- No backend
- No package manager

## Deployment

Deployment target: Cloudflare Pages.

Cloudflare Pages can serve this repository directly because the root page is `index.html` and all pages/assets are committed into the repository.

## Edit Workflow

Make a small content or style change, check it locally, then commit:

```sh
git status --short
git diff --check
git add <files>
git commit -m "Describe the site update"
```

Push only after reviewing what is staged. This site is public, so screenshots, logs, credentials, IPs, and private class/work material should be checked before publishing.

## Content Rule

LaunchShell pages should stay beginner-friendly, practical, and safety-conscious. The goal is to show real project work and clear learning paths without publishing sensitive details.
