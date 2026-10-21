# Review boundaries

The deterministic helper supports the documented deployment settings JSON contract: EnvironmentVariables (SchemaName, Value) and ConnectionReferences (LogicalName, ConnectionId, ConnectorId). Both sections must be arrays. Names compare case-insensitively and duplicate names are blockers. It does not parse arbitrary unpacked solution formats.

| Finding | Interpretation |
|---|---|
| Missing/empty connection ID | Incomplete explicit unattended mapping; existing target mappings or interactive selection need separate evidence. |
| Connector mismatch | Target mapping differs from template. A nonempty connection ID cannot fix this by itself. |
| Empty/missing variable mapping | Review effective target/default value and intentional emptiness. Never infer requiredness from template blankness. |
| Extra settings entry | Could be stale settings or mismatched template provenance; not proof of import failure. |
| Duplicate/invalid entry | Ambiguous or malformed input prevents trustworthy coverage checks. |
| No findings | Only static mapping coverage complete; every listed live prerequisite remains unverified. |

Configuration values are not echoed. This reduces accidental disclosure but is not a general-purpose sanitizer; other reports, source files, and screenshots still require inspection. Do not include raw settings in a public demonstration.

For secret-type environment variables, validate the intended reference mechanism with official documentation and target evidence. Do not ask for the secret or treat a nonempty string as proof the secret can be resolved.

The helper has deliberately limited placeholder recognition. It cannot determine that every plausible-looking value is correct, detect every unresolved pipeline expression, or validate all connector-specific configuration.
