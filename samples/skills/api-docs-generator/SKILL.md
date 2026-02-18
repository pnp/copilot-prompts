---
name: api-docs-generator
description: This skill should be used when the user asks to "generate API documentation", "document this API", "create API docs", "scaffold API reference docs", "write endpoint documentation", or needs to generate structured API reference documentation from source code, OpenAPI specs, or code comments.
---

# Generate API Reference Documentation

This skill generates structured API reference documentation from source code files, controllers, or OpenAPI/Swagger specifications. It produces clean Markdown documentation covering endpoints, parameters, request/response schemas, authentication, and usage examples.

## Before Starting

**Critical**: Always gather the following before proceeding:

1. **Source material** — one of the following:
   - A source code file (controller, route handler, service class)
   - An OpenAPI/Swagger specification file (JSON or YAML)
   - A set of files the user points to
2. **API name** — the name of the API or service (e.g., "User Management API")
3. **Output format** — how the docs should be organized. Options:
   - `single-file` (default) — one Markdown file with all endpoints
   - `per-endpoint` — separate Markdown file per endpoint
4. **Base URL** — the API's base URL (e.g., `https://api.example.com/v1`). Use a placeholder if unknown.
5. **Authentication method** — how the API authenticates requests. Common values:
   - `Bearer token` (default if not specified)
   - `API key`
   - `OAuth 2.0`
   - `None`
6. **Language/framework** — the backend language and framework (e.g., ASP.NET Core, Express.js, FastAPI). Auto-detect from source code if not specified.

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Output Structure

### Single-File Format (default)

```markdown
# {API Name} — API Reference

> Base URL: `{base-url}`
> Authentication: {auth-method}
> Version: {version}

## Table of Contents
- [Authentication](#authentication)
- [{Resource Group 1}](#{resource-group-1})
  - [{Method} {Path}](#{endpoint-anchor})
- [{Resource Group 2}](#{resource-group-2})
  - ...

## Authentication
{How to authenticate — headers, tokens, etc.}

## {Resource Group}

### {HTTP Method} `{path}`

{Short description of what the endpoint does.}

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `id` | path | integer | ✅ | The user's unique ID |
| `limit` | query | integer | ❌ | Max results (default: 20) |

**Request Body**

```json
{
  "field": "type — description"
}
```

**Response**

| Status | Description |
|--------|-------------|
| `200 OK` | Success — returns {description} |
| `404 Not Found` | Resource not found |

```json
{
  "example": "response"
}
```

**Example**

```bash
curl -X GET "{base-url}/{path}" \
  -H "Authorization: Bearer {token}"
```
```

### Per-Endpoint Format

Creates one file per endpoint named `{method}-{path-slug}.md` (e.g., `get-users-id.md`), each following the same endpoint template above, plus a `README.md` index file linking to all endpoints.

## Step 1: Analyze the Source

Read the source material and identify:
- All API endpoints (HTTP method + path)
- Route parameters, query parameters, and request body schemas
- Response types and status codes
- Authentication requirements
- Grouping by resource (e.g., Users, Orders, Products)
- Any existing doc comments, decorators, or annotations (e.g., `/// <summary>`, `@ApiOperation`, JSDoc)

Sort endpoints by resource group, then by path, then by HTTP method order: GET → POST → PUT → PATCH → DELETE.

## Step 2: Extract Parameter Details

For each endpoint, document:
- **Path parameters** — identify from route template (e.g., `/users/{id}`)
- **Query parameters** — identify from method signatures, decorators, or spec
- **Request body** — identify the schema/model, include field types and descriptions
- **Headers** — any custom headers beyond standard auth

For each parameter, determine:
- Name, location (path/query/header/body), type, required/optional, default value, description

## Step 3: Document Response Schemas

For each endpoint, document:
- All possible HTTP status codes and their meaning
- Response body schema with field types
- Provide a realistic JSON example for the success case (200/201)
- Document error response format if consistent across the API

## Step 4: Write Authentication Section

Document how to authenticate:
- Where to include credentials (header, query param, cookie)
- Format (e.g., `Authorization: Bearer {token}`)
- How to obtain credentials (link to auth endpoint or external provider)
- Token expiration and refresh (if applicable)

## Step 5: Generate Usage Examples

For each endpoint, provide a `curl` example showing:
- The full URL with path parameters filled in with realistic sample values
- Required headers (including auth)
- Request body (for POST/PUT/PATCH)
- Use realistic but obviously fake data (e.g., `user@example.com`, `acme-corp`)

## Step 6: Assemble Documentation

Combine all sections following the Output Structure:
1. Write the header with API name, base URL, auth method, and version
2. Generate the Table of Contents with anchor links
3. Write the Authentication section
4. Write each resource group with its endpoints
5. Add a footer with generation timestamp

## Rules

- **Extract documentation from the source — do not invent endpoints or parameters** that don't exist in the code
- **Use the exact route paths, parameter names, and types** from the source code
- **Preserve any existing descriptions** from doc comments, annotations, or OpenAPI descriptions
- **Every endpoint must have at least one curl example**
- **Response examples must be realistic** — use plausible fake data, not `"string"` or `"value"`
- **Group endpoints by resource** (e.g., all `/users/*` endpoints together)
- **Sort within groups**: GET → POST → PUT → PATCH → DELETE
- **If the source code is ambiguous**, note the ambiguity in the docs rather than guessing
- **Include both success and error responses** for each endpoint where possible
- **Use standard HTTP status code descriptions** (200 OK, 201 Created, 400 Bad Request, etc.)

## Examples

### Example: Documenting an ASP.NET Core controller

**Input:**
```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    /// <summary>
    /// Gets a user by their ID.
    /// </summary>
    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        // ...
    }

    /// <summary>
    /// Creates a new user.
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser([FromBody] CreateUserRequest request)
    {
        // ...
    }
}
```

**Output:**

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

**Response**

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

**Response**

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

## Validation Checklist

Before finalizing, verify:
- [ ] Every endpoint from the source is documented (none missing)
- [ ] No endpoints were invented that don't exist in the source
- [ ] All parameters have correct name, location, type, and required status
- [ ] Every endpoint has at least one curl example
- [ ] Response examples use realistic fake data
- [ ] Endpoints are grouped by resource and sorted by HTTP method
- [ ] Authentication section accurately describes the auth mechanism
- [ ] Table of Contents links are correct
- [ ] All code blocks have correct language tags

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [ASP.NET Core Web API Documentation](https://learn.microsoft.com/en-us/aspnet/core/tutorials/web-api-help-pages-using-swagger)
