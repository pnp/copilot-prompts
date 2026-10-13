import { access, readFile, readdir } from "node:fs/promises";
import path from "node:path";

const siteRoot = path.resolve(import.meta.dirname, "..");
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
