import { access, readFile, readdir } from "node:fs/promises";
import assert from "node:assert/strict";
import path from "node:path";

const siteRoot = path.resolve(import.meta.dirname, "..");
const repositoryRoot = path.resolve(siteRoot, "..");
const distRoot = path.join(siteRoot, "dist");
const basePath = "/copilot-prompts/";
const htmlFiles = [];

async function collectHtml(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await collectHtml(entryPath);
    } else if (entry.name.endsWith(".html")) {
      htmlFiles.push(entryPath);
    }
  }
}

async function targetExists(url) {
  const decodedPath = decodeURIComponent(url.pathname.slice(basePath.length));
  const filePath = path.join(distRoot, ...decodedPath.split("/").filter(Boolean));
  const candidates = url.pathname.endsWith("/")
    ? [path.join(filePath, "index.html"), `${filePath.replace(/[\\/]$/, "")}.html`]
    : [filePath, `${filePath}.html`, path.join(filePath, "index.html")];
  for (const candidate of candidates) {
    try {
      await access(candidate);
      return true;
    } catch {}
  }
  return false;
}

await collectHtml(distRoot);
const catalog = JSON.parse(await readFile(path.join(distRoot, "catalog.json"), "utf8"));
assert(Array.isArray(catalog), "Built catalog must be an array");
const catalogByRoute = new Map(catalog.map((sample) => [sample.route, sample]));
assert.equal(catalogByRoute.size, catalog.length, "Built catalog contains duplicate routes");
const home = await readFile(path.join(distRoot, "index.html"), "utf8");
const homeLinks = new Set([...home.matchAll(/\shref=["']([^"']+)["']/g)].map((match) => match[1]));
const builtPages = new Set(htmlFiles);
let sampleCount = 0;
for (const category of ["prompts", "agent-instructions", "skills"]) {
  const categoryRoot = path.join(repositoryRoot, "samples", category);
  const entries = await readdir(categoryRoot, { withFileTypes: true });
  for (const entry of entries.filter((candidate) => candidate.isDirectory())) {
    const route = `samples/${category}/${entry.name}`;
    const metadata = JSON.parse(await readFile(path.join(categoryRoot, entry.name, "assets", "sample.json"), "utf8"));
    const sample = catalogByRoute.get(route);
    assert(sample, `Sample missing from built catalog: ${route}`);
    assert.equal(sample.name, metadata[0].name, `Catalog identity mismatch: ${route}`);
    assert(builtPages.has(path.join(distRoot, ...route.split("/"), "index.html")), `Sample detail page missing: ${route}`);
    assert(homeLinks.has(`${basePath}${route}/`), `Sample missing from gallery home page: ${route}`);
    catalogByRoute.delete(route);
    sampleCount += 1;
  }
}
assert.equal(catalogByRoute.size, 0, `Unexpected catalog routes: ${[...catalogByRoute.keys()].join(", ")}`);
console.log(`[gallery] verified all ${sampleCount} repository samples in the catalog, home page, and detail pages`);

const broken = [];
const checked = new Set();
for (const htmlPath of htmlFiles) {
  const html = await readFile(htmlPath, "utf8");
  const route = `/${path.relative(distRoot, htmlPath).replaceAll(path.sep, "/").replace(/index\.html$/, "")}`;
  const pageUrl = new URL(route, "https://pnp.github.io");
  for (const match of html.matchAll(/\s(?:href|src)=["']([^"'#]+)["']/g)) {
    const url = new URL(match[1], pageUrl);
    if (url.origin !== "https://pnp.github.io" || !url.pathname.startsWith(basePath)) {
      continue;
    }
    url.hash = "";
    const identity = url.href;
    if (checked.has(identity)) {
      continue;
    }
    checked.add(identity);
    if (!(await targetExists(url))) {
      broken.push(`${path.relative(distRoot, htmlPath)} -> ${url.pathname}`);
    }
  }
}

if (broken.length > 0) {
  throw new Error(`Broken internal links:\n${broken.join("\n")}`);
}

console.log(`[gallery] validated ${checked.size} internal links and assets across ${htmlFiles.length} pages`);
