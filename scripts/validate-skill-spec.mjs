#!/usr/bin/env node
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { ROOT, createReporter } from "./lib/reporter.mjs";

const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const SEMVER_RE = /^\d+\.\d+\.\d+$/;
const TIERS = ["core", "labs"].map((label) => ({ label, skillsDir: join(ROOT, label, "skills") }));

function parseFrontmatter(raw) {
  const match = raw.match(/^(?:\uFEFF)?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) return null;
  const block = match[1];
  const getScalar = (key) => {
    const m = block.match(new RegExp(`^${key}:\\s*([^>\\n][^\\n]*)$`, "m"));
    return m ? m[1].trim().replace(/^['"]|['"]$/g, "") : null;
  };
  const getFolded = (key) => {
    const lines = block.split(/\r?\n/);
    const idx = lines.findIndex((l) => new RegExp(`^${key}:\\s*>-?\\s*$`).test(l));
    if (idx < 0) return null;
    const vals = [];
    for (let i = idx + 1; i < lines.length; i++) {
      const l = lines[i];
      if (!/^\s+/.test(l)) break;
      vals.push(l.trim());
    }
    return vals.join(" ").trim();
  };
  const metadataBlock = block.match(/^metadata:\s*\r?\n((?:\s+.*\r?\n?)*)/m)?.[1] ?? "";
  const meta = (key) => metadataBlock.match(new RegExp(`^\\s+${key}:\\s*([^\\n]+)$`, "m"))?.[1]?.trim()?.replace(/^['"]|['"]$/g, "") ?? null;
  return {
    name: getScalar("name"),
    description: getScalar("description") ?? getFolded("description"),
    license: getScalar("license"),
    metadata: { author: meta("author"), version: meta("version") },
  };
}

function validateSkill(path, folder, ctx, seen) {
  const { fail, warn, relPath } = ctx;
  const label = relPath(path);
  const raw = readFileSync(path, "utf8");
  const fm = parseFrontmatter(raw);
  if (!fm) { fail(`${label}: missing YAML frontmatter`); return; }

  for (const f of ["name", "description", "license"]) if (!fm[f]) fail(`${label}: missing required field "${f}"`);
  if (!fm.metadata.author) fail(`${label}: missing metadata.author`);
  if (!fm.metadata.version) fail(`${label}: missing metadata.version`);
  else if (!SEMVER_RE.test(fm.metadata.version)) fail(`${label}: metadata.version must be x.y.z`);

  if (fm.name) {
    if (!NAME_RE.test(fm.name)) fail(`${label}: invalid name "${fm.name}"`);
    if (fm.name !== folder) fail(`${label}: name must match folder "${folder}"`);
    if (seen.has(fm.name)) fail(`${label}: duplicate skill name "${fm.name}" in tier`);
    seen.add(fm.name);
  }
  if (fm.description && fm.description.length > 1024) fail(`${label}: description exceeds 1024 characters`);
  const lines = raw.split("\n").length;
  if (lines > 500) warn(`${label}: ${lines} lines; consider moving detail to references/`);
}

const ctx = createReporter();
for (const { label, skillsDir } of TIERS) {
  if (!existsSync(skillsDir)) { ctx.warn(`${label}/skills does not exist`); continue; }
  const seen = new Set();
  for (const d of readdirSync(skillsDir, { withFileTypes: true }).filter((x) => x.isDirectory())) {
    const p = join(skillsDir, d.name, "SKILL.md");
    if (existsSync(p)) validateSkill(p, d.name, ctx, seen);
  }
}
ctx.report();
