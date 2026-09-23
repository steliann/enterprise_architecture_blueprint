# Architecture AI

A private, GitHub-backed distribution repository for reusable Architecture AI skills. The repository is intentionally **vendor-neutral at the skill layer**: each capability is packaged as a standard `SKILL.md` folder, while marketplace manifests provide browser distribution for tools that understand the Claude-compatible plugin format.

## Repository model

```text
architecture-ai/
├── .claude-plugin/marketplace.json
├── core/
│   ├── .claude-plugin/plugin.json
│   └── skills/
├── labs/
│   ├── .claude-plugin/plugin.json
│   └── skills/
├── template/skill/
├── spec/
├── scripts/
└── .github/workflows/
```

- **core** — governed skills approved for normal architecture work.
- **labs** — experimental skills being developed or validated.
- **template** — starting point for a new skill.

## Initial skills

### Core
- `architecture-blueprint-review`
- `architecture-blueprint-report`
- `architecture-blueprint-coverage`
- `csp-objectives`
- `adr-authoring`
- `adr-ku-alignment`

### Labs
- `agentic-architecture-review`
- `architecture-knowledge-extraction`

## Private GitHub deployment

Keep the repository private and grant users normal GitHub read access. For local/IDE agents that support the Agent Skills convention, users can install from the authenticated Git repository. Example pattern:

```bash
gh auth login
npx skills add git@github.com:YOUR-ORG/architecture-ai.git --skill architecture-blueprint-review
```

Use your organization's standard GitHub authentication method (SSO, SSH, credential helper, or approved token). Do not embed tokens in repository URLs.

## Browser deployment

### Claude
For individual testing, package a skill folder as a ZIP and upload it through Claude's Skills interface. For managed distribution, configure the private repository as an organization plugin marketplace. Claude reads `.claude-plugin/marketplace.json` and the tier-specific `plugin.json` manifests.

### ChatGPT
For individual testing in a workspace that supports custom skills, upload the skill ZIP. For managed distribution, import the private GitHub repository as a plugin marketplace. The repository deliberately uses the Claude-compatible marketplace layout supported by both ecosystems.

## Validation

```bash
npm install
npm run validate
```

GitHub Actions runs the same checks on pushes and pull requests.

## Governance lifecycle

```text
idea -> labs -> test -> architecture review -> core -> release -> monitor -> revise/deprecate
```

A skill is promoted to `core` only when:
1. its activation conditions are explicit;
2. its expected inputs and outputs are documented;
3. human approval points are defined where decisions or changes are consequential;
4. test cases exist;
5. output schemas/templates are stable; and
6. the Architecture AI maintainers approve the pull request.

## Before first use

Replace `YOUR-ORG`, author names, repository URL, and the placeholder license with organization-specific values.
