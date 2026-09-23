#!/usr/bin/env node
import { existsSync, readFileSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { ROOT, createReporter } from "./lib/reporter.mjs";
const ctx=createReporter(); const {fail,warn,relPath}=ctx;
function readJSON(p){try{return JSON.parse(readFileSync(p,"utf8"))}catch(e){fail(`${relPath(p)}: invalid JSON — ${e.message}`);return null}}
const p=join(ROOT,".claude-plugin","marketplace.json");
if(!existsSync(p)){fail(".claude-plugin/marketplace.json is missing"); ctx.report(); process.exit();}
const m=readJSON(p); if(m){ for(const f of ["name","description","plugins"]) if(!(f in m)) fail(`marketplace.json missing "${f}"`); if(!Array.isArray(m.plugins)) fail("marketplace.json plugins must be an array"); else { const names=new Set(); for(const pl of m.plugins){ for(const f of ["name","description","source"]) if(!pl?.[f]) fail(`plugin ${pl?.name||'<unnamed>'} missing "${f}"`); if(!pl?.source) continue; if(names.has(pl.name)) fail(`duplicate plugin name ${pl.name}`); names.add(pl.name); const dir=resolve(ROOT,pl.source); if(relative(ROOT,dir).startsWith('..')){fail(`plugin ${pl.name} source escapes repository root`);continue;} if(!existsSync(dir)||!statSync(dir).isDirectory()){fail(`plugin ${pl.name} source ${pl.source} not found`);continue;} const pj=join(dir,'.claude-plugin','plugin.json'); if(!existsSync(pj)){fail(`${relPath(pj)} missing`);continue;} const manifest=readJSON(pj); if(manifest && manifest.name!==pl.name) warn(`${relPath(pj)} name differs from marketplace entry`); } }}
ctx.report();
