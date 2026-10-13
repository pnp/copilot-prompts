import type { APIRoute } from "astro";
import { loadCatalog, publicCatalogSample } from "../lib/catalog";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(loadCatalog().map(publicCatalogSample), null, 2), {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
