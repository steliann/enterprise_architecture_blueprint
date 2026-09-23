# Deployment Guide

## 1. Create the private GitHub repository

1. Create `YOUR-ORG/architecture-ai` as **Private** or **Internal** according to policy.
2. Push this repository.
3. Protect `main` and require pull-request review.
4. Require the `Validate skills` workflow before merge.
5. Grant users/teams read access and maintainers write access.

## 2. Local / IDE agent installation

Authenticate with GitHub first, then install a specific skill from the repository using the skill installer supported by your agent environment. Example:

```bash
gh auth login
npx skills add git@github.com:qlik-all/enterprise_architecture_blueprint.git --skill architecture-blueprint-review
```

Use the full SSH URL for private repositories when shorthand resolution is unreliable.

## 3. Claude browser

### Individual testing
Create a ZIP containing one skill folder and upload it in the Claude Skills UI. The release workflow can generate these ZIPs automatically.

### Managed deployment
Configure the private GitHub repository as an organization marketplace. The root `.claude-plugin/marketplace.json` exposes `architecture-ai-core` and `architecture-ai-labs` separately. Restrict the labs plugin to the development group if your workspace allows this.

## 4. ChatGPT browser

### Individual testing
Upload a generated skill ZIP where custom Skills are enabled for the workspace.

### Managed deployment
Import the private GitHub repository as the workspace plugin marketplace. The repository uses the compatible `.claude-plugin/marketplace.json`/`plugin.json` structure. Users still need workspace permission to install/use the exposed plugin.

## 5. Release flow

Recommended flow:

```text
feature branch -> labs -> PR -> validation -> human architecture review -> merge
                                           |
                                           +-> promote stable skill to core

core change -> PR -> validation -> merge -> tag/release -> browser marketplace sync
                                                     -> ZIP artifacts for manual upload
```

## 6. Security controls

- Never store GitHub tokens or AI-provider keys in skill files.
- Treat scripts as code and review them accordingly.
- Keep customer data outside the skill repository.
- Prefer explicit read-only tool permissions unless a skill genuinely requires write actions.
- For write-capable skills, document approval gates in `SKILL.md`.
