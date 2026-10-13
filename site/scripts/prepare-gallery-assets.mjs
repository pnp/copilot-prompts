import { copyFile, mkdir, readFile, readdir, rm } from "node:fs/promises";
import path from "node:path";

const repositoryRoot = path.resolve(import.meta.dirname, "..", "..");
const outputRoot = path.join(repositoryRoot, "site", "public", "generated", "previews");
const contentOutputRoot = path.join(repositoryRoot, "site", "public", "generated", "content");
const categories = ["prompts", "agent-instructions", "skills"];
const imageExtensions = new Set([".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"]);

await rm(outputRoot, { recursive: true, force: true });
await rm(contentOutputRoot, { recursive: true, force: true });

async function copyImages(sourceRoot, destinationRoot, relativeDirectory = "") {
  const sourceDirectory = path.join(sourceRoot, relativeDirectory);
  const entries = await readdir(sourceDirectory, { withFileTypes: true });
  for (const entry of entries) {
    const relativePath = path.join(relativeDirectory, entry.name);
    if (entry.isDirectory()) {
      await copyImages(sourceRoot, destinationRoot, relativePath);
    } else if (imageExtensions.has(path.extname(entry.name).toLocaleLowerCase("en-US"))) {
      const destination = path.join(destinationRoot, relativePath);
      await mkdir(path.dirname(destination), { recursive: true });
      await copyFile(path.join(sourceRoot, relativePath), destination);
      assetCount += 1;
    }
  }
}

let assetCount = 0;
for (const category of categories) {
  const categoryRoot = path.join(repositoryRoot, "samples", category);
  const entries = await readdir(categoryRoot, { withFileTypes: true });
  for (const entry of entries.filter((candidate) => candidate.isDirectory())) {
    const sampleRoot = path.join(categoryRoot, entry.name);
    const metadataPath = path.join(categoryRoot, entry.name, "assets", "sample.json");
    const metadata = JSON.parse(await readFile(metadataPath, "utf8"))[0];
    const sampleOutput = path.join(outputRoot, category, entry.name);
    await mkdir(sampleOutput, { recursive: true });

    for (const thumbnail of metadata.thumbnails ?? []) {
      const url = new URL(thumbnail.url);
      const pathnameParts = decodeURIComponent(url.pathname).split("/").filter(Boolean);
      const samplesIndex = pathnameParts.indexOf("samples");
      const imagesIndex = pathnameParts.indexOf("images");
      let sourcePath;
      if (samplesIndex >= 0) {
        sourcePath = path.join(repositoryRoot, ...pathnameParts.slice(samplesIndex));
      } else if (imagesIndex >= 0) {
        sourcePath = path.join(repositoryRoot, ...pathnameParts.slice(imagesIndex));
      } else {
        throw new Error(`${metadataPath}: unsupported thumbnail URL ${thumbnail.url}`);
      }

      await copyFile(sourcePath, path.join(sampleOutput, path.basename(sourcePath)));
      assetCount += 1;
    }

    await copyImages(sampleRoot, path.join(contentOutputRoot, category, entry.name));
  }
}

await copyImages(path.join(repositoryRoot, "images"), path.join(contentOutputRoot, "shared"));

console.log(`[gallery] copied ${assetCount} preview assets into the site artifact`);
