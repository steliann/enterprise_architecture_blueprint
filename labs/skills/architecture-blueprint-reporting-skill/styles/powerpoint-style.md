# PowerPoint Style — Architecture Blueprint Workshop

## Design intent

Use a restrained Qlik presentation style suitable for architecture discussion:

- 16:9;
- white background;
- dark grey titles;
- green subtitle/accent;
- generous whitespace;
- small Qlik-style header/footer line motif generated from shapes;
- green, teal and dark-blue architecture accents.

The original example presentation is intentionally not included.

## Master composition

Content slide:

- title at top-left;
- optional green subtitle directly below;
- thin generated horizontal green/teal motif along the top-right;
- small footer label bottom-left;
- slide number bottom-right.

Do not reuse or extract the original example slide artwork.

## Typography

Preferred: Inter.

Typical sizes:

- title: 25 pt;
- subtitle: 13–14 pt green;
- body: 10.5–12 pt;
- small annotation: 9 pt;
- KPI number: 32–36 pt.

Avoid shrinking body text below approximately 9 pt.

## Palette

Use `style-tokens.yaml`.

Primary roles:

- Qlik green: architectural centre / primary emphasis;
- teal/deep teal: operating, integration and secondary emphasis;
- dark blue/navy: strong structural bands where needed;
- light green/light blue/light grey: cards and callouts;
- red/amber: only for confirmed concern/status, not normal validation prompts.

## Title slide

Minimal:

- large title;
- green subtitle;
- customer / meeting context;
- date;
- optional small generated line motif.

## Architecture slides

Prefer a visual flow:

`Sources -> Integration & Warehouse -> Shared Core -> Specialised Products / Consumption`

Use:

- rounded rectangles;
- simple chevrons;
- grouped cards;
- thin connectors;
- limited labels.

## KPI slide

Use large numbers in two rows or a grid.

Each KPI has:

- number;
- short label;
- one short context phrase.

Keep the interpretation neutral. Counts express architecture scope, not health.

## Discussion prompts

Use a light green or light blue panel, usually on the right or bottom.

Header examples:

- `DISCUSS / VALIDATE`
- `CONFIRM`
- `CLARIFY`

Keep prompts to 2–4 concise questions.

## Transition slide

A horizontal transition view works well:

- current state;
- transition;
- intended direction.

Do not imply a recommendation unless the direction is already established in
the source.

## Closing slide

For a baseline-only workshop:

**Confirming the architecture baseline**

Summarise the 3–5 items that need customer validation.

Do not introduce gap-analysis framing unless explicitly requested.
