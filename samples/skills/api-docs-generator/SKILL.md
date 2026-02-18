---
name: api-docs-generator
description: Generate structured API reference documentation from source code, OpenAPI specs, or route definitions. Trigger phrases include "generate API docs", "document this API", "create API reference", "write endpoint docs", "scaffold API docs".
---

# API Documentation Generator

Generate clean, structured Markdown API reference docs from source code, OpenAPI/Swagger specs, or route definitions.

## Gather Context

Before writing anything, determine:

1. **Source** — Controller, route file, OpenAPI spec (JSON/YAML), or a set of files?
2. **API name** — e.g., "User Management API". Infer from class/file name if not stated.
3. **Base URL** — e.g., `https://api.example.com/v1`. Default to `https://api.example.com` if unknown.
4. **Auth method** — Bearer token (default), API key, OAuth 2.0, or none.
5. **Output format**:
   - `single-file` (default) — one Markdown file with all endpoints
   - `per-endpoint` — one file per endpoint (`{method}-{path-slug}.md`) plus a `README.md` index
6. **Language/framework** — Auto-detect from file extensions, imports, and decorators.

**If context is missing:** In conversational mode, ask. In agent/inline mode, use sensible defaults and note your assumptions at the top of the output.

## Analyzing the Source

### From Source Code

Read the file(s) and extract:

- Every endpoint: HTTP method + route path
- Route params, query params, request body schemas
- Response types, status codes, and return models
- Auth requirements (per-endpoint if they vary)
- Doc comments, decorators, or annotations (`/// <summary>`, `@ApiOperation`, `@app.get(...)`, JSDoc `@param`/`@returns`, etc.)

**Framework detection hints:**

| Signal | Framework |
|--------|-----------|
| `[ApiController]`, `[HttpGet]` | ASP.NET Core |
| `@app.get()`, `@router.post()` | FastAPI |
| `router.get()`, `app.use()` | Express.js |
| `@GetMapping`, `@RestController` | Spring Boot |
| `@Controller`, `@Get()` | NestJS |
| `resources :users` | Rails |

### From OpenAPI/Swagger Specs

Parse the spec and map directly:

- `paths` → endpoints
- `parameters` → params table
- `requestBody` → request body section
- `responses` → response table + examples
- `components/schemas` → inline the referenced models
- `securityDefinitions` / `securitySchemes` → auth section
- `info.title`, `info.version`, `servers[0].url` → header metadata

Prefer descriptions from the spec. Only infer descriptions when the spec omits them.

### Handling Incomplete Source

If the source references models, DTOs, or types defined in other files:

- Document what's visible. Use the type name as-is (e.g., `UserDto`) and note that the full schema is defined elsewhere.
- If the user provides multiple files, cross-reference them to build complete schemas.
- Never fabricate fields for a model you can't see.

## Documentation Template

````markdown
# {API Name} — API Reference

> Base URL: `{base-url}`
> Authentication: {auth-method}
> Version: {version}

## Table of Contents

- [Authentication](#authentication)
- [{Resource Group}](#{resource-group-slug})
  - [{METHOD} {path}](#{endpoint-anchor})

## Authentication

{How to authenticate: header format, token acquisition, expiration/refresh if known.}

**Header format:**

```
Authorization: Bearer {token}
```

---

## {Resource Group}

### {METHOD} `{path}`

{One-line description from doc comments or inferred from the code.}

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `id` | path | integer | ✅ | Resource ID |
| `limit` | query | integer | ❌ | Max results (default: 20) |

**Request Body** *(POST/PUT/PATCH only)*

```json
{
  "email": "string — the user's email address",
  "displayName": "string — display name"
}
```

**Responses**

| Status | Description |
|--------|-------------|
| `200 OK` | Returns the resource |
| `404 Not Found` | Resource not found |

```json
{
  "id": 42,
  "email": "jane@example.com",
  "displayName": "Jane Smith",
  "createdAt": "2026-01-15T10:30:00Z"
}
```

**Example**

```bash
curl -X GET "{base-url}/{path}" \
  -H "Authorization: Bearer eyJhbG..."
```
````

For `per-endpoint` format: one file per endpoint named `{method}-{path-slug}.md` (e.g., `get-users-id.md`), each using the endpoint section above, plus a `README.md` that links to all of them grouped by resource.

## Common API Patterns to Document

When you encounter these in the source, document them:

- **Pagination** — query params like `page`, `limit`, `offset`, `cursor`. Note defaults and max values if visible.
- **Filtering/sorting** — query params like `sort`, `filter`, `q`, `status`. Document allowed values.
- **Rate limiting** — if headers like `X-RateLimit-*` or decorators like `@Throttle()` are present, add a "Rate Limiting" section.
- **Versioning** — if the API uses path versioning (`/v1/`, `/v2/`) or header versioning, note it in the header.
- **Bulk operations** — endpoints accepting arrays or batch payloads.

## Rules

**Do:**

- Extract only what exists in the source — never invent endpoints, params, or fields
- Use exact route paths, param names, and types from the code
- Preserve existing descriptions from doc comments, annotations, or spec descriptions
- Include a `curl` example for every endpoint
- Use realistic fake data in examples (`jane@example.com`, `42`, `"acme-corp"` — not `"string"` or `"value"`)
- Document both success and error responses
- Use standard HTTP status descriptions (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, etc.)
- Flag ambiguity with a note (e.g., *"Response schema inferred from return type; actual response may differ"*)

**Don't:**

- Invent endpoints or params that aren't in the source
- Use placeholder junk like `"string"`, `"value"`, or `"example"` in response bodies
- Skip error responses — include at least 400 and 404 where applicable
- Assume auth requirements if the code doesn't specify them — note the uncertainty instead

## Example

**Input** — ASP.NET Core controller:

```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    /// <summary>Gets a user by their ID.</summary>
    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(int id) { }

    /// <summary>Creates a new user.</summary>
    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser([FromBody] CreateUserRequest request) { }
}
```

**Output:**

````markdown
# Users API — API Reference

> Base URL: `https://api.example.com`
> Authentication: Bearer token

## Users

### GET `/api/users/{id}`

Gets a user by their ID.

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `id` | path | integer | ✅ | The user's unique ID |

**Responses**

| Status | Description |
|--------|-------------|
| `200 OK` | Returns the user |
| `404 Not Found` | User not found |

```json
{
  "id": 42,
  "email": "jane@example.com",
  "displayName": "Jane Smith",
  "createdAt": "2026-01-15T10:30:00Z"
}
```

**Example**

```bash
curl -X GET "https://api.example.com/api/users/42" \
  -H "Authorization: Bearer eyJhbG..."
```

---

### POST `/api/users`

Creates a new user.

**Request Body**

```json
{
  "email": "string — the user's email address",
  "displayName": "string — the user's display name",
  "role": "string — user role (admin, member, viewer)"
}
```

**Responses**

| Status | Description |
|--------|-------------|
| `201 Created` | User created successfully |
| `400 Bad Request` | Invalid request body |
| `409 Conflict` | Email already exists |

```json
{
  "id": 43,
  "email": "john@example.com",
  "displayName": "John Doe",
  "createdAt": "2026-02-18T14:00:00Z"
}
```

**Example**

```bash
curl -X POST "https://api.example.com/api/users" \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "displayName": "John Doe", "role": "member"}'
```
````

## Pre-Delivery Checklist

- [ ] Every endpoint in the source is documented — none missing, none invented
- [ ] All params have correct name, location (`path`/`query`/`header`/`body`), type, and required status
- [ ] Every endpoint has a `curl` example with realistic data
- [ ] Response examples use plausible fake data, not placeholders
- [ ] Endpoints are grouped by resource and sorted GET → POST → PUT → PATCH → DELETE
- [ ] Auth section matches what the code actually specifies
- [ ] Ambiguities are flagged, not silently assumed
- [ ] TOC anchors resolve correctly