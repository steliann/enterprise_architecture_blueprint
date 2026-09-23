import { relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
export const ROOT = resolve(fileURLToPath(new URL("../../", import.meta.url)));
export function createReporter(){
  let failures=0,warnings=0;
  const relPath=(p)=>relative(ROOT,p).replaceAll("\\","/");
  return {
    fail:(m)=>{failures++; console.error(`ERROR: ${m}`)},
    warn:(m)=>{warnings++; console.warn(`WARN: ${m}`)},
    relPath,
    report:()=>{console.log(`Validation complete: ${failures} error(s), ${warnings} warning(s).`); if(failures) process.exitCode=1;}
  };
}
