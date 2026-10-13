import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

const repositoryRoot = path.resolve(import.meta.dirname, "..", "..");
const samplesRoot = path.join(repositoryRoot, "samples");
const visitorStatsBaseUrl = "https://m365-visitor-stats.azurewebsites.net/copilot-prompts";
const categories = {
  prompts: "prompt",
  "agent-instructions": "agent",
  skills: "skill",
};

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

let sampleCount = 0;
for (const [category, taxonomy] of Object.entries(categories)) {
  const categoryRoot = path.join(samplesRoot, category);
  const entries = await readdir(categoryRoot, { withFileTypes: true });
  const samples = entries
    .filter((entry) => entry.isDirectory())
    .sort((left, right) => left.name.localeCompare(right.name));

  for (const sample of samples) {
    const identity = `copilotprompts-${taxonomy}-${sample.name}`;
    const expectedTracker = `![](${visitorStatsBaseUrl}/${identity})`;
    const readmePath = path.join(categoryRoot, sample.name, "README.md");
    const metadataPath = path.join(categoryRoot, sample.name, "assets", "sample.json");
    const markdown = await readFile(readmePath, "utf8");
    const metadata = JSON.parse(await readFile(metadataPath, "utf8"));
    const finalLine = markdown.trimEnd().split(/\r?\n/).at(-1)?.trim();
    const trackerCount = (markdown.match(/m365-visitor-stats\.azurewebsites\.net/g) ?? []).length;
    const source = path.relative(repositoryRoot, readmePath);

    assert(finalLine === expectedTracker, `${source}: README must end with ${expectedTracker}`);
    assert(trackerCount === 1, `${source}: README must contain exactly one visitor-stats tracker`);
    assert(Array.isArray(metadata) && metadata.length === 1, `${source}: sample.json must contain one record`);
    assert(metadata[0]?.name === identity, `${source}: sample.json name must be ${identity}`);
    sampleCount += 1;
  }
}

console.log(`[gallery] validated README view trackers and identities for ${sampleCount} samples`);
