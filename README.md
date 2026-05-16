# LaunchShell

**Build. Launch. Repeat.**

[LaunchShell.org](https://www.launchshell.org/) is a student-built project journal and guide site for practical technology builds: Linux, cloud servers, Git/GitHub, Python scripts, web apps, electronics, virtual machines, and safe beginner cybersecurity labs.

The site is intentionally simple. It is plain HTML and CSS so the content stays easy to inspect, edit, commit, and publish.

## Live Site

- [Homepage](https://www.launchshell.org/) — `index.html`
- [Guides](https://www.launchshell.org/guides/) — `guides/index.html`
- [Projects](https://www.launchshell.org/projects/) — `projects/index.html`
- [Resources](https://www.launchshell.org/resources/) — `resources/index.html`
- [Book Recommendations](https://www.launchshell.org/resources/book-recommendations/) — `resources/book-recommendations/index.html`

## Homepage Sections

- Start here
- Featured guides and projects
- Suggested learning paths
- LaunchShell method
- Free and low-cost student resources

## Guides

- [Linux Terminal Intro](https://www.launchshell.org/guides/linux-terminal-intro/) — `guides/linux-terminal-intro/`
- [AWS Free VPS Setup](https://www.launchshell.org/guides/aws-free-vps/) — `guides/aws-free-vps/`
- [What Is a VM?](https://www.launchshell.org/guides/what-is-a-vm/) — `guides/what-is-a-vm/`
- [What Is Hacking?](https://www.launchshell.org/guides/what-is-hacking/) — `guides/what-is-hacking/`
- [Git and GitHub](https://www.launchshell.org/guides/git-and-github/) — `guides/git-and-github/`
- [GitHub Codespaces](https://www.launchshell.org/guides/github-codespace/) — `guides/github-codespace/`
- [Use Libby With Your Library](https://www.launchshell.org/guides/libby/) — `guides/libby/`
- [Cloudflare Pages](https://www.launchshell.org/guides/cloudflare/) — `guides/cloudflare/`
- [IT and Cybersecurity Certifications](https://www.launchshell.org/guides/certification/) — `guides/certification/`

## Projects

- [Build and Deploy a Flask JSON App](https://www.launchshell.org/projects/cheap-server-web-app/) — `projects/cheap-server-web-app/`
- [Small Python Projects and Diceware](https://www.launchshell.org/projects/python/) — `projects/python/`
- [T-Pot Honeynet Project](https://www.launchshell.org/projects/tpot-honeynet/) — `projects/tpot-honeynet/`
- [8-Bit Computer and ROM Tooling](https://www.launchshell.org/projects/8-bit/) — `projects/8-bit/`
- [JSON Book Recommendations](https://www.launchshell.org/projects/json-book-recommendation/) — `projects/json-book-recommendation/`
- [How This Site Was Built](https://www.launchshell.org/projects/build-this-site/) — `projects/build-this-site/`

## Resources

- [Student Resources](https://www.launchshell.org/resources/) — `resources/index.html`
- [Top 30 Book Recommendations](https://www.launchshell.org/resources/book-recommendations/) — `resources/book-recommendations/`
- Book recommendation data — `resources/book-recommendations/books_public.json`

## Tech Stack

- Plain HTML
- Shared CSS
- Local assets
- No framework
- No build step
- No backend
- No package manager

## Repository Structure

```text
.
├── assets/
│   ├── site.css
│   └── shared images and icons
├── guides/
│   ├── aws-free-vps/
│   ├── certification/
│   ├── cloudflare/
│   ├── git-and-github/
│   ├── github-codespace/
│   ├── libby/
│   ├── linux-terminal-intro/
│   ├── what-is-a-vm/
│   └── what-is-hacking/
├── projects/
│   ├── 8-bit/
│   ├── build-this-site/
│   ├── cheap-server-web-app/
│   ├── json-book-recommendation/
│   ├── python/
│   └── tpot-honeynet/
├── resources/
│   ├── book-recommendations/
│   │   ├── books_public.json
│   │   └── index.html
│   └── index.html
├── index.html
└── README.md
```

## Deployment

Deployment target: [Cloudflare Pages](https://www.launchshell.org/guides/cloudflare/).

Cloudflare Pages can serve this repository directly because the root page is `index.html` and all pages/assets are committed into the repository.

## Edit Workflow

Make a small content or style change, check it locally, then commit:

```sh
git status --short
git diff --check
git add <files>
git commit -m "Describe the site update"
```

Push only after reviewing what is staged:

```sh
git push
```

This site is public, so screenshots, logs, credentials, IPs, and private class/work material should be checked before publishing.

## Content Rule

LaunchShell pages should stay beginner-friendly, practical, and safety-conscious.

The goal is to show real project work, clear learning paths, and public portfolio evidence without publishing sensitive details.
