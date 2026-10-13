import fs from "node:fs";
import path from "node:path";
import { marked } from "marked";
import sanitizeHtml from "sanitize-html";

const repositoryRoot = path.resolve(process.cwd(), "..");

const categories = {
  prompts: "Prompt",
  "agent-instructions": "Agent instruction",
  skills: "Skill",
} as const;

type Category = keyof typeof categories;

interface Thumbnail {
  type: string;
  order: number;
  url: string;
  alt: string;
}

interface Author {
  gitHubAccount: string;
  name: string;
  pictureUrl?: string;
}

interface Reference {
  name: string;
  description?: string;
  url: string;
}

interface Metadata {
  name: string;
  title: string;
  shortDescription: string;
  longDescription: string[];
  creationDateTime: string;
  updateDateTime: string;
  products: string[];
  thumbnails: Thumbnail[];
  authors: Author[];
  references: Reference[];
  url: string;
  downloadUrl: string;
}

export interface CatalogSample extends Metadata {
  category: Category;
  type: (typeof categories)[Category];
  slug: string;
  route: string;
  readmeHtml: string;
}

function requireText(value: unknown, field: string, source: string): asserts value is string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${source}: ${field} must be a non-empty string`);
  }
}

function encodePath(value: string) {
  return value.split("/").map(encodeURIComponent).join("/");
}

function normalizeReadmeTarget(category: Category, slug: string, target: string, image: boolean) {
  const cleanedTarget = decodeURIComponent(target.trim()).replace(/^\[|\]$/g, "");
  if (cleanedTarget === "") {
    return cleanedTarget;
  }
  if (cleanedTarget.startsWith("//")) {
    return `https:${cleanedTarget}`;
  }
  if (/^www\./i.test(cleanedTarget)) {
    return `https://${cleanedTarget}`;
  }
  if (/^(?:[a-z]+:|#)/i.test(cleanedTarget)) {
    return cleanedTarget;
  }

  const normalizedTarget = path.posix.normalize(
    cleanedTarget.replaceAll("\\", "/").replace(/^\/+/, "").replaceAll("//", "/"),
  );
  const repositoryPath = path.posix.normalize(
    path.posix.join("samples", category, slug, normalizedTarget),
  );
  const samplePrefix = `samples/${category}/${slug}/`;
  const sharedImagePrefix = "images/";
  if (!repositoryPath.startsWith(samplePrefix) && !(image && repositoryPath.startsWith(sharedImagePrefix))) {
    throw new Error(`Unsafe README target in ${category}/${slug}: ${target}`);
  }

  const absoluteTarget = path.join(repositoryRoot, ...repositoryPath.split("/"));
  if (!fs.existsSync(absoluteTarget)) {
    throw new Error(`Missing README target in ${category}/${slug}: ${target}`);
  }

  if (!image) {
    return `https://github.com/pnp/copilot-prompts/blob/main/${encodePath(repositoryPath)}`;
  }

  const basePath = import.meta.env.BASE_URL.replace(/\/?$/, "/");
  if (repositoryPath.startsWith(sharedImagePrefix)) {
    return `${basePath}generated/content/shared/${encodePath(repositoryPath.slice(sharedImagePrefix.length))}`;
  }
  return `${basePath}generated/content/${category}/${slug}/${encodePath(repositoryPath.slice(samplePrefix.length))}`;
}

function loadSample(category: Category, slug: string): CatalogSample {
  const sampleDirectory = path.join(repositoryRoot, "samples", category, slug);
  const metadataPath = path.join(sampleDirectory, "assets", "sample.json");
  const readmePath = path.join(sampleDirectory, "README.md");
  const source = path.relative(repositoryRoot, metadataPath);
  const parsed = JSON.parse(fs.readFileSync(metadataPath, "utf8")) as unknown;

  if (!Array.isArray(parsed) || parsed.length !== 1) {
    throw new Error(`${source}: expected a one-item array`);
  }

  const metadata = parsed[0] as Metadata;
  requireText(metadata.name, "name", source);
  requireText(metadata.title, "title", source);
  requireText(metadata.shortDescription, "shortDescription", source);
  requireText(metadata.url, "url", source);
  requireText(metadata.downloadUrl, "downloadUrl", source);

  if (!Array.isArray(metadata.products) || metadata.products.length === 0) {
    throw new Error(`${source}: products must contain at least one item`);
  }
  if (!Array.isArray(metadata.authors) || metadata.authors.length === 0) {
    throw new Error(`${source}: authors must contain at least one item`);
  }
  if (!Array.isArray(metadata.thumbnails) || metadata.thumbnails.length === 0) {
    throw new Error(`${source}: thumbnails must contain at least one item`);
  }

  const readme = fs.readFileSync(readmePath, "utf8");
  const renderableReadme = readme
    .replace(/^#\s+.*(?:\r?\n)+/, "")
    .replace(/^.*https:\/\/m365-visitor-stats\.azurewebsites\.net\/.*$/gim, "");
  const readmeHtml = sanitizeHtml(marked.parse(renderableReadme, { async: false }), {
    allowedTags: sanitizeHtml.defaults.allowedTags.concat(["img"]),
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      img: ["src", "alt", "title"],
    },
    allowedSchemes: ["http", "https", "mailto"],
    transformTags: {
      a: (tagName, attribs) => ({
        tagName,
        attribs: {
          ...attribs,
          href: normalizeReadmeTarget(category, slug, attribs.href ?? "", false),
        },
      }),
      img: (tagName, attribs) => ({
        tagName,
        attribs: {
          ...attribs,
          src: normalizeReadmeTarget(category, slug, attribs.src ?? "", true),
        },
      }),
    },
  });

  const basePath = import.meta.env.BASE_URL.replace(/\/?$/, "/");
  const thumbnails = metadata.thumbnails.map((thumbnail) => {
    const filename = path.basename(decodeURIComponent(new URL(thumbnail.url).pathname));
    return {
      ...thumbnail,
      url: `${basePath}generated/previews/${category}/${slug}/${encodeURIComponent(filename)}`,
    };
  });

  return {
    ...metadata,
    thumbnails,
    category,
    type: categories[category],
    slug,
    route: `samples/${category}/${slug}`,
    readmeHtml,
  };
}

export function loadCatalog(): CatalogSample[] {
  const samples = Object.keys(categories).flatMap((categoryName) => {
    const category = categoryName as Category;
    const directory = path.join(repositoryRoot, "samples", category);
    return fs
      .readdirSync(directory, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => loadSample(category, entry.name));
  });

  const identities = new Set<string>();
  for (const sample of samples) {
    if (identities.has(sample.name)) {
      throw new Error(`Duplicate sample identity: ${sample.name}`);
    }
    identities.add(sample.name);
  }

  return samples.sort((left, right) => left.title.localeCompare(right.title));
}

export function publicCatalogSample({ readmeHtml: _readmeHtml, ...sample }: CatalogSample) {
  return sample;
}
