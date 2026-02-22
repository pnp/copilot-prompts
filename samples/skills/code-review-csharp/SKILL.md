---
name: code-review-csharp
description: Perform structured code reviews of C# source code covering naming conventions, performance, security, readability, and .NET best practices. Trigger phrases include "review this C# code", "check my C# for best practices", "analyze this C# class", "find issues in my C# code".
---

# Review C# Code for Best Practices

Perform a structured code review of C# source code. Identify issues related to naming conventions, performance, security, readability, and .NET best practices. Produce a prioritized report with actionable suggestions.

## Gather Context

Before reviewing, determine:

1. **Code to review** — the C# file, class, or snippet. If the user points to a file, read it. If they paste code, use it directly.
2. **Review focus** — what to prioritize:
   - `all` (default) — full review across all categories
   - `naming` — naming conventions only
   - `performance` — performance and memory only
   - `security` — security vulnerabilities only
   - `readability` — clarity, structure, and maintainability only
3. **Target framework** — the .NET version. Default to .NET 8 if not specified. Auto-detect from `<TargetFramework>` in `.csproj` if accessible.
4. **Severity threshold** — `all` (default), `warnings-and-above`, or `critical-only`.

**If context is missing:** Default to `all` focus, .NET 8, and `all` severities. Don't block the review to ask — just state your assumptions at the top of the report. Only ask if you genuinely have no code to review.

## Report Format

```markdown
# Code Review: {FileName or ClassName}

> Target: .NET {version} | Focus: {focus} | Reviewed: {date}

## Summary

{One-paragraph overview. Lead with the most important finding. State the total issue count by severity.}

## Issues

| # | Severity | Location | Issue | Why It Matters | Suggestion |
|---|----------|----------|-------|----------------|------------|
| 1 | Critical | `Class.Method:L12` | {issue} | {impact} | {fix} |
| 2 | Warning  | `Class.Property`   | {issue} | {impact} | {fix} |
| 3 | Info     | `Class.Method:L25` | {issue} | {impact} | {fix} |

## What's Done Well

- {Positive pattern — be specific, not generic}

## Recommendations

1. **[Critical]** {Highest-impact change}
2. **[Warning]** {Next priority}
3. ...
```

**Severity levels:**
- **Critical** — bugs, security vulnerabilities, data loss risks. Fix immediately.
- **Warning** — convention violations, performance pitfalls, maintainability concerns. Fix soon.
- **Info** — style preferences, minor modernization opportunities. Fix when convenient.

## Review Categories

### 1. Structure and Design

- Single Responsibility Principle — does the class do too many things?
- File length and class complexity
- Namespace organization
- Unnecessary or missing `using` directives
- Dependency injection — is `new` used where DI should be?
- Constructor complexity — too many dependencies suggests SRP violation
- Proper use of `sealed` on classes not designed for inheritance

### 2. Naming Conventions

Verify against [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions):

| Element | Convention | Example |
|---------|-----------|---------|
| Classes, records, structs | PascalCase | `UserManager` |
| Interfaces | `I` + PascalCase | `IUserRepository` |
| Methods | PascalCase | `GetUserById` |
| Properties | PascalCase | `FirstName` |
| Public constants/statics | PascalCase | `MaxRetryCount` |
| Private fields | `_camelCase` | `_userCount` |
| Local variables, parameters | camelCase | `userId` |
| Enum types and values | PascalCase | `OrderStatus.Pending` |
| Type parameters | `T` + PascalCase | `TEntity`, `TKey` |
| Async methods | PascalCase + `Async` suffix | `GetUserAsync` |
| Booleans | `Is`/`Has`/`Can`/`Should` prefix | `IsActive`, `HasPermission` |
| Event handlers | PascalCase + `EventArgs` | `OnUserCreated` |

### 3. Performance

Check for:

- String concatenation in loops → suggest `StringBuilder` or `string.Join`
- Unnecessary allocations: boxing, repeated `ToList()`, `new` in hot paths
- `async void` → should be `async Task` (except event handlers)
- `Task.Result` or `Task.Wait()` → deadlock risk, use `await` instead
- Missing `ConfigureAwait(false)` in library code
- Sync-over-async (`Task.Run(() => AsyncMethod().Result)`)
- `IEnumerable` multiple enumeration → materialize with `ToList()` or use `IReadOnlyList`
- LINQ misuse: `Count() > 0` → `Any()`, `.Count()` on `ICollection` → `.Count`
- Missing `IDisposable` / `using` / `await using` for disposable resources
- Unnecessary `Task.Run` on already-async code
- Large `struct` types being copied repeatedly (consider `ref` or `class`)

### 4. Security

Check for:

- **SQL injection** — string concatenation or interpolation in SQL → use parameterized queries
- **Hardcoded secrets** — connection strings, API keys, passwords in source → use configuration/secrets management
- **Missing input validation** — public method parameters not validated → add guard clauses
- **Exception information leakage** — returning stack traces or internal messages to callers → use generic error responses
- **Null safety** — missing null checks, inconsistent nullable reference type annotations
- **Insecure cryptography** — MD5/SHA1 for security purposes, custom crypto → use standard libraries
- **Unsafe deserialization** — `BinaryFormatter`, `TypeNameHandling.All` in JSON → use safe serializers
- **Path traversal** — user input in file paths without sanitization
- **`HttpClient` misuse** — creating new instances per request → use `IHttpClientFactory`
- **LINQ injection** — dynamic LINQ from user input without sanitization

### 5. Readability and Maintainability

Check for:

- Methods over ~30 lines → suggest extraction
- Deeply nested conditionals (3+ levels) → suggest guard clauses or early returns
- Magic numbers and strings → extract to named constants
- Outdated or misleading comments (worse than no comments)
- Missing XML doc comments on public API members
- Inconsistent formatting and whitespace
- Modern C# opportunities (based on target framework):
  - Pattern matching (`is`, `switch` expressions)
  - File-scoped namespaces (.NET 6+)
  - Primary constructors (.NET 8+)
  - Records for immutable data types
  - `var` usage consistency
  - Collection expressions (.NET 8+)
  - Raw string literals (.NET 7+)
  - `required` properties (.NET 7+)

## Rules

**Do:**

- Explain **why** each issue matters, not just what to change
- Be specific about locations — class name, method name, and line number where possible
- Acknowledge good patterns — at least 1-2 things done well. A review that only lists problems is demoralizing.
- Respect the target framework — don't suggest `.NET 8` features for a `.NET 6` project
- Sort issues by severity: Critical → Warning → Info
- If the code has no issues, say so. Don't invent problems to fill a report.
- If asked to fix issues (not just review), apply the changes directly

**Don't:**

- Modify code unless the user explicitly asks you to apply fixes
- Flag framework-specific features as issues when they match the target version
- Report false positives — every issue must be verifiable in the code
- Be vague — "consider improving performance" is not actionable. Say exactly what to change and why.
- Overwhelm with low-severity noise — if there are many Info items, summarize them rather than listing each one

## Example

**Input:**

```csharp
public class userManager
{
    string connStr = "Server=prod;Password=admin123";

    public void deleteUser(int id)
    {
        var sql = "DELETE FROM Users WHERE Id = " + id;
        // execute sql
    }

    public List<string> GetNames(List<User> users)
    {
        List<string> result = new List<string>();
        for (int i = 0; i < users.Count; i++)
        {
            result.Add(users[i].FirstName + " " + users[i].LastName);
        }
        return result;
    }
}
```

**Output:**

# Code Review: userManager

> Target: .NET 8 (assumed) | Focus: all | Reviewed: 2026-02-18

## Summary

This class has **2 critical security issues** that need immediate attention: hardcoded credentials and a SQL injection vulnerability. There are also naming convention violations and missed opportunities for modern C# patterns. 6 issues total (2 Critical, 3 Warning, 1 Info).

## Issues

| # | Severity | Location | Issue | Why It Matters | Suggestion |
|---|----------|----------|-------|----------------|------------|
| 1 | Critical | `userManager.connStr` | Hardcoded connection string with plaintext password | Credentials in source code end up in version control and are trivially extractable | Move to `appsettings.json` + secrets management (e.g., Azure Key Vault, User Secrets for dev) |
| 2 | Critical | `userManager.deleteUser:L6` | SQL injection via string concatenation | Attacker-controlled input can execute arbitrary SQL | Use parameterized queries or an ORM (e.g., Entity Framework, Dapper with parameters) |
| 3 | Warning | Class declaration | `userManager` violates PascalCase convention | Inconsistent naming makes the codebase harder to navigate | Rename to `UserManager` |
| 4 | Warning | `deleteUser` method | Method name violates PascalCase convention | Same as above | Rename to `DeleteUser` |
| 5 | Warning | `connStr` field | Private field missing `_` prefix and access modifier | Implicit `private` is less readable; missing prefix breaks convention | Rename to `_connectionString` with explicit `private` |
| 6 | Info | `GetNames` method | Manual loop with string concatenation where LINQ would be clearer | LINQ expresses intent more directly and reduces boilerplate | `users.Select(u => $"{u.FirstName} {u.LastName}").ToList()` |

## What's Done Well

- `GetNames` returns a clearly typed `List<string>` — good use of explicit return types
- Method names are descriptive of their intent (`deleteUser`, `GetNames`)

## Recommendations

1. **[Critical]** Remove hardcoded credentials — externalize all secrets to configuration
2. **[Critical]** Replace concatenated SQL with parameterized queries throughout the codebase
3. **[Warning]** Apply consistent PascalCase naming to all classes, methods, and properties
4. **[Info]** Modernize `GetNames` with LINQ and string interpolation

## Pre-Delivery Checklist

Before finalizing the report, verify:

- [ ] Every reported issue is real and verifiable in the code — no false positives
- [ ] Each issue has a severity, location, explanation, and actionable suggestion
- [ ] At least 1-2 positive patterns acknowledged
- [ ] Recommendations are ordered by impact
- [ ] Suggestions are compatible with the target .NET version
- [ ] Security issues (if any) are marked Critical
- [ ] Report follows the defined format