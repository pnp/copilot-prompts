---
name: code-review-csharp
description: This skill should be used when the user asks to "review C# code", "check my C# for best practices", "analyze this C# class", "find issues in my C# code", or needs a structured code review of C# source files covering naming conventions, performance, security, and .NET best practices.
---

# Review C# Code for Best Practices

This skill performs a structured code review of C# source code, identifying issues related to naming conventions, performance, security, readability, and .NET best practices. It produces a prioritized report with actionable suggestions.

## Before Starting

**Critical**: Always gather the following before proceeding:

1. **Code to review** — the C# file, class, or code snippet the user wants reviewed. If the user points to a file, read it. If they paste code, use that directly.
2. **Review focus** — what aspects to prioritize. Options:
   - `all` (default) — full review covering all categories
   - `naming` — naming conventions and consistency
   - `performance` — performance and memory considerations
   - `security` — security vulnerabilities and input validation
   - `readability` — code clarity, structure, and maintainability
3. **Target framework** — the .NET version (defaults to .NET 8 if not specified)
4. **Severity threshold** — minimum severity to report. Options: `all` (default), `warnings-and-above`, `critical-only`

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Output Structure

The review produces a structured report in Markdown with these sections:

```markdown
# Code Review: {FileName or ClassName}

## Summary
{One-paragraph overview of code quality, highlighting the most important finding.}

## Issues Found

| # | Severity | Location | Issue | Suggestion |
|---|----------|----------|-------|------------|
| 1 | 🔴 Critical | `ClassName.Method:L12` | {issue} | {fix} |
| 2 | 🟡 Warning | `ClassName.Property` | {issue} | {fix} |
| 3 | 🔵 Info | `ClassName.Method:L25` | {issue} | {fix} |

## Positive Patterns ✅
- {Things the code does well}

## Recommendations
1. {Highest priority change}
2. {Next priority}
3. ...
```

## Step 1: Analyze Code Structure

Examine the overall structure of the code:
- Class organization and responsibility (Single Responsibility Principle)
- File length and complexity
- Namespace usage and organization
- Using directives (unnecessary imports, missing imports)
- Dependency injection patterns

## Step 2: Check Naming Conventions

Verify naming against [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions):
- **Classes, records, structs**: PascalCase (e.g., `UserManager`)
- **Interfaces**: PascalCase with `I` prefix (e.g., `IUserRepository`)
- **Methods**: PascalCase (e.g., `GetUserById`)
- **Properties**: PascalCase (e.g., `FirstName`)
- **Private fields**: camelCase with `_` prefix (e.g., `_userCount`)
- **Local variables and parameters**: camelCase (e.g., `userId`)
- **Constants**: PascalCase (e.g., `MaxRetryCount`)
- **Async methods**: Suffix with `Async` (e.g., `GetUserAsync`)
- **Boolean properties/variables**: Prefix with `Is`, `Has`, `Can`, `Should` where appropriate

## Step 3: Evaluate Performance Patterns

Check for common performance issues:
- String concatenation in loops (suggest `StringBuilder`)
- Unnecessary allocations (boxing, repeated `ToList()`, etc.)
- Missing `ConfigureAwait(false)` in library code
- Sync-over-async or async-over-sync patterns
- IEnumerable multiple enumeration
- LINQ misuse (e.g., `Count()` when `Any()` suffices)
- Missing `IDisposable` implementation or `using` statements

## Step 4: Assess Security Considerations

Look for security issues:
- SQL injection vulnerabilities (string concatenation in queries)
- Missing input validation
- Hardcoded secrets or connection strings
- Improper exception handling that leaks internal details
- Missing null checks (or improper nullable reference type usage)
- Insecure cryptography or hashing

## Step 5: Review Readability and Maintainability

Evaluate code clarity:
- Method length (flag methods over ~30 lines)
- Cyclomatic complexity (deeply nested conditionals)
- Magic numbers and strings (should be constants)
- Comment quality (outdated, redundant, or missing where complex logic exists)
- Consistent formatting and whitespace
- Use of modern C# features where appropriate (pattern matching, records, file-scoped namespaces, etc.)

## Step 6: Generate Report

Produce the report following the Output Structure above:
1. Write a concise Summary paragraph
2. List all issues in the table, sorted by severity (🔴 → 🟡 → 🔵)
3. Acknowledge positive patterns (at least 1–2 things done well)
4. Provide prioritized recommendations (top 3–5 actions)

## Rules

- **NEVER modify the user's code directly** — only report findings and suggest changes
- **Always explain WHY each issue matters**, not just what to change
- **If the code has no issues, say so explicitly** — do not invent problems to fill the report
- **Prioritize issues by severity**: 🔴 Critical (bugs, security) → 🟡 Warning (conventions, performance) → 🔵 Info (style, minor improvements)
- **Be specific about locations** — reference class names, method names, and line numbers where possible
- **Suggest modern C# alternatives** when appropriate, but respect the target framework version
- **Do not flag framework-version-specific features** as issues if they match the user's target framework
- **Acknowledge good patterns** — a review that only lists problems is discouraging; balance criticism with recognition

## Examples

### Example: Reviewing a simple class

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

## Summary
The class has **critical security issues** (hardcoded credentials, SQL injection) alongside naming convention violations and missed opportunities for modern C# patterns. Immediate remediation of the security issues is strongly recommended.

## Issues Found

| # | Severity | Location | Issue | Suggestion |
|---|----------|----------|-------|------------|
| 1 | 🔴 Critical | `userManager.connStr` | Hardcoded connection string with plaintext password | Move to configuration/secrets management (e.g., `appsettings.json` + Azure Key Vault) |
| 2 | 🔴 Critical | `userManager.deleteUser:L6` | SQL injection — string concatenation in SQL query | Use parameterized queries or an ORM like Entity Framework |
| 3 | 🟡 Warning | Class name | `userManager` does not follow PascalCase | Rename to `UserManager` |
| 4 | 🟡 Warning | `deleteUser` method | Method name does not follow PascalCase | Rename to `DeleteUser` |
| 5 | 🟡 Warning | `connStr` field | Private field missing underscore prefix | Rename to `_connStr` (or better: remove entirely) |
| 6 | 🔵 Info | `GetNames` method | Manual loop with string concat could use LINQ and interpolation | Use `users.Select(u => $"{u.FirstName} {u.LastName}").ToList()` |

## Positive Patterns ✅
- `GetNames` returns a clear, typed result
- Method names are descriptive of their purpose

## Recommendations
1. **[Critical]** Remove hardcoded credentials and use secure configuration
2. **[Critical]** Replace string-concatenated SQL with parameterized queries
3. Fix all naming convention violations to follow C# standards
4. Modernize `GetNames` with LINQ for readability

## Validation Checklist

Before finalizing, verify:
- [ ] All issues include severity, location, and an actionable suggestion
- [ ] No false positives — every reported issue is real and verifiable
- [ ] Positive patterns are acknowledged (at least 1–2)
- [ ] Recommendations are prioritized by impact
- [ ] Report follows the defined output structure
- [ ] Security issues (if any) are marked 🔴 Critical
- [ ] Suggestions respect the target .NET framework version

## References

- [C# Coding Conventions — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [.NET Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/)
- [Secure Coding Guidelines for .NET](https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines)
- [CA Rules — .NET Code Analysis](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/)
