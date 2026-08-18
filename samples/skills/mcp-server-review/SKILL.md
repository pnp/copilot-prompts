---
name: mcp-server-review
description: Review a Model Context Protocol (MCP) server implementation against the 2026-07-28 protocol revision, which removed the initialize handshake and Mcp-Session-Id and made the protocol stateless. Use when the user asks to review, audit, upgrade or migrate an MCP server, asks whether their MCP server is spec compliant, asks which protocol revision their server implements, or reports that an MCP client cannot connect to their server.
---

# Review an MCP Server Against the 2026-07-28 Revision

Protocol revision `2026-07-28` is the largest change to the Model Context Protocol since it launched. Server code written before it still compiles, still passes its own tests, and still looks correct in review. It simply speaks a shape that modern clients no longer send.

This skill finds that gap. It reviews an MCP server implementation against the current revision, reports what is obsolete, what is missing, and what is a security requirement rather than a nicety, and it distinguishes between a genuine finding and something it could not determine from the code available.

## Before Starting

**Critical**: Always ask the user for the following information before proceeding:

1. **Server code** - the repository, folder, or files implementing the MCP server
2. **Target revision** - the protocol revision the server intends to implement. Defaults to `2026-07-28` if not specified
3. **Transport** - Streamable HTTP or stdio. Defaults to Streamable HTTP if not specified, since the header rules below apply only to it
4. **Backward compatibility requirement** - whether the server must still serve clients on `2025-03-26` through `2025-11-25`. Defaults to no

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

Do not infer the revision from an SDK version number. SDK majors and protocol revisions move independently. Read what the code actually sends and accepts.

## Output Structure

Produce a review report with these sections:

1. **Revision verdict** - one line stating which revision the code appears to implement, and the evidence for that conclusion
2. **Blocking findings** - table of `Finding | Location | Why it breaks | Fix`
3. **Security findings** - the spec's MUST-level security requirements, listed separately because they are not stylistic
4. **Deprecated but working** - features on the twelve month removal clock
5. **Not determined** - checks that could not be evaluated from the code provided, and what to look at to resolve each
6. **Nothing to change** - the checks that passed

The **Not determined** section is required and must never be silently folded into "passed". A reviewer reading a clean report has to be able to tell the difference between "this is correct" and "this was not visible".

Every finding must cite the specific rule it comes from. Do not invent limits or headers. If a rule cannot be tied to the specification, leave it out and say so.

## Step 1: Establish which revision the server implements

Look for the strongest available evidence, in this order:

- An explicit protocol version constant or string, for example `2026-07-28`, `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05`
- The presence or absence of an `initialize` request handler
- The presence or absence of `Mcp-Session-Id` handling
- Whether request handlers read `params._meta` for the protocol version

State the verdict plainly. "This server implements a pre-2026-07-28 revision" is a useful finding on its own, and it is usually the root cause when a client cannot connect.

## Step 2: Find removed features still present

These were removed in `2026-07-28`. Each is a blocking finding for a server that claims to implement it.

| Removed | What to search for | Replacement |
|---|---|---|
| `initialize` / `initialized` handshake (SEP-2575) | A handler for method `initialize`, or `notifications/initialized` | Nothing. Every request is self contained |
| `Mcp-Session-Id` (SEP-2567) | The header name, session stores, sticky routing, `DELETE` to terminate a session | Nothing. Any request may land on any instance |
| GET stream endpoint | A `GET` route on the MCP endpoint that opens SSE | `subscriptions/listen`, whose response is itself the stream |
| Resumable streams | `Last-Event-ID` handling | Not supported. Streams are not resumable |
| Server-initiated JSON-RPC requests on SSE | The server sending a request (not a notification) on a response stream | Multi Round-Trip Requests: return an `InputRequiredResult` containing `inputRequests` |

A server that only supports this revision and receives legacy traffic **should** answer `GET` or `DELETE` on the MCP endpoint with `405 Method Not Allowed`, ignore any `Mcp-Session-Id` it receives without minting or echoing one, and ignore `Last-Event-ID`.

## Step 3: Check the request metadata contract

Under Streamable HTTP the client mirrors body fields into headers so intermediaries can route without parsing the body. The server has obligations on the receiving side.

**Required headers on every POST:**

- `MCP-Protocol-Version` - must equal the `io.modelcontextprotocol/protocolVersion` value inside `params._meta`
- `Mcp-Method` - must equal the body's `method`
- `Mcp-Name` - required for `tools/call`, `resources/read` and `prompts/get`; sourced from `params.name` or `params.uri`

**The server MUST reject disagreement.** If a header and its body value differ, or a required header is missing or malformed, respond `400 Bad Request` with JSON-RPC error code **`-32020`** (`HeaderMismatch`). Verify this is actually implemented, not merely documented. A server that trusts headers without validating them against the body is the exact vulnerability this rule exists to prevent, because a load balancer may route on the header while the server executes on the body.

**The `_meta` keys are exact.** Check for all three:

```
io.modelcontextprotocol/protocolVersion
io.modelcontextprotocol/clientInfo
io.modelcontextprotocol/clientCapabilities
```

**Version negotiation:** an unsupported version must return `400` with an `UnsupportedProtocolVersionError` listing the versions the server does support. An unimplemented method must return `404` with JSON-RPC `-32601`. The JSON-RPC error body is what distinguishes a modern server's `404` from a legacy server that simply does not host the endpoint.

## Step 4: Check response handling

- The endpoint **must** accept `POST`. A request body is a single JSON-RPC request or notification, never a response
- For a **request**, the server returns either `Content-Type: application/json` with one JSON object, or `Content-Type: text/event-stream` with a stream. Either is valid; the client must support both
- For a **notification**, the server returns `202 Accepted` with **no body** when it accepts it
- On an SSE stream, the server may send notifications related to that request before the final response, and the final response should terminate the stream
- Closing the response stream **must** be treated as cancellation of that request. Confirm the server actually stops work rather than merely detaching
- When opening an SSE stream, the server **should** send `X-Accel-Buffering: no` so reverse proxies do not buffer events
- For long-lived `subscriptions/listen` streams, the server is encouraged to emit periodic SSE comment lines (`:`) as keep-alives

## Step 5: Check the security requirements

These are MUST-level in the specification. Report them separately from style findings.

1. **Origin validation.** The server **must** validate the `Origin` header on all incoming connections to prevent DNS rebinding attacks, and respond `403 Forbidden` when it is present and invalid. This is the most commonly missing check in server code
2. **Local binding.** When running locally, bind to `127.0.0.1` rather than `0.0.0.0`
3. **Authentication.** The server should implement proper authentication for all connections

Without the first two, a remote web page can reach a local MCP server through the user's browser.

## Step 6: Check `x-mcp-header` tool annotations

If the server annotates tool parameters for header mirroring, the annotations must be valid or conforming clients will exclude the whole tool from `tools/list`.

An `x-mcp-header` value must:

- Be non-empty and match HTTP field-name token syntax
- Contain no control characters, including CR or LF
- Be case-insensitively unique across the `inputSchema`
- Sit only on **primitive** properties: `string`, `boolean`, `integer`. **`number` is not permitted**
- Be *statically reachable* from the schema root through a chain consisting solely of `properties` keys. The chain must not pass through `items`, `oneOf`, `anyOf`, `allOf`, `not`, `if`/`then`/`else`, or `$ref`

Also confirm the server **decodes** the Base64 sentinel form before comparing a header to its body value. Values that are not header-safe travel as `=?base64?<base64>?=`, and a plain value that merely looks like the sentinel is also encoded. A server that compares the raw header against the body will reject valid requests from conforming clients.

## Step 7: Flag deprecated features

Deprecated in this revision, with a twelve month minimum window before removal. These are not blocking, but a server still relying on them needs a migration plan.

- Roots
- Sampling
- Logging
- Dynamic Client Registration, in favour of Client ID Metadata Documents
- The legacy HTTP+SSE transport from `2024-11-05`

## Step 8: Check what the revision added

Not implementing these is not a defect, but they are the reason to move:

- **Stateless operation.** No session store, no sticky routing. Confirm nothing in the server assumes affinity between requests
- **`server/discover`.** An optional RPC letting a client learn capabilities without a handshake
- **Cacheable list results.** `tools/list`, `prompts/list`, `resources/list` and `resources/read` may return `ttlMs` and `cacheScope`
- **Multi Round-Trip Requests.** Server-to-client interaction is returned inside a result rather than sent as a separate request

## Step 9: Write the report

Follow the Output Structure above. Then apply these rules before returning it:

- **Cite the rule** behind every finding. A finding a reader cannot verify is not actionable
- **Separate MUST from SHOULD.** The specification distinguishes them and so should the report
- **Put anything unverifiable in "Not determined"**, never in "passed". If the auth path is in a separate service you cannot see, say that
- **Do not guess header names, error codes or limits.** If you are unsure, check the specification at https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http rather than writing from memory. The single most likely way to produce a wrong review of this revision is to describe the protocol as you remember it

## Reference

- Streamable HTTP transport: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
- What changed in 2026-07-28: https://blog.modelcontextprotocol.io/posts/2026-07-28
- Specification index: https://modelcontextprotocol.io/specification/latest
