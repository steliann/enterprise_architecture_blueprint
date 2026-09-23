# Word Style — Architecture Blueprint Customer Report

## Design intent

Use a clean Qlik white-paper visual language:

- white page;
- generous whitespace;
- green architecture headings;
- dark grey body text;
- teal table headers;
- restrained light-green/light-teal callouts;
- minimal decorative elements.

The style definition is self-contained. Do not require the original reference
document.

## Page

- A4 portrait.
- Margins approximately 0.65–0.75 in.
- Avoid dense edge-to-edge tables.
- Keep major headings with the paragraph that follows.

## Cover

Use a simple branded white-paper treatment:

- small uppercase eyebrow: `ARCHITECTURE BLUEPRINT`;
- large green customer/report title;
- grey subtitle: `Current Architecture Baseline`;
- date / status / confidentiality in smaller muted text;
- thin generated green/teal line motif near the top or lower third.

Do not embed the original reference cover artwork.

## Typography

Preferred:

- body: Inter;
- report cover/display title: Noto Serif or a similar restrained serif;
- fallback fonts are defined in `style-tokens.yaml`.

Typical sizes:

- cover title: 28–31 pt;
- section heading: 18 pt green;
- subsection heading: 12–13 pt dark green;
- body: ~10.3 pt;
- table: 8–9 pt.

## Heading hierarchy

- H1 / numbered major section: green, prominent, ample space before.
- H2: dark green.
- small contextual heading: dark green or teal, bold.

Do not over-number below the level useful to the customer.

## Tables

- header fill: teal or dark green;
- header text: white, bold;
- body fill: white;
- light borders;
- first column may be bold for scanability;
- avoid more than four columns when possible.

If a table becomes dense, reduce content before reducing font size.

## Callouts

Use light green or light teal fill with subtle border.

Good uses:

- defining architecture characteristic;
- trust principle;
- material operating dependency;
- transition/future direction;
- important validation note.

Callouts should not look like error banners unless a confirmed serious concern
exists.

## Architecture diagrams

Prefer simple native shapes:

- source domains;
- integration/warehouse;
- shared analytical core;
- specialised products;
- consumers.

Use green for the architectural centre of gravity and neutral/light fills for
supporting layers.

## Header/footer

Keep understated.

Recommended footer:

`<Customer> Architecture Blueprint | Source report vX.Y`

Page number on the right.

## Content density

A polished customer report is normally around 10–18 pages depending on solution
complexity.

Do not try to preserve every Markdown line. Preserve meaning and architecture
significance.
